//! Batched exact area integrals for admitted rectangle densities.
//!
//! This is a geometry primitive, not a packing verifier. In particular, zero
//! area for a point or segment is valid for an area integral but cannot discharge
//! a closed-domain coverage obligation in the n=11 capture proof.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

type Rational = BigRational;

const MAX_INPUT_BYTES: usize = 64 * 1024 * 1024;
const MAX_RATIONAL_TOKEN_BYTES: usize = 2048;
const MAX_RATIONAL_BITS: u64 = 4096;
const MAX_RECTANGLES: usize = 100_000;
const MAX_POLYGONS: usize = 100_000;
const MAX_VERTICES: usize = 1_000_000;
const MAX_CONVEXITY_PAIRS: usize = 10_000_000;
const MAX_INTERSECTIONS: usize = 50_000_000;

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct RawBatch {
    version: u32,
    rectangles: Vec<RawRectangle>,
    polygons: Vec<Vec<[String; 2]>>,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct RawOpen {
    version: u32,
    rectangles: Vec<RawRectangle>,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct RawQuery {
    version: u32,
    sequence: u64,
    table_sha256: String,
    polygons: Vec<Vec<[String; 2]>>,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct RawRectangle {
    left: String,
    bottom: String,
    right: String,
    top: String,
    density: String,
}

#[derive(Serialize)]
struct Output {
    version: u32,
    coverages: Vec<String>,
}

#[derive(Serialize)]
struct QueryOutput {
    version: u32,
    sequence: u64,
    table_sha256: String,
    coverages: Vec<String>,
}

#[derive(Clone, PartialEq)]
struct Point {
    x: Rational,
    y: Rational,
}

struct Rectangle {
    left: Rational,
    bottom: Rational,
    right: Rational,
    top: Rational,
    density: Rational,
}

/// A parsed, source-bound rectangle table for one resident exact geometry session.
pub struct DensityTable {
    rectangles: Vec<Rectangle>,
    sha256: String,
    next_sequence: u64,
}

impl DensityTable {
    /// SHA-256 of the exact JSON opening line, excluding its line terminator.
    #[must_use]
    pub fn sha256(&self) -> &str {
        &self.sha256
    }

    /// Number of exact rectangles admitted into this session.
    #[must_use]
    pub fn rectangle_count(&self) -> usize {
        self.rectangles.len()
    }
}

fn integer(token: &str) -> Result<BigInt, String> {
    let digits = token.strip_prefix('-').unwrap_or(token);
    if digits.is_empty() || !digits.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err("rational component is not a decimal integer".into());
    }
    let value = BigInt::parse_bytes(token.as_bytes(), 10)
        .ok_or_else(|| "rational component cannot be parsed".to_string())?;
    if value.bits() > MAX_RATIONAL_BITS {
        return Err("rational component exceeds the bit limit".into());
    }
    Ok(value)
}

fn rational(token: &str) -> Result<Rational, String> {
    if token.len() > MAX_RATIONAL_TOKEN_BYTES {
        return Err("rational token is too long".into());
    }
    if let Some((numerator, denominator)) = token.split_once('/') {
        if denominator.contains('/') {
            return Err("rational token has multiple slashes".into());
        }
        let numerator = integer(numerator)?;
        let denominator = integer(denominator)?;
        if denominator.is_zero() {
            return Err("rational denominator is zero".into());
        }
        Ok(Rational::new(numerator, denominator))
    } else {
        Ok(Rational::from_integer(integer(token)?))
    }
}

fn parse_rectangle(raw: &RawRectangle) -> Result<Rectangle, String> {
    let rectangle = Rectangle {
        left: rational(&raw.left)?,
        bottom: rational(&raw.bottom)?,
        right: rational(&raw.right)?,
        top: rational(&raw.top)?,
        density: rational(&raw.density)?,
    };
    if rectangle.left >= rectangle.right || rectangle.bottom >= rectangle.top {
        return Err("rectangle must have positive width and height".into());
    }
    if rectangle.density < Rational::zero() {
        return Err("rectangle density is negative".into());
    }
    Ok(rectangle)
}

fn cross(a: &Point, b: &Point, c: &Point) -> Rational {
    (&b.x - &a.x) * (&c.y - &b.y) - (&b.y - &a.y) * (&c.x - &b.x)
}

fn parse_polygon(raw: Vec<[String; 2]>) -> Result<Vec<Point>, String> {
    let points: Vec<Point> = raw
        .into_iter()
        .map(|[x, y]| {
            Ok(Point {
                x: rational(&x)?,
                y: rational(&y)?,
            })
        })
        .collect::<Result<_, String>>()?;
    if points.len() < 3 {
        return Ok(points);
    }
    let mut direction = 0_i8;
    for index in 0..points.len() {
        for vertex in &points {
            let turn = cross(&points[index], &points[(index + 1) % points.len()], vertex);
            let sign = match turn.cmp(&Rational::zero()) {
                std::cmp::Ordering::Greater => 1,
                std::cmp::Ordering::Less => -1,
                std::cmp::Ordering::Equal => 0,
            };
            if sign != 0 {
                if direction != 0 && direction != sign {
                    return Err("polygon is not convex".into());
                }
                direction = sign;
            }
        }
    }
    if direction != 0 {
        for first in 0..points.len() {
            for second in first + 1..points.len() {
                if points[first] == points[second]
                    && second != first + 1
                    && !(first == 0 && second == points.len() - 1)
                {
                    return Err("positive-area polygon repeats a vertex".into());
                }
            }
        }
    }
    Ok(points)
}

fn coordinate(point: &Point, axis: usize) -> &Rational {
    if axis == 0 { &point.x } else { &point.y }
}

fn clip_axis(polygon: &[Point], axis: usize, edge: &Rational, keep_ge: bool) -> Vec<Point> {
    if polygon.is_empty() {
        return Vec::new();
    }
    let inside: Vec<bool> = polygon
        .iter()
        .map(|point| {
            if keep_ge {
                coordinate(point, axis) >= edge
            } else {
                coordinate(point, axis) <= edge
            }
        })
        .collect();
    if inside.iter().all(|inside| *inside) {
        return polygon.to_vec();
    }
    if !inside.iter().any(|inside| *inside) {
        return Vec::new();
    }
    let mut output = Vec::with_capacity(polygon.len() + 2);
    let mut previous = &polygon[polygon.len() - 1];
    let mut previous_inside = inside[inside.len() - 1];
    for (current, current_inside) in polygon.iter().zip(inside) {
        if current_inside != previous_inside {
            let factor = (coordinate(previous, axis) - edge)
                / (coordinate(previous, axis) - coordinate(current, axis));
            output.push(Point {
                x: &previous.x + &factor * (&current.x - &previous.x),
                y: &previous.y + &factor * (&current.y - &previous.y),
            });
        }
        if current_inside {
            output.push(current.clone());
        }
        previous = current;
        previous_inside = current_inside;
    }
    output
}

fn intersection_area(rectangle: &Rectangle, polygon: &[Point]) -> Rational {
    let mut clipped = polygon.to_vec();
    for (axis, edge, keep_ge) in [
        (0, &rectangle.left, true),
        (0, &rectangle.right, false),
        (1, &rectangle.bottom, true),
        (1, &rectangle.top, false),
    ] {
        clipped = clip_axis(&clipped, axis, edge, keep_ge);
        if clipped.len() < 3 {
            return Rational::zero();
        }
    }
    let twice_area = clipped
        .iter()
        .enumerate()
        .fold(Rational::zero(), |sum, (index, point)| {
            let next = &clipped[(index + 1) % clipped.len()];
            sum + &point.x * &next.y - &point.y * &next.x
        });
    twice_area.abs() / Rational::from_integer(BigInt::from(2))
}

fn coverage(rectangles: &[Rectangle], polygon: &[Point]) -> Rational {
    if polygon.len() < 3 {
        return Rational::zero();
    }
    let mut left = &polygon[0].x;
    let mut right = left;
    let mut bottom = &polygon[0].y;
    let mut top = bottom;
    for point in &polygon[1..] {
        left = left.min(&point.x);
        right = right.max(&point.x);
        bottom = bottom.min(&point.y);
        top = top.max(&point.y);
    }
    rectangles.iter().fold(Rational::zero(), |sum, rectangle| {
        if rectangle.right <= *left
            || rectangle.left >= *right
            || rectangle.top <= *bottom
            || rectangle.bottom >= *top
        {
            return sum;
        }
        sum + &rectangle.density * intersection_area(rectangle, polygon)
    })
}

fn validate_counts(rectangle_count: usize, polygons: &[Vec<[String; 2]>]) -> Result<(), String> {
    if rectangle_count > MAX_RECTANGLES || polygons.len() > MAX_POLYGONS {
        return Err("batch count limit exceeded".into());
    }
    let vertices = polygons
        .iter()
        .try_fold(0_usize, |sum, polygon| sum.checked_add(polygon.len()))
        .ok_or_else(|| "vertex count overflow".to_string())?;
    if vertices > MAX_VERTICES {
        return Err("batch vertex limit exceeded".into());
    }
    let convexity_pairs = polygons
        .iter()
        .try_fold(0_usize, |sum, polygon| {
            sum.checked_add(polygon.len().checked_mul(polygon.len())?)
        })
        .ok_or_else(|| "convexity work count overflow".to_string())?;
    if convexity_pairs > MAX_CONVEXITY_PAIRS {
        return Err("batch convexity work limit exceeded".into());
    }
    let intersections = rectangle_count
        .checked_mul(polygons.len())
        .ok_or_else(|| "intersection count overflow".to_string())?;
    if intersections > MAX_INTERSECTIONS {
        return Err("batch intersection limit exceeded".into());
    }
    Ok(())
}

fn parse_rectangles(raw: &[RawRectangle]) -> Result<Vec<Rectangle>, String> {
    raw.iter().map(parse_rectangle).collect()
}

fn parse_polygons(raw: Vec<Vec<[String; 2]>>) -> Result<Vec<Vec<Point>>, String> {
    raw.into_iter().map(parse_polygon).collect()
}

fn coverages(rectangles: &[Rectangle], polygons: &[Vec<Point>]) -> Vec<String> {
    polygons
        .iter()
        .map(|polygon| coverage(rectangles, polygon).to_string())
        .collect()
}

/// Parse and bind a fixed rectangle table for a resident JSONL session.
///
/// # Errors
///
/// Refuses an oversized opening line, malformed JSON, unsupported version,
/// invalid exact rectangle, or excessive rectangle count.
pub fn open_session(input: &str) -> Result<DensityTable, String> {
    if input.len() > MAX_INPUT_BYTES {
        return Err("opening line exceeds the input byte limit".into());
    }
    let raw: RawOpen =
        serde_json::from_str(input).map_err(|error| format!("invalid opening JSON: {error}"))?;
    if raw.version != 1 {
        return Err("unsupported session version".into());
    }
    if raw.rectangles.len() > MAX_RECTANGLES {
        return Err("rectangle count limit exceeded".into());
    }
    let rectangles = parse_rectangles(&raw.rectangles)?;
    Ok(DensityTable {
        rectangles,
        sha256: format!("{:x}", Sha256::digest(input.as_bytes())),
        next_sequence: 0,
    })
}

/// Evaluate one complete JSONL request against the previously bound table.
///
/// The request must name the opening-line digest and the next sequence number.
/// A failed request cannot advance the session or yield a partial coverage.
///
/// # Errors
///
/// Refuses malformed, oversized, out-of-order, or invalid geometry requests.
pub fn query_session(table: &mut DensityTable, input: &str) -> Result<String, String> {
    if input.len() > MAX_INPUT_BYTES {
        return Err("query line exceeds the input byte limit".into());
    }
    let raw: RawQuery =
        serde_json::from_str(input).map_err(|error| format!("invalid query JSON: {error}"))?;
    if raw.version != 1 || raw.sequence != table.next_sequence {
        return Err("query version or sequence changed".into());
    }
    if raw.table_sha256 != table.sha256 {
        return Err("query rectangle-table digest changed".into());
    }
    if raw.polygons.is_empty() {
        return Err("query must contain a polygon".into());
    }
    validate_counts(table.rectangles.len(), &raw.polygons)?;
    let polygons = parse_polygons(raw.polygons)?;
    let output = QueryOutput {
        version: 1,
        sequence: raw.sequence,
        table_sha256: table.sha256.clone(),
        coverages: coverages(&table.rectangles, &polygons),
    };
    let encoded = serde_json::to_string(&output)
        .map_err(|error| format!("cannot encode exact output: {error}"))?;
    if encoded.len() > MAX_INPUT_BYTES {
        return Err("response exceeds the byte limit".into());
    }
    table.next_sequence = table
        .next_sequence
        .checked_add(1)
        .ok_or_else(|| "query sequence overflow".to_string())?;
    Ok(encoded)
}

/// Evaluate one bounded JSON batch and return exact rational coverages as JSON.
///
/// Input version 1 has `rectangles` with string-valued rational edges/densities
/// and `polygons` with arrays of rational-string coordinate pairs. Output order
/// matches polygon order. This primitive does not admit a packing candidate or
/// certify that its centre domain was completely searched.
///
/// # Errors
///
/// Refuses malformed, oversized, nonconvex, or unsupported batch input, and
/// reports JSON serialization errors rather than emitting a partial result.
pub fn evaluate(input: &str) -> Result<String, String> {
    if input.len() > MAX_INPUT_BYTES {
        return Err("batch exceeds the input byte limit".into());
    }
    let raw: RawBatch =
        serde_json::from_str(input).map_err(|error| format!("invalid batch JSON: {error}"))?;
    if raw.version != 1 {
        return Err("unsupported batch version".into());
    }
    validate_counts(raw.rectangles.len(), &raw.polygons)?;
    let rectangles = parse_rectangles(&raw.rectangles)?;
    let polygons = parse_polygons(raw.polygons)?;
    let output = Output {
        version: 1,
        coverages: coverages(&rectangles, &polygons),
    };
    serde_json::to_string(&output).map_err(|error| format!("cannot encode exact output: {error}"))
}

#[cfg(test)]
mod tests {
    use super::{evaluate, open_session, query_session};

    #[test]
    fn exact_area_and_tangency() {
        let input = r#"{"version":1,"rectangles":[{"left":"0","bottom":"0","right":"1","top":"1","density":"2"}],"polygons":[[["0","0"],["1","0"],["1","1"],["0","1"]],[["1","0"],["2","0"],["2","1"],["1","1"]],[["1","1"]]]}"#;
        let result = evaluate(input).expect("valid exact batch");
        assert_eq!(result, r#"{"version":1,"coverages":["2","0","0"]}"#);
    }

    #[test]
    fn zero_denominator_and_nonconvex_polygon_refuse() {
        let invalid = r#"{"version":1,"rectangles":[{"left":"0/0","bottom":"0","right":"1","top":"1","density":"1"}],"polygons":[]}"#;
        assert!(
            evaluate(invalid)
                .expect_err("zero denominator must refuse")
                .contains("denominator")
        );
        let nonconvex = r#"{"version":1,"rectangles":[],"polygons":[[["0","0"],["2","0"],["1","1"],["2","2"],["0","2"]]]}"#;
        assert!(
            evaluate(nonconvex)
                .expect_err("nonconvex polygon must refuse")
                .contains("not convex")
        );
        let star = r#"{"version":1,"rectangles":[],"polygons":[[["0","3"],["2","-2"],["-3","1"],["3","1"],["-2","-2"]]]}"#;
        assert!(
            evaluate(star)
                .expect_err("self-crossing star must refuse")
                .contains("not convex")
        );
    }

    #[test]
    fn resident_table_binding_and_monotone_sequence() {
        let opening = r#"{"version":1,"rectangles":[{"left":"0","bottom":"0","right":"1","top":"1","density":"2"}]}"#;
        let mut table = open_session(opening).expect("valid table");
        assert_eq!(table.rectangle_count(), 1);
        let query = format!(
            r#"{{"version":1,"sequence":0,"table_sha256":"{}","polygons":[[["0","0"],["1","0"],["1","1"],["0","1"]]]}}"#,
            table.sha256()
        );
        let answer = query_session(&mut table, &query).expect("first exact query");
        assert!(answer.contains(r#""coverages":["2"]"#));
        assert!(
            query_session(&mut table, &query)
                .expect_err("duplicate sequence must refuse")
                .contains("sequence")
        );
        let changed = query.replace(table.sha256(), "0");
        assert!(
            query_session(
                &mut table,
                &changed.replace("\"sequence\":0", "\"sequence\":1")
            )
            .expect_err("wrong table digest must refuse")
            .contains("digest")
        );
    }
}
