//! Certificate admission: exact parsing, the D4 expansion, and the exact
//! premises (mass, shrink margin, net reach) that the coverage search assumes.

use std::collections::{HashMap, HashSet};
use std::fmt;
use std::io::Read;
use std::path::Path;

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::de::{self, Deserializer, IgnoredAny, MapAccess, SeqAccess, Visitor};
use serde_json::Value;
use sha2::{Digest, Sha256};

use crate::exact::{enclose, parse_rational};
use crate::interval::Iv;

/// The largest container side admitted. The error budget of `SOUNDNESS.md`
/// (lemma F2) is proved for coordinates of magnitude at most `4 * MAX_SIDE`.
pub const MAX_SIDE: i64 = 1000;

/// One expanded rectangle with its exact data.
#[derive(Clone, Debug)]
pub struct ExactRect {
    /// Left edge.
    pub x1: BigRational,
    /// Bottom edge.
    pub y1: BigRational,
    /// Right edge.
    pub x2: BigRational,
    /// Top edge.
    pub y2: BigRational,
    /// Uniform density on the rectangle.
    pub density: BigRational,
}

/// One expanded rectangle as binary64 enclosures, for the interval search.
#[derive(Clone, Copy, Debug)]
pub struct Rect {
    /// Enclosure of the left edge.
    pub x1: Iv,
    /// Enclosure of the right edge.
    pub x2: Iv,
    /// Enclosure of the bottom edge.
    pub y1: Iv,
    /// Enclosure of the top edge.
    pub y2: Iv,
    /// Enclosure of the density.
    pub rho: Iv,
    /// Enclosure of the mass `density * area`.
    pub mass: Iv,
    /// Approximate centre abscissa, for classification with slack.
    pub mx: f64,
    /// Approximate centre ordinate.
    pub my: f64,
    /// Approximate half-width.
    pub wx: f64,
    /// Approximate half-height.
    pub wy: f64,
}

/// An admitted certificate.
#[derive(Clone, Debug)]
pub struct Certificate {
    /// The count the certificate refutes.
    pub n: u64,
    /// Container side `L`.
    pub side: BigRational,
    /// Shrunk square side `B`.
    pub core: BigRational,
    /// Net step `D`.
    pub step: BigRational,
    /// Number of net directions.
    pub angle_count: u32,
    /// Exact total mass.
    pub mass: BigRational,
    /// Number of positive-weight source rectangles.
    pub source_rectangles: usize,
    /// The expanded, merged rectangles with exact data.
    pub exact: Vec<ExactRect>,
    /// The same rectangles as enclosures.
    pub rects: Vec<Rect>,
    /// SHA-256 of the input bytes as read (before decompression).
    pub input_sha256: String,
    /// The coverage threshold the certificate declares, if any.
    pub declared_threshold: Option<BigRational>,
}

/// An admission refusal.
#[derive(Debug)]
pub struct AdmissionError(pub String);

impl fmt::Display for AdmissionError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.0)
    }
}

impl std::error::Error for AdmissionError {}

fn refuse<T>(message: impl Into<String>) -> Result<T, AdmissionError> {
    Err(AdmissionError(message.into()))
}

/// A visitor that walks a JSON document and refuses any object with a repeated
/// key, so that no two readers can disagree about which value a key holds.
struct DuplicateKeyCheck;

impl<'de> de::Deserialize<'de> for DuplicateKeyCheck {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        deserializer.deserialize_any(DuplicateKeyVisitor)
    }
}

struct DuplicateKeyVisitor;

impl<'de> Visitor<'de> for DuplicateKeyVisitor {
    type Value = DuplicateKeyCheck;

    fn expecting(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str("any JSON value")
    }

    fn visit_bool<E>(self, _: bool) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_i64<E>(self, _: i64) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_u64<E>(self, _: u64) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_f64<E>(self, _: f64) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_str<E>(self, _: &str) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_string<E>(self, _: String) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_unit<E>(self) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_none<E>(self) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_seq<A: SeqAccess<'de>>(self, mut seq: A) -> Result<Self::Value, A::Error> {
        while seq.next_element::<DuplicateKeyCheck>()?.is_some() {}
        Ok(DuplicateKeyCheck)
    }
    fn visit_map<A: MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
        let mut seen = HashSet::new();
        while let Some(key) = map.next_key::<String>()? {
            if !seen.insert(key.clone()) {
                return Err(de::Error::custom(format!("duplicate JSON key {key:?}")));
            }
            if key == "$serde_json::private::Number" {
                map.next_value::<IgnoredAny>()?;
            } else {
                map.next_value::<DuplicateKeyCheck>()?;
            }
        }
        Ok(DuplicateKeyCheck)
    }
}

/// Read a candidate file, plain or gzip, returning its raw bytes and decoded JSON.
///
/// # Errors
///
/// Refuses unreadable, oversized, non-JSON or duplicate-key input.
pub fn read_json(path: &Path) -> Result<(Vec<u8>, Value), AdmissionError> {
    let raw = std::fs::read(path)
        .map_err(|error| AdmissionError(format!("cannot read {}: {error}", path.display())))?;
    if raw.len() > 64 * 1024 * 1024 {
        return refuse("candidate exceeds 64 MiB");
    }
    let decoded = if raw.starts_with(&[0x1f, 0x8b]) {
        let mut text = Vec::new();
        flate2::read::GzDecoder::new(raw.as_slice())
            .take(512 * 1024 * 1024)
            .read_to_end(&mut text)
            .map_err(|error| AdmissionError(format!("bad gzip: {error}")))?;
        text
    } else {
        raw.clone()
    };
    serde_json::from_slice::<DuplicateKeyCheck>(&decoded)
        .map_err(|error| AdmissionError(format!("candidate JSON refused: {error}")))?;
    let value: Value = serde_json::from_slice(&decoded)
        .map_err(|error| AdmissionError(format!("candidate JSON refused: {error}")))?;
    Ok((raw, value))
}

fn rational_of(value: &Value, field: &str) -> Result<BigRational, AdmissionError> {
    let token = match value {
        Value::Number(number) => number.to_string(),
        Value::String(text) => text.clone(),
        _ => return refuse(format!("{field} is not a number or rational string")),
    };
    parse_rational(&token).map_err(|error| AdmissionError(format!("{field}: {error}")))
}

fn ratio(p: i64, q: i64) -> BigRational {
    BigRational::new(BigInt::from(p), BigInt::from(q))
}

/// The eight images of `[x1,x2] x [y1,y2]` under the symmetries of `[0,L]^2`.
#[must_use]
pub fn d4_images(
    side: &BigRational,
    x1: &BigRational,
    y1: &BigRational,
    x2: &BigRational,
    y2: &BigRational,
) -> [[BigRational; 4]; 8] {
    let rx1 = side - x2;
    let rx2 = side - x1;
    let ry1 = side - y2;
    let ry2 = side - y1;
    [
        [x1.clone(), y1.clone(), x2.clone(), y2.clone()],
        [rx1.clone(), y1.clone(), rx2.clone(), y2.clone()],
        [x1.clone(), ry1.clone(), x2.clone(), ry2.clone()],
        [rx1.clone(), ry1.clone(), rx2.clone(), ry2.clone()],
        [y1.clone(), x1.clone(), y2.clone(), x2.clone()],
        [ry1.clone(), x1.clone(), ry2.clone(), x2.clone()],
        [y1.clone(), rx1.clone(), y2.clone(), rx2.clone()],
        [ry1, rx1, ry2, rx2],
    ]
}

/// The net direction's exact cosine and sine, `t = r D`, `theta = 2 atan t`.
#[must_use]
pub fn direction(step: &BigRational, index: u32) -> (BigRational, BigRational) {
    let t = step * BigRational::from_integer(BigInt::from(index));
    let one = BigRational::from_integer(BigInt::from(1));
    let denominator = &one + &t * &t;
    let cosine = (&one - &t * &t) / &denominator;
    let sine = (BigRational::from_integer(BigInt::from(2)) * &t) / &denominator;
    (cosine, sine)
}

/// Admit a candidate value for count `n` (and, if given, side `expected_side`).
///
/// # Errors
///
/// Refuses any malformed field and any failed exact premise: the mass must lie
/// strictly between zero and `n`, `0 < B < 1`, `B (1 + D) < 1`, the net must reach
/// past `pi/4`, and every positive rectangle must be a nondegenerate rectangle
/// inside the container.
pub fn admit(
    raw: &[u8],
    value: &Value,
    n: u64,
    expected_side: Option<&BigRational>,
) -> Result<Certificate, AdmissionError> {
    let Value::Object(object) = value else {
        return refuse("candidate JSON must be an object");
    };
    if let Some(declared) = object.get("n")
        && declared.as_u64() != Some(n)
    {
        return refuse(format!(
            "candidate n {declared} does not match requested n {n}"
        ));
    }
    let side = rational_of(
        object.get("L").ok_or(AdmissionError("missing L".into()))?,
        "L",
    )?;
    let core = rational_of(
        object.get("B").ok_or(AdmissionError("missing B".into()))?,
        "B",
    )?;
    if let Some(expected) = expected_side
        && &side != expected
    {
        return refuse(format!(
            "candidate side {side} is not the requested {expected}"
        ));
    }
    let mut step = ratio(83, 40_000);
    let mut angle_count: u32 = 201;
    if let Some(metadata) = object.get("certificate") {
        let Value::Object(metadata) = metadata else {
            return refuse("certificate metadata must be an object");
        };
        if let Some(d) = metadata.get("D") {
            step = rational_of(d, "certificate.D")?;
        }
        if let Some(count) = metadata.get("angle_count") {
            angle_count = count
                .as_u64()
                .and_then(|c| u32::try_from(c).ok())
                .ok_or(AdmissionError("bad angle_count".into()))?;
        }
        for (key, mine) in [("L", &side), ("B", &core)] {
            if let Some(declared) = metadata.get(key)
                && &rational_of(declared, key)? != mine
            {
                return refuse(format!(
                    "certificate metadata {key} disagrees with the candidate"
                ));
            }
        }
    }
    let zero = BigRational::zero();
    let one = ratio(1, 1);
    if !(side.is_positive() && side <= ratio(MAX_SIDE, 1)) {
        return refuse(format!("side {side} outside (0, {MAX_SIDE}]"));
    }
    if !(core > zero && core < one) {
        return refuse("B must lie strictly between 0 and 1");
    }
    if &side * &side < ratio(2, 1) * &core * &core {
        return refuse("L^2 < 2 B^2: the centre domain could be empty");
    }
    if !(step.is_positive() && angle_count >= 2) {
        return refuse("the net needs a positive step and at least two directions");
    }
    if &core * (&one + &step) >= one {
        return refuse("B (1 + D) >= 1: the shrunk square need not fit inside the unit square");
    }
    let last = &step * BigRational::from_integer(BigInt::from(angle_count - 1));
    if &last * &last + ratio(2, 1) * &last - &one <= zero {
        return refuse("the net does not reach past pi/4");
    }
    if last >= one {
        return refuse("the net overshoots pi/2 (t >= 1)");
    }

    let rows = object
        .get("rectangles")
        .and_then(Value::as_array)
        .ok_or(AdmissionError("missing rectangles array".into()))?;
    let weights = object
        .get("weights")
        .and_then(Value::as_array)
        .ok_or(AdmissionError("missing weights array".into()))?;
    if rows.len() != weights.len() {
        return refuse("rectangles and weights differ in length");
    }
    if rows.len() > 1_000_000 {
        return refuse("too many rectangles");
    }
    let mut merged: HashMap<[BigRational; 4], BigRational> = HashMap::new();
    let mut order: Vec<[BigRational; 4]> = Vec::new();
    let mut mass = BigRational::zero();
    let mut source_rectangles = 0usize;
    let eight = ratio(8, 1);
    for (index, (row, weight)) in rows.iter().zip(weights).enumerate() {
        let weight = rational_of(weight, &format!("weight {index}"))?;
        if weight.is_negative() {
            return refuse(format!("weight {index} is negative"));
        }
        let Some(row) = row.as_array().filter(|r| r.len() == 4) else {
            return refuse(format!("rectangle {index} needs four coordinates"));
        };
        // A zero weight puts no mass anywhere, so its coordinates cannot matter.
        if weight.is_zero() {
            continue;
        }
        let coordinates: Vec<BigRational> = row
            .iter()
            .map(|v| rational_of(v, &format!("rectangle {index}")))
            .collect::<Result<_, _>>()?;
        let (x1, y1, x2, y2) = (
            &coordinates[0],
            &coordinates[1],
            &coordinates[2],
            &coordinates[3],
        );
        if !(&zero <= x1 && x1 < x2 && x2 <= &side && &zero <= y1 && y1 < y2 && y2 <= &side) {
            return refuse(format!(
                "positive rectangle {index} is degenerate or outside [0, L]^2"
            ));
        }
        source_rectangles += 1;
        let area = (x2 - x1) * (y2 - y1);
        let density = &weight / (&eight * &area);
        mass += &weight;
        for image in d4_images(&side, x1, y1, x2, y2) {
            if let Some(total) = merged.get_mut(&image) {
                *total += &density;
            } else {
                order.push(image.clone());
                merged.insert(image, density.clone());
            }
        }
    }
    if !(mass.is_positive() && mass < BigRational::from_integer(BigInt::from(n))) {
        return refuse(format!(
            "exact mass {mass} is not strictly between 0 and n = {n}"
        ));
    }
    let mut exact = Vec::with_capacity(order.len());
    let mut rects = Vec::with_capacity(order.len());
    let mut integrated = BigRational::zero();
    for key in order {
        let density = merged[&key].clone();
        let [x1, y1, x2, y2] = key;
        let image_mass = &density * (&x2 - &x1) * (&y2 - &y1);
        let rect = ExactRect {
            x1,
            y1,
            x2,
            y2,
            density,
        };
        rects.push(float_rect(&rect, &image_mass).map_err(AdmissionError)?);
        integrated += image_mass;
        exact.push(rect);
    }
    if integrated != mass {
        return refuse("the D4 expansion does not integrate to the declared mass");
    }
    let declared_threshold = object
        .get("coverage_lower_bound_exact")
        .map(|value| rational_of(value, "coverage_lower_bound_exact"))
        .transpose()?;
    let input_sha256 = Sha256::digest(raw)
        .iter()
        .fold(String::new(), |mut text, byte| {
            use std::fmt::Write;
            let _ = write!(text, "{byte:02x}");
            text
        });
    Ok(Certificate {
        n,
        side,
        core,
        step,
        angle_count,
        mass,
        source_rectangles,
        exact,
        rects,
        input_sha256,
        declared_threshold,
    })
}

/// Binary64 data for one exact rectangle. The edges, density and mass are
/// tight enclosures; the centre and half-sizes are approximations within a
/// few units in the last place, which lemma F2's slack covers.
///
/// # Errors
///
/// Returns a message if a value lies outside the binary64 range.
pub fn float_rect(rect: &ExactRect, mass: &BigRational) -> Result<Rect, String> {
    let x1 = enclose(&rect.x1)?;
    let x2 = enclose(&rect.x2)?;
    let y1 = enclose(&rect.y1)?;
    let y2 = enclose(&rect.y2)?;
    let rho = enclose(&rect.density)?;
    let mass = enclose(mass)?;
    Ok(Rect {
        x1,
        x2,
        y1,
        y2,
        rho,
        mass,
        mx: f64::midpoint(x1.lo, x2.lo),
        my: f64::midpoint(y1.lo, y2.lo),
        wx: 0.5 * (x2.lo - x1.lo),
        wy: 0.5 * (y2.lo - y1.lo),
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn images_preserve_area_and_cover_the_orbit() {
        let side = ratio(10, 1);
        let images = d4_images(
            &side,
            &ratio(1, 1),
            &ratio(2, 1),
            &ratio(3, 1),
            &ratio(7, 1),
        );
        let unique: HashSet<_> = images.iter().cloned().collect();
        assert_eq!(unique.len(), 8);
        for [x1, y1, x2, y2] in &images {
            assert_eq!((x2 - x1) * (y2 - y1), ratio(10, 1));
        }
    }

    #[test]
    fn net_directions_are_rational_rotations() {
        let (c, s) = direction(&ratio(83, 40_000), 7);
        assert_eq!(&c * &c + &s * &s, ratio(1, 1));
        assert!(c.is_positive() && s.is_positive());
    }
}
