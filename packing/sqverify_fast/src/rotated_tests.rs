//! Property and differential tests of the rotated-direction bounds against the
//! exact rational oracle.

use super::*;
use crate::certificate::ExactRect;
use crate::exact::of_f64;
use crate::oracle::{intersection_area, square};
use num_traits::ToPrimitive;

fn ratio(p: i64, q: i64) -> BigRational {
    BigRational::new(BigInt::from(p), BigInt::from(q))
}

fn lcg(state: &mut u64) -> f64 {
    *state = state
        .wrapping_mul(6_364_136_223_846_793_005)
        .wrapping_add(1_442_695_040_888_963_407);
    (*state >> 11) as f64 / (1u64 << 53) as f64
}

pub(crate) fn test_cert(rects: Vec<ExactRect>) -> Certificate {
    let floats = rects
        .iter()
        .map(|r| {
            let mass = &r.density * (&r.x2 - &r.x1) * (&r.y2 - &r.y1);
            crate::certificate::float_rect(r, &mass).unwrap()
        })
        .collect();
    Certificate {
        n: 100,
        side: ratio(6, 1),
        core: ratio(9977, 10000),
        step: ratio(83, 40000),
        angle_count: 201,
        mass: ratio(1, 1),
        source_rectangles: rects.len(),
        exact: rects,
        rects: floats,
        input_sha256: String::new(),
        declared_threshold: None,
    }
}

fn random_rects(state: &mut u64, count: usize) -> Vec<ExactRect> {
    (0..count)
        .map(|_| {
            let x = (lcg(state) * 4_000_000.0) as i64 + 1_000_000;
            let y = (lcg(state) * 4_000_000.0) as i64 + 1_000_000;
            let w = (lcg(state) * 900_000.0) as i64 + 1_000;
            let h = (lcg(state) * 900_000.0) as i64 + 1_000;
            ExactRect {
                x1: ratio(x, 1_000_000),
                y1: ratio(y, 1_000_000),
                x2: ratio(x + w, 1_000_000),
                y2: ratio(y + h, 1_000_000),
                density: ratio(1, 1),
            }
        })
        .collect()
}

#[test]
fn area_lower_bound_is_below_and_close_to_exact() {
    let mut state = 7u64;
    let cert = test_cert(random_rects(&mut state, 300));
    for index in [1u32, 2, 37, 100, 199, 200] {
        let fr = frame(&cert, index).unwrap();
        let (c, s) = direction(&cert.step, index);
        for _ in 0..12 {
            let x0 = 2.0 + 2.0 * lcg(&mut state);
            let y0 = 2.0 + 2.0 * lcg(&mut state);
            let polygon = square(&of_f64(x0), &of_f64(y0), &c, &s, &cert.core);
            for (exact, rect) in cert.exact.iter().zip(&cert.rects) {
                let truth = intersection_area(exact, &polygon);
                let bound = area_dn(&fr, rect, x0, y0);
                assert!(
                    of_f64(bound) <= truth,
                    "area bound {bound} above exact {} at r={index}",
                    truth.to_f64().unwrap()
                );
                let gap = truth.to_f64().unwrap() - bound;
                assert!(
                    gap < 1e-9,
                    "area bound {bound} loose by {gap} at r={index}, rect {rect:?}, centre ({x0}, {y0})"
                );
            }
        }
    }
}

/// Exact length of the vertical segment `{a} x [b, e]` inside the square of
/// direction `(c, s)` and half-side `h` centred at `(x, y)`.
fn exact_vertical_length(
    a: &BigRational,
    b: &BigRational,
    e: &BigRational,
    x: &BigRational,
    y: &BigRational,
    c: &BigRational,
    s: &BigRational,
    h: &BigRational,
) -> BigRational {
    let xi = a - x;
    let f1 = (h - c * &xi) / s;
    let f2 = (h + s * &xi) / c;
    let g1 = (-h - c * &xi) / s;
    let g2 = (s * &xi - h) / c;
    let top = (e - y).min(f1).min(f2);
    let bottom = (b - y).max(g1).max(g2);
    let length = top - bottom;
    if length > BigRational::from_integer(BigInt::from(0)) {
        length
    } else {
        BigRational::from_integer(BigInt::from(0))
    }
}

#[test]
fn edge_length_enclosures_contain_exact_lengths_over_the_box() {
    let mut state = 11u64;
    let cert = test_cert(random_rects(&mut state, 4));
    let two = ratio(2, 1);
    let h = &cert.core / &two;
    for index in [1u32, 2, 50, 133, 200] {
        let fr = frame(&cert, index).unwrap();
        let (c, s) = direction(&cert.step, index);
        for _ in 0..400 {
            let x0 = 3.0 + lcg(&mut state);
            let y0 = 3.0 + lcg(&mut state);
            let dx = 10f64.powf(-1.0 - 4.0 * lcg(&mut state));
            let dy = 10f64.powf(-1.0 - 4.0 * lcg(&mut state));
            // A vertical segment near the square's boundary, so all regimes occur.
            let a = x0 + (lcg(&mut state) - 0.5) * 1.4;
            let b = y0 + (lcg(&mut state) - 0.5) * 1.6;
            let e = b + lcg(&mut state) * 0.6 + 1e-6;
            let w = offset(Iv::point(a), x0, dx);
            let ev = offset(Iv::point(e), y0, dy);
            let bv = offset(Iv::point(b), y0, dy);
            let len = Iv::point(e).minus(Iv::point(b));
            let enclosure = segment_length(&fr.vertical, w, ev, bv, len);
            for (u, v) in [
                (-1.0, -1.0),
                (1.0, 1.0),
                (-1.0, 1.0),
                (0.3, -0.7),
                (0.0, 0.0),
            ] {
                let px = of_f64(x0) + of_f64(u) * of_f64(dx);
                let py = of_f64(y0) + of_f64(v) * of_f64(dy);
                let exact =
                    exact_vertical_length(&of_f64(a), &of_f64(b), &of_f64(e), &px, &py, &c, &s, &h);
                assert!(
                    of_f64(enclosure.lo) <= exact && exact <= of_f64(enclosure.hi),
                    "r={index}: {enclosure:?} misses {}",
                    exact.to_f64().unwrap()
                );
            }
        }
    }
}
