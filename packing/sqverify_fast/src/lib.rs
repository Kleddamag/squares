//! Clean-room verifier for measure-capture lower-bound certificates.
//!
//! A certificate is a nonnegative measure on `[0, L]^2` of total mass below
//! `n`. It proves `s(n) >= L` if every unit square in the container captures
//! mass at least one. The net-and-shrink argument reduces that to finitely
//! many directions, at each of which every centre of a shrunk square of side
//! `B` must capture the threshold. `SOUNDNESS.md` beside this crate states and
//! proves every lemma the code relies on; `INDEPENDENCE.md` records what was
//! read and run while writing it.

pub mod axis;
pub mod certificate;
pub mod exact;
pub mod interval;
pub mod oracle;
pub mod rotated;

use num_rational::BigRational;
use serde_json::{Value, json};

use crate::certificate::{Certificate, direction};
use crate::exact::of_f64;
use crate::rotated::{Limits, Verdict};

/// The receipt for one direction.
#[derive(Clone, Debug)]
pub struct DirectionReport {
    /// Net index.
    pub index: u32,
    /// Whether the direction is verified.
    pub verified: bool,
    /// Wall seconds.
    pub seconds: f64,
    /// The JSON receipt.
    pub receipt: Value,
}

/// Verify one direction and build its receipt.
///
/// `threshold` is exact; the search compares against the upper end of its
/// binary64 enclosure. With `confirm`, a counterexample candidate is
/// re-evaluated in exact rationals.
///
/// # Errors
///
/// Returns a message when a constant cannot be enclosed.
pub fn run_direction(
    cert: &Certificate,
    index: u32,
    threshold: &BigRational,
    limits: Limits,
    confirm: bool,
) -> Result<DirectionReport, String> {
    let threshold_hi = crate::exact::enclose(threshold)?.hi;
    if index == 0 {
        let start = std::time::Instant::now();
        let result = crate::axis::verify_axis(cert, threshold_hi)?;
        let seconds = start.elapsed().as_secs_f64();
        let receipt = json!({
            "r": 0,
            "method": "axis-vertex-sweep",
            "verdict": if result.verified { "verified" } else { "refused" },
            "x_events": result.x_events,
            "y_events": result.y_events,
            "vertices": result.x_events * result.y_events,
            "min_certified_lower_bound": result.min_lower,
            "argmin": [result.argmin.0, result.argmin.1],
            "seconds": seconds,
        });
        return Ok(DirectionReport { index, verified: result.verified, seconds, receipt });
    }
    let result = crate::rotated::verify_direction(cert, index, threshold_hi, limits)?;
    let mut receipt = json!({
        "r": index,
        "method": "interval-branch-and-bound",
        "verdict": result.verdict.as_str(),
        "nodes": result.nodes,
        "leaves": result.leaves,
        "max_depth": result.max_depth,
        "min_certified_lower_bound": if result.min_lower.is_finite() { json!(result.min_lower) } else { Value::Null },
        "mean_boundary_rectangles": result.mean_boundary,
        "seconds": result.seconds,
    });
    if let Some((x, y, dx, dy)) = result.argmin {
        receipt["least_bound_box"] = json!({"x": x, "y": y, "dx": dx, "dy": dy});
    }
    if let Some((x, y, value)) = result.witness {
        receipt["witness"] = json!({"x": x, "y": y, "centre_lower_bound": value});
        if confirm && result.verdict == Verdict::CounterexampleCandidate {
            let (c, s) = direction(&cert.step, index);
            let exact = crate::oracle::coverage(cert, &of_f64(x), &of_f64(y), &c, &s);
            receipt["witness"]["exact_coverage"] = json!(exact.to_string());
            receipt["witness"]["exact_below_threshold"] = json!(&exact < threshold);
        }
    }
    Ok(DirectionReport {
        index,
        verified: result.verdict == Verdict::Verified,
        seconds: result.seconds,
        receipt,
    })
}

/// The certificate-level premises, for the summary receipt.
#[must_use]
pub fn premises(cert: &Certificate) -> Value {
    json!({
        "n": cert.n,
        "L": cert.side.to_string(),
        "B": cert.core.to_string(),
        "D": cert.step.to_string(),
        "angle_count": cert.angle_count,
        "mass_exact": cert.mass.to_string(),
        "mass_below_n": (BigRational::from_integer(cert.n.into()) - &cert.mass).to_string(),
        "source_rectangles": cert.source_rectangles,
        "expanded_rectangles": cert.exact.len(),
        "input_sha256": cert.input_sha256,
    })
}
