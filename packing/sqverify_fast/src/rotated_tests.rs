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
                assert!(gap < 1e-9, "area bound {bound} loose by {gap} at r={index}, rect {rect:?}, centre ({x0}, {y0})");
            }
        }
    }
}
