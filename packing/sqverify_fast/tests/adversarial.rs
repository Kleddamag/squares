//! Adversarial soundness tests from the 3 October soundness review
//! (`docs/project/reviews/review-2026-10-03-sqverify-fast-soundness.md`).
//!
//! Each test builds a certificate or a box aimed at one suspected weakness and
//! compares the verifier's certified bounds with the exact rational oracle. A
//! test marked `ignore` reproduces an open defect: it fails on the reviewed
//! build and should pass, un-ignored, once the defect is fixed.

use num_bigint::BigInt;
use num_rational::BigRational;
use serde_json::{Value, json};
use sqverify_fast::certificate::{Certificate, admit, direction, domain_upper};
use sqverify_fast::exact::{of_f64, parse_rational};
use sqverify_fast::oracle::coverage;
use sqverify_fast::rotated::{Limits, box_lower_bound, centre_lower_bound};

fn ratio(p: i64, q: i64) -> BigRational {
    BigRational::new(BigInt::from(p), BigInt::from(q))
}

fn text(q: &BigRational) -> String {
    format!("{}/{}", q.numer(), q.denom())
}

fn admit_value(value: &Value, n: u64) -> Result<Certificate, String> {
    let raw = value.to_string().into_bytes();
    admit(&raw, value, n, None).map_err(|error| error.0)
}

const LIMITS: Limits = Limits {
    max_nodes: 2_000_000,
    max_depth: 60,
    audit_every: 1024,
    inject_fault_at: None,
};

// ---------------------------------------------------------------- admission

#[test]
fn decimal_masses_are_exact_and_the_mass_premise_is_strict() {
    // 0.1 + 0.2 is 0.3 exactly, which binary64 would deny; total_mass is checked
    // against the exact sum.
    let base = |weights: Value, total: &str| {
        json!({"n": 1, "L": "3", "B": "9/10", "total_mass": total,
            "rectangles": [{"rectangle": [0, 0, 1, 1], "mass": weights[0]},
                           {"rectangle": [1, 1, 2, 2], "mass": weights[1]}],
            "points": []})
    };
    assert!(admit_value(&base(json!([0.1, 0.2]), "0.3"), 1).is_ok());
    assert!(admit_value(&base(json!([0.1, 0.2]), "0.30000000000000004"), 1).is_err());
    // A mass equal to n, written as decimals that sum to it exactly, is refused;
    // one part in 10^40 below it is admitted.
    let at_n = base(
        json!(["0.9999999999999999999999999999999999999999", "1e-40"]),
        "1",
    );
    assert!(admit_value(&at_n, 1).is_err());
    let below = base(
        json!(["0.9999999999999999999999999999999999999998", "1e-40"]),
        "0.9999999999999999999999999999999999999999",
    );
    assert!(admit_value(&below, 1).is_ok());
}

#[test]
fn admission_refuses_each_broken_premise() {
    let good = json!({"L": "3", "B": "9/10", "rectangles": [[0, 0, 1, 1]], "weights": [1]});
    assert!(admit_value(&good, 2).is_ok());
    let variants = [
        // B (1 + D) = 1 exactly
        json!({"L": "3", "B": "40000/40083", "rectangles": [[0, 0, 1, 1]], "weights": [1]}),
        // a negative weight balanced by a positive one
        json!({"L": "3", "B": "9/10", "rectangles": [[0, 0, 1, 1], [1, 1, 2, 2]], "weights": [2, -1]}),
        // a rectangle poking out of the container by 10^-30
        json!({"L": "3", "B": "9/10", "rectangles": [[0, 0, 1, "3.000000000000000000000000000001"]], "weights": [1]}),
        // a degenerate rectangle
        json!({"L": "3", "B": "9/10", "rectangles": [[1, 0, 1, 1]], "weights": [1]}),
        // a net that stops one step short of pi/4 (t_199 < tan(pi/8))
        json!({"L": "3", "B": "9/10", "rectangles": [[0, 0, 1, 1]], "weights": [1],
               "certificate": {"angle_count": 200}}),
        // metadata that disagrees with the candidate's side
        json!({"L": "3", "B": "9/10", "rectangles": [[0, 0, 1, 1]], "weights": [1],
               "certificate": {"L": "3.0000000000000000001"}}),
        // format L with a different net
        json!({"schema": "point_line_rectangle_v1", "L": "3", "B": "9/10",
               "net": {"step": "83/40001", "last": 200},
               "primitives": [{"kind": "point", "geometry": [1, 1], "mass": 1}]}),
        // format L, a segment of length zero
        json!({"schema": "point_line_rectangle_v1", "L": "3", "B": "9/10",
               "net": {"step": "83/40000", "last": 200},
               "primitives": [{"kind": "segment", "geometry": [1, 1, 1, 1], "mass": 1}]}),
    ];
    for (index, variant) in variants.iter().enumerate() {
        assert!(
            admit_value(variant, 2).is_err(),
            "variant {index} was admitted"
        );
    }
}

#[test]
fn duplicate_keys_are_refused_before_any_reader_disagrees() {
    let dir = std::env::temp_dir().join(format!("sqverify-adv-{}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    let path = dir.join("dup.json");
    std::fs::write(
        &path,
        r#"{"L": "3", "B": "9/10", "rectangles": [[0, 0, 1, 1]], "weights": [1], "weights": [0.5]}"#,
    )
    .unwrap();
    assert!(sqverify_fast::certificate::read_json(&path).is_err());
    std::fs::remove_dir_all(&dir).unwrap();
}

// ------------------------------------------------- boxes at the F2 extremes

/// A format L certificate at side 1000 (the largest admitted, where lemma F2's
/// slack is tightest) whose rectangles, points and segments sit exactly on the
/// boundary of the square at `(x0, y0)` and direction `index`: the square's
/// axis-aligned bounding box, a sliver along each square edge, every vertex as
/// a point, and every square edge as a segment.
fn boundary_cert(index: u32, x0: f64, y0: f64) -> Certificate {
    let side = ratio(1000, 1);
    let core = ratio(9977, 10000);
    let (c, s) = direction(&ratio(83, 40000), index);
    let corners = sqverify_fast::oracle::square(&of_f64(x0), &of_f64(y0), &c, &s, &core);
    let xs: Vec<&BigRational> = corners.iter().map(|p| &p.0).collect();
    let ys: Vec<&BigRational> = corners.iter().map(|p| &p.1).collect();
    let (left, right) = (
        (*xs.iter().min().expect("four corners")).clone(),
        (*xs.iter().max().expect("four corners")).clone(),
    );
    let (bottom, top) = (
        (*ys.iter().min().expect("four corners")).clone(),
        (*ys.iter().max().expect("four corners")).clone(),
    );
    let eps = ratio(1, 1_000_000_000_000);
    let mut primitives = vec![
        json!({"kind": "rectangle", "geometry": [text(&left), text(&bottom), text(&right), text(&top)], "mass": "1"}),
        // slivers of width 10^-12 hugging each side of the bounding box from inside
        json!({"kind": "rectangle", "geometry": [text(&left), text(&bottom), text(&(&left + &eps)), text(&top)], "mass": "1"}),
        json!({"kind": "rectangle", "geometry": [text(&(&right - &eps)), text(&bottom), text(&right), text(&top)], "mass": "1"}),
        json!({"kind": "rectangle", "geometry": [text(&left), text(&(&top - &eps)), text(&right), text(&top)], "mass": "1"}),
    ];
    for (k, p) in corners.iter().enumerate() {
        let q = &corners[(k + 1) % 4];
        primitives
            .push(json!({"kind": "point", "geometry": [text(&p.0), text(&p.1)], "mass": "1"}));
        primitives.push(json!({"kind": "segment", "geometry": [text(&p.0), text(&p.1), text(&q.0), text(&q.1)], "mass": "1"}));
        // a segment from the vertex straight outward, touching the square at one point
        let out = (&p.0 + (&p.0 - of_f64(x0)), &p.1 + (&p.1 - of_f64(y0)));
        primitives.push(json!({"kind": "segment", "geometry": [text(&p.0), text(&p.1), text(&out.0), text(&out.1)], "mass": "1"}));
    }
    let value = json!({"schema": "point_line_rectangle_v1", "L": text(&side), "B": text(&core),
        "net": {"step": "83/40000", "last": 200}, "primitives": primitives});
    admit_value(&value, 1_000_000).expect("boundary certificate is admissible")
}

#[test]
fn box_bounds_never_exceed_exact_capture_on_boundary_configurations() {
    let mut checked = 0;
    for index in [0u32, 1, 57, 133, 200] {
        let cert = boundary_cert(index, 700.123_456_789, 811.987_654_321);
        let (c, s) = direction(&cert.step, index);
        for &(x0, y0) in &[
            (700.123_456_789, 811.987_654_321),
            (700.123_456_789 + 3e-10, 811.987_654_321),
        ] {
            let centre = centre_lower_bound(&cert, index, x0, y0).unwrap();
            let exact = coverage(&cert, &of_f64(x0), &of_f64(y0), &c, &s);
            assert!(
                of_f64(centre) <= exact,
                "r={index} centre {centre} > {exact}"
            );
            for &d in &[0.0, 1e-12, 1e-9, 1e-6, 1e-3, 0.25] {
                for &(dx, dy) in &[(d, d), (d, 0.0), (0.0, d), (d, 2.0 * d)] {
                    let bound = box_lower_bound(&cert, index, x0, y0, dx, dy).unwrap();
                    for (sx, sy) in [
                        (-1.0, -1.0),
                        (1.0, -1.0),
                        (-1.0, 1.0),
                        (1.0, 1.0),
                        (0.0, 0.0),
                        (0.37, -0.81),
                    ] {
                        let (px, py) = (x0 + sx * dx, y0 + sy * dy);
                        // Only poses inside the box the bound speaks for.
                        if (px - x0).abs() > dx || (py - y0).abs() > dy {
                            continue;
                        }
                        let truth = coverage(&cert, &of_f64(px), &of_f64(py), &c, &s);
                        assert!(
                            of_f64(bound) <= truth,
                            "r={index} box ({x0},{y0})+-({dx},{dy}) bound {bound} above exact at ({px},{py})"
                        );
                        checked += 1;
                    }
                }
            }
        }
    }
    assert!(checked > 500);
}

// ------------------------------------------------------- the domain premise

#[test]
fn per_bin_domain_needs_the_fold_at_pi_over_four() {
    // Lemma D's per-bin domain is the least half-width over [a_r, tan(pi/8)];
    // at r = 200 the bin [t - D/2, t + D/2] reaches past tan(pi/8), where the
    // half-width rho falls again. A unit square at half-angle t_200 + D/2 has a
    // half-width below rho(a_200): the domain is valid only because orientations
    // above pi/4 are folded by the diagonal (spec N5), not merely those above
    // theta_max (SOUNDNESS.md step N2).
    let rho = |a: &BigRational| {
        let one = ratio(1, 1);
        let two = ratio(2, 1);
        (&one + &two * a - a * a) / (&two * (&one + a * a))
    };
    let d = ratio(83, 40000);
    let t = &d * ratio(200, 1);
    let a = &t - &d / ratio(2, 1);
    let far = &t + &d / ratio(2, 1);
    assert!(rho(&far) < rho(&a));
    let value = json!({"n": 3, "L": "3", "B": "9/10", "points": [],
        "rectangles": [{"rectangle": [0, 0, 1, 1], "mass": 1}]});
    let cert = admit_value(&value, 3).unwrap();
    assert_eq!(domain_upper(&cert, 200).unwrap(), ratio(3, 1) - rho(&a));
}

// ------------------------------------------------- non-finite intermediates

/// The certificate of finding S1, as JSON: a band of density 2 that every
/// centre on the domain's lower edge captures in full, plus twenty slivers of
/// height 2^-1000 ending at ordinate `top` whose summed slope steps overflow in
/// the axis sweep, with weight `weight` each. At `(3.5, 3.5)`, inside the r = 0
/// domain `[2, 3.55]^2`, the exact capture is zero.
fn overflow_value(top: &BigRational, weight: &str) -> Value {
    let den = BigInt::from(1) << 1000usize;
    let y1 = top - BigRational::new(BigInt::from(1), den);
    let mut rects = vec![json!(["0", "3/2", "4", "5/2"])];
    let mut weights = vec![json!("16")];
    for k in 0..20 {
        rects.push(json!([
            text(&ratio(k, 1000)),
            text(&y1),
            text(&(ratio(4, 1) - ratio(k, 1000))),
            text(top)
        ]));
        weights.push(json!(weight));
    }
    json!({"L": "4", "B": "9/10", "rectangles": rects, "weights": weights})
}

/// The S1 certificate past admission. Lemma F3's density cap refuses it, so it
/// is admitted with tiny sliver weights and the slivers' densities are then
/// raised to about 1.5e307 in place: the sweep itself meets the overflow.
fn overflow_cert(top: &BigRational) -> Certificate {
    let light = overflow_value(top, &format!("1/{}", BigInt::from(1) << 950usize));
    let mut cert = admit_value(&light, 1_000_000_000).expect("the light version is admissible");
    let huge = ratio(15, 1) * BigRational::from_integer(BigInt::from(10).pow(306));
    for (exact, rect) in cert.exact.iter_mut().zip(cert.rects.iter_mut()) {
        if &exact.y2 - &exact.y1 < ratio(1, 1_000_000) {
            exact.density = huge.clone();
            rect.rho = sqverify_fast::interval::Iv::point(1.5e307);
        }
    }
    cert
}

#[test]
fn admission_refuses_the_overflow_densities() {
    // Lemma F3's cap: the slivers' densities, about 1.5e307, exceed 2^96.
    let value = overflow_value(&ratio(49, 20), "22000000");
    let error = admit_value(&value, 1_000_000_000).expect_err("the S1 certificate was admitted");
    assert!(error.contains("density"), "{error}");
}

#[test]
fn overflow_certificate_has_an_uncovered_centre() {
    // The witness half of S1: a centre of the r = 0 domain captures nothing.
    let cert = overflow_cert(&ratio(49, 20));
    assert!(domain_upper(&cert, 0).unwrap() >= ratio(71, 20));
    let exact = coverage(
        &cert,
        &ratio(7, 2),
        &ratio(7, 2),
        &ratio(1, 1),
        &ratio(0, 1),
    );
    assert_eq!(exact, ratio(0, 1));
}

#[test]
fn axis_sweep_refuses_the_overflow_certificate() {
    // The slivers' steps lie just below the domain: the overflow is in the
    // initial slope.
    let cert = overflow_cert(&ratio(49, 20));
    let threshold = parse_rational("1").unwrap();
    let report = sqverify_fast::run_direction(&cert, 0, &threshold, LIMITS, false).unwrap();
    assert!(!report.verified, "direction 0 verified: {}", report.receipt);
    assert_eq!(
        report.receipt["verdict"], "non-finite",
        "{}",
        report.receipt
    );
}

#[test]
fn axis_sweep_refuses_an_overflow_inside_the_domain() {
    // The second reproducer: slivers ending at ordinate 3 put their steps at
    // about 2.55, inside the domain [2, 3.55], so the overflow arises in a
    // column's step list rather than its initial slope.
    let cert = overflow_cert(&ratio(3, 1));
    let threshold = parse_rational("1").unwrap();
    let report = sqverify_fast::run_direction(&cert, 0, &threshold, LIMITS, false).unwrap();
    assert!(!report.verified, "direction 0 verified: {}", report.receipt);
    assert_eq!(
        report.receipt["verdict"], "non-finite",
        "{}",
        report.receipt
    );
}

#[test]
fn a_fault_injected_run_is_never_verified() {
    // Finding S2: with the audit sampled too sparsely to see it, an injected
    // fault must still not yield a verified receipt, and the receipt names it.
    let value = json!({"L": "3", "B": "9/10",
        "rectangles": [[0, 0, 3, 3]], "weights": [8]});
    let cert = admit_value(&value, 9).unwrap();
    let threshold = parse_rational("1/2").unwrap();
    let limits = Limits {
        audit_every: 1 << 40,
        inject_fault_at: Some(2),
        ..LIMITS
    };
    for index in [0u32, 1, 100] {
        let report = sqverify_fast::run_direction(&cert, index, &threshold, limits, false).unwrap();
        assert!(!report.verified, "r={index}: {}", report.receipt);
        assert_eq!(
            report.receipt["fault_injected_at_box"], 2,
            "{}",
            report.receipt
        );
        let clean = sqverify_fast::run_direction(&cert, index, &threshold, LIMITS, false).unwrap();
        assert!(
            clean.verified,
            "r={index} clean run refused: {}",
            clean.receipt
        );
    }
}
