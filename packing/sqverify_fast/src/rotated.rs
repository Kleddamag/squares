//! Directions `r >= 1`: interval branch and bound over centre boxes.
//!
//! For a box of centres with midpoint `c0` and half-widths `(dx, dy)` the
//! accepted bound is
//!
//! `F(c) >= F(c0) - Gx dx - Gy dy`,
//!
//! where `Gx`, `Gy` bound `|dF/dx|`, `|dF/dy|` over the whole box (lemma R3 of
//! `SOUNDNESS.md`). Rectangles certified inside the common core of every square
//! in the box contribute their whole mass and no derivative; rectangles
//! certified outside every square contribute nothing (lemma R1). The others
//! contribute a certified lower bound on their overlap area at `c0` (lemma R2,
//! concave sections and trapezoids) and an enclosure of their edge-length
//! derivative (lemmas R4, R5).

use std::time::Instant;

use num_bigint::BigInt;
use num_rational::BigRational;

use crate::certificate::{Certificate, Rect, direction};
use crate::exact::{approx, enclose};
use crate::interval::{Iv, add_dn, add_up, dn, mul_dn, mul_up, sub_dn, sub_up, up};

/// Absolute slack for classification decisions made in plain binary64
/// (lemma F2: the rounding error of those expressions is below `1e-11` for
/// sides up to `MAX_SIDE`).
pub const TAU: f64 = 1e-9;

/// Search limits for one direction.
#[derive(Clone, Copy, Debug)]
pub struct Limits {
    /// Node budget; exceeding it leaves the direction unresolved.
    pub max_nodes: u64,
    /// Depth budget; exceeding it leaves the direction unresolved.
    pub max_depth: u32,
}

/// The verdict of one direction.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Verdict {
    /// Every box of the reduced centre domain was accepted.
    Verified,
    /// A box centre's lower bound is below the threshold by more than the
    /// arithmetic could explain; the centre is reported for exact confirmation.
    CounterexampleCandidate,
    /// A budget ran out first.
    Unresolved,
}

impl Verdict {
    /// The receipt spelling.
    #[must_use]
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Verified => "verified",
            Self::CounterexampleCandidate => "counterexample-candidate",
            Self::Unresolved => "unresolved",
        }
    }
}

/// The outcome of one rotated direction.
#[derive(Clone, Debug)]
pub struct DirectionResult {
    /// Net index.
    pub index: u32,
    /// Verdict.
    pub verdict: Verdict,
    /// Boxes evaluated.
    pub nodes: u64,
    /// Boxes accepted.
    pub leaves: u64,
    /// Deepest box evaluated.
    pub max_depth: u32,
    /// Least accepted lower bound (a certified lower bound on the minimum).
    pub min_lower: f64,
    /// Centre and half-widths of the accepted box with the least bound.
    pub argmin: Option<(f64, f64, f64, f64)>,
    /// For a non-verified direction, the box centre that stopped the search.
    pub witness: Option<(f64, f64, f64)>,
    /// Wall seconds of this direction's search.
    pub seconds: f64,
    /// Mean number of boundary rectangles per evaluated box.
    pub mean_boundary: f64,
}

/// Coefficients of the four boundary lines of a centred square, seen from a
/// family of parallel lines (vertical or horizontal), as enclosures.
#[derive(Clone, Copy, Debug)]
struct LineCoeffs {
    /// `h/s` for vertical lines (`h/c` for horizontal ones), and so on with
    /// cosine and sine exchanged.
    hs: Iv,
    hc: Iv,
    cs: Iv,
    sc: Iv,
    isc: Iv,
    two_hs: Iv,
    two_hc: Iv,
    hsum: Iv,
}

/// Per-direction constants.
#[derive(Clone, Copy, Debug)]
struct Frame {
    cf: f64,
    sf: f64,
    hf: f64,
    vertical: LineCoeffs,
    horizontal: LineCoeffs,
}

fn quotient(p: &BigRational, q: &BigRational) -> Result<Iv, String> {
    enclose(&(p / q))
}

fn frame(cert: &Certificate, index: u32) -> Result<Frame, String> {
    let (c, s) = direction(&cert.step, index);
    let two = BigRational::from_integer(BigInt::from(2));
    let h = &cert.core / &two;
    let one = BigRational::from_integer(BigInt::from(1));
    let vertical = LineCoeffs {
        hs: quotient(&h, &s)?,
        hc: quotient(&h, &c)?,
        cs: quotient(&c, &s)?,
        sc: quotient(&s, &c)?,
        isc: quotient(&one, &(&s * &c))?,
        two_hs: quotient(&(&two * &h), &s)?,
        two_hc: quotient(&(&two * &h), &c)?,
        hsum: enclose(&(&h / &s + &h / &c))?,
    };
    let horizontal = LineCoeffs {
        hs: vertical.hc,
        hc: vertical.hs,
        cs: vertical.sc,
        sc: vertical.cs,
        isc: vertical.isc,
        two_hs: vertical.two_hc,
        two_hc: vertical.two_hs,
        hsum: vertical.hsum,
    };
    Ok(Frame {
        cf: approx(&c)?,
        sf: approx(&s)?,
        hf: approx(&h)?,
        vertical,
        horizontal,
    })
}

/// Lower bound on `k * x` for an interval `k >= 0` and a value `x`.
#[inline]
fn kx_dn(k: Iv, x: f64) -> f64 {
    if x >= 0.0 {
        mul_dn(k.lo, x)
    } else {
        mul_dn(k.hi, x)
    }
}

/// Upper bound on `k * x` for an interval `k >= 0` and a value `x`.
#[inline]
fn kx_up(k: Iv, x: f64) -> f64 {
    if x >= 0.0 {
        mul_up(k.hi, x)
    } else {
        mul_up(k.lo, x)
    }
}

/// Lower bound of `h(xi) = min(e, f1, f2) - max(b, g1, g2)` at offset `xi`,
/// where `e` is a lower and `b` an upper bound of the segment's offsets.
#[inline]
fn section_dn(k: &LineCoeffs, xi: f64, e: f64, b: f64) -> f64 {
    let f1 = sub_dn(k.hs.lo, kx_up(k.cs, xi));
    let f2 = add_dn(k.hc.lo, kx_dn(k.sc, xi));
    let g1 = sub_up(-k.hs.lo, kx_dn(k.cs, xi));
    let g2 = add_up(-k.hc.lo, kx_up(k.sc, xi));
    sub_dn(e.min(f1).min(f2), b.max(g1).max(g2))
}

/// A certified lower bound on `|R ∩ Q(c0)|` (lemma R2).
fn area_dn(fr: &Frame, rect: &Rect, x0: f64, y0: f64) -> f64 {
    let k = &fr.vertical;
    // The inner representable rectangle [x1.hi, x2.lo] x [y1.hi, y2.lo] lies in R.
    let xi1 = sub_up(rect.x1.hi, x0);
    let xi2 = sub_dn(rect.x2.lo, x0);
    let e = sub_dn(rect.y2.lo, y0);
    let b = sub_up(rect.y1.hi, y0);
    if !(xi1 < xi2 && b < e) {
        return 0.0;
    }
    let (c, s, h) = (fr.cf, fr.sf, fr.hf);
    // Approximate breakpoints of h(xi): its exact positions only affect accuracy.
    // Breakpoints of the concave h are where two of its affine pieces cross;
    // its zeros are added too, so that no trapezoid straddles a sign change by
    // more than rounding (a straddling trapezoid is valid but loses area).
    let mut nodes = [0.0f64; 14];
    nodes[0] = xi1;
    nodes[1] = xi2;
    let candidates = [
        // top and bottom vertices, where f1 = f2 and g1 = g2
        h * (c - s),
        -h * (c - s),
        // e = f1, e = f2, b = g1, b = g2
        (h - s * e) / c,
        (c * e - h) / s,
        -(h + s * b) / c,
        (c * b + h) / s,
        // zeros: right and left vertices (f1 = g2, f2 = g1), e = g1, e = g2,
        // f1 = b, f2 = b
        h * (c + s),
        -h * (c + s),
        -(h + s * e) / c,
        (c * e + h) / s,
        (h - s * b) / c,
        (c * b - h) / s,
    ];
    let mut count = 2;
    for t in candidates {
        if t > xi1 && t < xi2 {
            nodes[count] = t;
            count += 1;
        }
    }
    let nodes = &mut nodes[..count];
    nodes.sort_unstable_by(f64::total_cmp);
    let mut total = 0.0;
    let mut previous_x = nodes[0];
    let mut previous_v = section_dn(k, previous_x, e, b);
    for &x in &nodes[1..] {
        let v = section_dn(k, x, e, b);
        let sum = add_dn(previous_v, v);
        if sum > 0.0 {
            let width = sub_dn(x, previous_x);
            if width > 0.0 {
                total = add_dn(total, dn(mul_dn(sum, width) * 0.5));
            }
        }
        previous_x = x;
        previous_v = v;
    }
    total
}

/// Enclosure over the box of the length of a segment inside the square
/// (lemma R5). `w` encloses the line's offset from the centre, `e`/`b` the
/// segment ends' offsets, `len` its length.
#[inline]
fn segment_length(k: &LineCoeffs, w: Iv, e: Iv, b: Iv, len: Iv) -> Iv {
    let cw = w.mul_nonneg(k.cs);
    let sw = w.mul_nonneg(k.sc);
    let iw = w.mul_nonneg(k.isc);
    let t2 = e.add(k.hs).add(cw);
    let t3 = e.add(k.hc).sub(sw);
    let t4 = k.hs.sub(cw).sub(b);
    let t5 = k.hc.add(sw).sub(b);
    let t8 = k.hsum.sub(iw);
    let t9 = k.hsum.add(iw);
    len.min(t2)
        .min(t3)
        .min(t4)
        .min(t5)
        .min(k.two_hs)
        .min(k.two_hc)
        .min(t8)
        .min(t9)
        .pos()
}

/// Offset enclosure `a - (centre +- half)` for a coordinate enclosure `a`.
#[inline]
fn offset(a: Iv, centre: f64, half: f64) -> Iv {
    Iv::new(sub_dn(sub_dn(a.lo, centre), half), add_up(sub_up(a.hi, centre), half))
}

/// The geometry of one box of centres, shared by every rectangle test.
#[derive(Clone, Copy, Debug)]
struct BoxGeom {
    x0: f64,
    y0: f64,
    dx: f64,
    dy: f64,
    /// Box half-extent along the square's first axis, `c dx + s dy`.
    bu: f64,
    /// Box half-extent along the square's second axis, `s dx + c dy`.
    bv: f64,
    /// Half the square's axis-aligned extent, `h (c + s)`.
    ext: f64,
}

/// Gradient enclosure of one rectangle's overlap area over the box.
#[inline]
fn gradient(fr: &Frame, g: &BoxGeom, rect: &Rect) -> (Iv, Iv) {
    let ylen = rect.y2.sub(rect.y1);
    let xlen = rect.x2.sub(rect.x1);
    let ye = offset(rect.y2, g.y0, g.dy);
    let yb = offset(rect.y1, g.y0, g.dy);
    let xe = offset(rect.x2, g.x0, g.dx);
    let xb = offset(rect.x1, g.x0, g.dx);
    let v = &fr.vertical;
    let hz = &fr.horizontal;
    let left = segment_length(v, xb, ye, yb, ylen);
    let right = segment_length(v, xe, ye, yb, ylen);
    let bottom = segment_length(hz, yb, xe, xb, xlen);
    let top = segment_length(hz, ye, xe, xb, xlen);
    (
        left.sub(right).mul_nonneg(rect.rho),
        bottom.sub(top).mul_nonneg(rect.rho),
    )
}

#[derive(Clone, Copy, Debug)]
enum Class {
    Inside,
    Outside,
    Boundary,
}

/// Classify an axis-aligned rectangle with centre `(mx, my)` and half-sizes
/// `(wx, wy)` against every square centred in the box (lemma R1). The
/// comparisons carry the slack `TAU`, which exceeds their rounding error.
#[inline]
fn classify_extent(fr: &Frame, g: &BoxGeom, mx: f64, my: f64, wx: f64, wy: f64) -> Class {
    let (c, s, h) = (fr.cf, fr.sf, fr.hf);
    let ddx = mx - g.x0;
    let ddy = my - g.y0;
    let du = (c * ddx + s * ddy).abs();
    let dv = (c * ddy - s * ddx).abs();
    let eu = c * wx + s * wy;
    let ev = s * wx + c * wy;
    if du + eu + g.bu + TAU <= h && dv + ev + g.bv + TAU <= h {
        return Class::Inside;
    }
    if du >= eu + h + g.bu + TAU
        || dv >= ev + h + g.bv + TAU
        || ddx.abs() >= wx + g.dx + g.ext + TAU
        || ddy.abs() >= wy + g.dy + g.ext + TAU
    {
        return Class::Outside;
    }
    Class::Boundary
}

/// Classify a rectangle against every square centred in the box.
#[inline]
fn classify(fr: &Frame, g: &BoxGeom, rect: &Rect) -> Class {
    classify_extent(fr, g, rect.mx, rect.my, rect.wx, rect.wy)
}

#[derive(Clone, Copy, Debug)]
struct Node {
    xl: f64,
    xh: f64,
    yl: f64,
    yh: f64,
    depth: u32,
    parent_start: usize,
    parent_end: usize,
    inner: f64,
}

/// Verify one rotated net direction `index >= 1`.
///
/// # Errors
///
/// Returns a message if a constant cannot be enclosed.
pub fn verify_direction(
    cert: &Certificate,
    index: u32,
    threshold_hi: f64,
    limits: Limits,
) -> Result<DirectionResult, String> {
    let start = Instant::now();
    let fr = frame(cert, index)?;
    let (c, s) = direction(&cert.step, index);
    let two = BigRational::from_integer(BigInt::from(2));
    let extent = &cert.core * (&c + &s) / &two;
    let lower = enclose(&(&cert.side / &two))?.lo;
    let upper = enclose(&(&cert.side - &extent))?.hi;
    // Half the axis-aligned extent of the square, an upper bound with slack.
    let ext = approx(&extent)?;

    let rects = &cert.rects;
    let mut arena: Vec<u32> = (0..u32::try_from(rects.len()).map_err(|_| "too many rectangles")?).collect();
    let mut stack = vec![Node {
        xl: lower,
        xh: upper,
        yl: lower,
        yh: upper,
        depth: 0,
        parent_start: 0,
        parent_end: rects.len(),
        inner: 0.0,
    }];
    let mut nodes = 0u64;
    let mut leaves = 0u64;
    let mut max_depth = 0u32;
    let mut min_lower = f64::INFINITY;
    let mut argmin = None;
    let mut boundary_total = 0u64;
    let mut verdict = Verdict::Verified;
    let mut witness = None;
    while let Some(node) = stack.pop() {
        arena.truncate(node.parent_end);
        nodes += 1;
        max_depth = max_depth.max(node.depth);
        let x0 = 0.5 * (node.xl + node.xh);
        let y0 = 0.5 * (node.yl + node.yh);
        let dx = up((node.xh - x0).max(x0 - node.xl));
        let dy = up((node.yh - y0).max(y0 - node.yl));
        let g = BoxGeom {
            x0,
            y0,
            dx,
            dy,
            bu: fr.cf * dx + fr.sf * dy,
            bv: fr.sf * dx + fr.cf * dy,
            ext,
        };
        let mut inner = node.inner;
        let own_start = arena.len();
        for position in node.parent_start..node.parent_end {
            let id = arena[position];
            let rect = &rects[id as usize];
            match classify(&fr, &g, rect) {
                Class::Inside => inner = add_dn(inner, rect.mass.lo),
                Class::Outside => {}
                Class::Boundary => arena.push(id),
            }
        }
        let own_end = arena.len();
        boundary_total += (own_end - own_start) as u64;
        let mut value = inner;
        let mut gx = Iv::point(0.0);
        let mut gy = Iv::point(0.0);
        for position in own_start..own_end {
            let rect = &rects[arena[position] as usize];
            value = add_dn(value, mul_dn(rect.rho.lo, area_dn(&fr, rect, x0, y0)));
            let (rx, ry) = gradient(&fr, &g, rect);
            gx = gx.add(rx);
            gy = gy.add(ry);
        }
        #[cfg(debug_assertions)]
        {
            let full = centre_lower_bound(cert, index, x0, y0)?;
            assert!(
                (full - value).abs() < 1e-9,
                "incremental value {value} differs from full {full} at depth {} box {:?}",
                node.depth,
                (node.xl, node.xh, node.yl, node.yh)
            );
        }
        let px = mul_up(gx.mag(), dx);
        let py = mul_up(gy.mag(), dy);
        let bound = sub_dn(value, add_up(px, py));
        if bound >= threshold_hi {
            leaves += 1;
            if bound < min_lower {
                min_lower = bound;
                argmin = Some((x0, y0, dx, dy));
            }
            continue;
        }
        if value < threshold_hi - 1e-7 {
            verdict = Verdict::CounterexampleCandidate;
            witness = Some((x0, y0, value));
            break;
        }
        if node.depth >= limits.max_depth || nodes >= limits.max_nodes {
            verdict = Verdict::Unresolved;
            witness = Some((x0, y0, value));
            break;
        }
        let split_x = if px == py { dx >= dy } else { px > py };
        let child = |xl, xh, yl, yh| Node {
            xl,
            xh,
            yl,
            yh,
            depth: node.depth + 1,
            parent_start: own_start,
            parent_end: own_end,
            inner,
        };
        if split_x {
            if !(x0 > node.xl && x0 < node.xh) {
                verdict = Verdict::Unresolved;
                witness = Some((x0, y0, value));
                break;
            }
            stack.push(child(x0, node.xh, node.yl, node.yh));
            stack.push(child(node.xl, x0, node.yl, node.yh));
        } else {
            if !(y0 > node.yl && y0 < node.yh) {
                verdict = Verdict::Unresolved;
                witness = Some((x0, y0, value));
                break;
            }
            stack.push(child(node.xl, node.xh, y0, node.yh));
            stack.push(child(node.xl, node.xh, node.yl, y0));
        }
    }
    Ok(DirectionResult {
        index,
        verdict,
        nodes,
        leaves,
        max_depth,
        min_lower: if verdict == Verdict::Verified { min_lower } else { f64::NAN },
        argmin,
        witness,
        seconds: start.elapsed().as_secs_f64(),
        mean_boundary: boundary_total as f64 / nodes.max(1) as f64,
    })
}

/// A certified lower bound on the mass captured at one centre, summed over
/// every rectangle without classification: the differential-test probe.
///
/// # Errors
///
/// Returns a message if a constant cannot be enclosed.
pub fn centre_lower_bound(cert: &Certificate, index: u32, x0: f64, y0: f64) -> Result<f64, String> {
    let fr = frame(cert, index)?;
    let mut value = 0.0;
    for rect in &cert.rects {
        value = add_dn(value, mul_dn(rect.rho.lo, area_dn(&fr, rect, x0, y0)));
    }
    Ok(value)
}

/// A certified lower bound over a whole box of centres, from the root's full
/// rectangle list: the differential-test probe for boxes.
///
/// # Errors
///
/// Returns a message if a constant cannot be enclosed.
pub fn box_lower_bound(cert: &Certificate, index: u32, x0: f64, y0: f64, dx: f64, dy: f64) -> Result<f64, String> {
    let fr = frame(cert, index)?;
    let (c, s) = direction(&cert.step, index);
    let two = BigRational::from_integer(BigInt::from(2));
    let ext = approx(&(&cert.core * (&c + &s) / &two))?;
    let g = BoxGeom {
        x0,
        y0,
        dx,
        dy,
        bu: fr.cf * dx + fr.sf * dy,
        bv: fr.sf * dx + fr.cf * dy,
        ext,
    };
    let mut value = 0.0;
    let mut gx = Iv::point(0.0);
    let mut gy = Iv::point(0.0);
    for rect in &cert.rects {
        match classify(&fr, &g, rect) {
            Class::Inside => value = add_dn(value, rect.mass.lo),
            Class::Outside => {}
            Class::Boundary => {
                value = add_dn(value, mul_dn(rect.rho.lo, area_dn(&fr, rect, x0, y0)));
                let (rx, ry) = gradient(&fr, &g, rect);
                gx = gx.add(rx);
                gy = gy.add(ry);
            }
        }
    }
    Ok(sub_dn(value, add_up(mul_up(gx.mag(), dx), mul_up(gy.mag(), dy))))
}

#[cfg(test)]
#[path = "rotated_tests.rs"]
mod tests;
