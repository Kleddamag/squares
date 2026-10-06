//! Native arithmetic and LP kernel for the retained n=17 branch-and-bound pilot.

mod lp;
mod tinylp;
use pyo3::exceptions::{PyIndexError, PyValueError, PyZeroDivisionError};
use pyo3::prelude::*;
use std::collections::HashMap;
type Iv = (f64, f64);
type Box4 = (f64, f64, f64, f64);
type Plane = (f64, f64, f64);
type Term = (String, Vec<Iv>, Vec<Plane>, Vec<Plane>, Vec<Plane>);
// Comparisons deliberately preserve the first operand on ties (including signed zero)
// and unordered comparisons, like Python min/max. Rust f64::min/max do not.
fn min(a: f64, b: f64) -> f64 {
    if b < a { b } else { a }
}
fn max(a: f64, b: f64) -> f64 {
    if b > a { b } else { a }
}
fn dn(x: f64) -> f64 {
    x.next_down()
}
fn up(x: f64) -> f64 {
    x.next_up()
}
fn iadd(a: Iv, b: Iv) -> Iv {
    (dn(a.0 + b.0), up(a.1 + b.1))
}
fn isub(a: Iv, b: Iv) -> Iv {
    (dn(a.0 - b.1), up(a.1 - b.0))
}
fn imul(a: Iv, b: Iv) -> Iv {
    let p = [a.0 * b.0, a.0 * b.1, a.1 * b.0, a.1 * b.1];
    (
        dn(p[1..].iter().fold(p[0], |v, &x| min(v, x))),
        up(p[1..].iter().fold(p[0], |v, &x| max(v, x))),
    )
}
fn ineg(a: Iv) -> Iv {
    (-a.1, -a.0)
}
fn magnitude(a: Iv) -> f64 {
    max(-a.0, a.1)
}
fn least_abs(a: Iv) -> f64 {
    if a.0 >= 0.0 {
        a.0
    } else if a.1 <= 0.0 {
        -a.1
    } else {
        0.0
    }
}
fn up_mul(a: f64, b: f64) -> f64 {
    up(a * b)
}
fn up_add(a: f64, b: f64) -> f64 {
    up(a + b)
}
fn h_from(c: Iv, s: Iv) -> f64 {
    dn((least_abs(c) + least_abs(s)) / 2.0)
}
fn quantised(lo: f64, hi: f64) -> f64 {
    let middle = 0.5 * (lo + hi);
    let quantum = 2.0_f64.powi(-24);
    // Python round returns an integer, so a rounded zero is positive.
    let r = (middle / quantum).round_ties_even();
    let snapped = if r == 0.0 { 0.0 } else { r * quantum };
    if lo <= snapped && snapped <= hi {
        snapped
    } else {
        middle
    }
}
fn difference_box(a: Box4, b: Box4) -> (Iv, Iv) {
    (
        (dn(b.0 - a.1), up(b.1 - a.0)),
        (dn(b.2 - a.3), up(b.3 - a.2)),
    )
}
fn squared_range(dx: Iv, dy: Iv) -> Iv {
    let (nx, ny, fx, fy) = (least_abs(dx), least_abs(dy), magnitude(dx), magnitude(dy));
    (dn(dn(nx * nx) + dn(ny * ny)), up(up(fx * fx) + up(fy * fy)))
}
fn merge(mut pieces: Vec<Iv>, gap: f64) -> Vec<Iv> {
    pieces.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    let mut out: Vec<Iv> = vec![];
    for (lo, hi) in pieces {
        if let Some(last) = out.last_mut() {
            let allowance = gap * max(last.1 - last.0, hi - lo);
            if lo <= last.1 + allowance {
                last.1 = max(last.1, hi);
                continue;
            }
        }
        out.push((lo, hi));
    }
    out
}
#[pyclass]
/// Cached interval-trigonometry kernel for pair constraints.
struct Core {
    callback: Py<PyAny>,
    multiples: HashMap<i32, Iv>,
    merge_gap: f64,
    trig: HashMap<u64, (Iv, Iv)>,
}
impl Core {
    fn trig(&mut self, py: Python<'_>, theta: f64) -> PyResult<(Iv, Iv)> {
        if let Some(v) = self.trig.get(&theta.to_bits()) {
            return Ok(*v);
        }
        let v = self.callback.call1(py, (theta,))?.extract(py)?;
        self.trig.insert(theta.to_bits(), v);
        Ok(v)
    }
    fn contains(&self, lo: f64, hi: f64) -> bool {
        up(hi - lo) >= self.multiples[&1].0
            || self.multiples.values().any(|p| lo <= p.1 && hi >= p.0)
    }
    fn trig_difference(&mut self, py: Python<'_>, p: f64, q: f64) -> PyResult<(Iv, Iv)> {
        let (cp, sp) = self.trig(py, p)?;
        let (cq, sq) = self.trig(py, q)?;
        Ok((
            iadd(imul(cp, cq), imul(sp, sq)),
            isub(imul(sp, cq), imul(cp, sq)),
        ))
    }
    fn gap_lower(&mut self, py: Python<'_>, ti: Iv, tj: Iv) -> PyResult<f64> {
        if (tj.0 <= ti.1 && ti.0 <= tj.1) || self.contains(dn(tj.0 - ti.1), up(tj.1 - ti.0)) {
            return Ok(1.0);
        }
        let (c, s) = self.trig_difference(py, tj.0, ti.1)?;
        let low = h_from(c, s);
        let (c, s) = self.trig_difference(py, tj.1, ti.0)?;
        Ok(max(1.0, dn(0.5 + min(low, h_from(c, s)))))
    }
    fn pieces(&self, ti: Iv, tj: Iv, window: Option<Iv>) -> Vec<Iv> {
        let mut out = vec![];
        for theta in [ti, tj] {
            for k in 0..4 {
                let shift = self.multiples[&k];
                let piece = (dn(theta.0 + shift.0), up(theta.1 + shift.1));
                if let Some(w) = window {
                    for turns in [-1, 0, 1] {
                        let shifted = if turns == 0 {
                            piece
                        } else {
                            let s = if turns > 0 {
                                self.multiples[&4]
                            } else {
                                ineg(self.multiples[&4])
                            };
                            (dn(piece.0 + s.0), up(piece.1 + s.1))
                        };
                        let lo = max(shifted.0, w.0);
                        let hi = min(shifted.1, w.1);
                        if lo <= hi {
                            out.push((lo, hi));
                        }
                    }
                } else {
                    out.push(piece);
                }
            }
        }
        out
    }
    fn option_planes(
        &mut self,
        py: Python<'_>,
        lo: f64,
        hi: f64,
        dx: Iv,
        dy: Iv,
        d_max: f64,
        g: f64,
    ) -> PyResult<Vec<Plane>> {
        let m = quantised(lo, hi);
        let mut found = vec![];
        if up(hi - lo) < self.multiples[&1].0 {
            let x = up(max(up(m - lo), up(hi - m)));
            let chord = dn(g * dn(1.0 - up(x * x) / 2.0));
            for (angle, rhs) in [(lo, g), (hi, g), (m, chord)] {
                let (c, s) = self.trig(py, angle)?;
                if iadd(imul(c, dx), imul(s, dy)).1 >= rhs {
                    let eps = max(up(c.1 - c.0), up(s.1 - s.0));
                    let slack = up_mul(eps, up_add(magnitude(dx), magnitude(dy)));
                    found.push((0.5 * (c.0 + c.1), 0.5 * (s.0 + s.1), dn(rhs - slack)));
                }
            }
        } else {
            let (c, s) = self.trig(py, m)?;
            let eps = max(up(c.1 - c.0), up(s.1 - s.0));
            let tau = up(max(up(m - lo), up(hi - m)) / 2.0);
            let perp = magnitude(iadd(imul(ineg(s), dx), imul(c, dy)));
            let loss = up_mul(2.0 * tau, up_add(perp, up_mul(tau, d_max)));
            let loss = up_add(loss, up_mul(eps, up_add(magnitude(dx), magnitude(dy))));
            found.push((0.5 * (c.0 + c.1), 0.5 * (s.0 + s.1), dn(g - loss)));
        }
        found.retain(|&(nx, ny, bound)| iadd(imul((nx, nx), dx), imul((ny, ny), dy)).1 >= bound);
        Ok(found)
    }
}
#[pymethods]
impl Core {
    #[new]
    /// Create a pair kernel from the pilot's interval trigonometry callback.
    fn new(
        cos_sin: Py<PyAny>,
        half_pi_multiples: HashMap<i32, Iv>,
        merge_gap: f64,
    ) -> PyResult<Self> {
        if merge_gap != 0.0 {
            return Err(PyValueError::new_err(
                "the native kernel requires merge_gap=0",
            ));
        }
        for k in [0, 1, 2, 3, 4] {
            if !half_pi_multiples.contains_key(&k) {
                return Err(PyValueError::new_err(format!(
                    "missing half-pi multiple {k}"
                )));
            }
        }
        Ok(Self {
            callback: cos_sin,
            multiples: half_pi_multiples,
            merge_gap,
            trig: HashMap::new(),
        })
    }
    #[pyo3(signature=(ti,tj,window,box_i,box_j))]
    /// Evaluate one pair term with the pilot's exact tuple return shape.
    fn pair_term(
        &mut self,
        py: Python<'_>,
        ti: Iv,
        tj: Iv,
        window: Option<Iv>,
        box_i: Box4,
        box_j: Box4,
    ) -> PyResult<Term> {
        let (dx, dy) = difference_box(box_i, box_j);
        let squared = squared_range(dx, dy);
        if squared.0 >= 2.0 {
            return Ok(("separated".into(), vec![], vec![], vec![], vec![]));
        }
        if squared.1 < 1.0 {
            return Ok(("disc".into(), vec![], vec![], vec![], vec![]));
        }
        let g = self.gap_lower(py, ti, tj)?;
        let d_max = up(squared.1.sqrt());
        let pieces = self.pieces(ti, tj, window);
        let mut planes = vec![];
        let mut alive = vec![];
        for &(lo, hi) in &pieces {
            let found = self.option_planes(py, lo, hi, dx, dy, d_max, g)?;
            if !found.is_empty() {
                alive.push((lo, hi));
                planes.extend(found);
            }
        }
        let recorded = pieces
            .iter()
            .map(|&(lo, hi)| (lo, hi, quantised(lo, hi)))
            .collect();
        if alive.is_empty() {
            return Ok(("pair".into(), vec![], vec![], vec![], recorded));
        }
        let options = merge(alive, self.merge_gap);
        let cuts = hull_cuts(&planes, dx, dy);
        Ok((
            if options.len() > 1 {
                "undecided"
            } else {
                "decided"
            }
            .into(),
            options,
            cuts,
            planes,
            recorded,
        ))
    }
}
fn clip_box(dx: Iv, dy: Iv, (nx, ny, r): Plane) -> Vec<Iv> {
    let corners = [(dx.0, dy.0), (dx.1, dy.0), (dx.1, dy.1), (dx.0, dy.1)];
    let mut result = vec![];
    for i in 0..4 {
        let start = corners[i];
        let end = corners[(i + 1) % 4];
        let fs = nx * start.0 + ny * start.1 - r;
        let fe = nx * end.0 + ny * end.1 - r;
        if fs >= 0.0 {
            result.push(start);
        }
        if fs * fe < 0.0 {
            let t = fs / (fs - fe);
            result.push((
                start.0 + t * (end.0 - start.0),
                start.1 + t * (end.1 - start.1),
            ));
        }
    }
    result
}
fn turn(o: Iv, a: Iv, b: Iv) -> f64 {
    (a.0 - o.0) * (b.1 - o.1) - (a.1 - o.1) * (b.0 - o.0)
}
fn float_hull(points: Vec<Iv>) -> Vec<Iv> {
    // Deduplicate before sorting to retain the first signed-zero representation.
    let mut ordered = vec![];
    let mut seen = std::collections::HashSet::new();
    for p in points {
        let key = (
            if p.0 == 0.0 { 0 } else { p.0.to_bits() },
            if p.1 == 0.0 { 0 } else { p.1.to_bits() },
        );
        if seen.insert(key) {
            ordered.push(p);
        }
    }
    ordered.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    if ordered.len() < 3 {
        return ordered;
    }
    let mut lower: Vec<Iv> = vec![];
    let mut upper: Vec<Iv> = vec![];
    for &p in &ordered {
        while lower.len() >= 2 && turn(lower[lower.len() - 2], lower[lower.len() - 1], p) <= 0.0 {
            lower.pop();
        }
        lower.push(p);
    }
    for &p in ordered.iter().rev() {
        while upper.len() >= 2 && turn(upper[upper.len() - 2], upper[upper.len() - 1], p) <= 0.0 {
            upper.pop();
        }
        upper.push(p);
    }
    lower.pop();
    upper.pop();
    lower.extend(upper);
    lower
}
fn plane_min(u: Iv, (nx, ny, r): Plane, dx: Iv, dy: Iv) -> f64 {
    let mut candidates = vec![0.0];
    if nx != 0.0 {
        candidates.push(u.0 / nx);
    }
    if ny != 0.0 {
        candidates.push(u.1 / ny);
    }
    let mut best = f64::NEG_INFINITY;
    for lam in candidates {
        if !(lam >= 0.0) || lam.is_infinite() {
            continue;
        }
        let scaled = (lam, lam);
        let cx = isub((u.0, u.0), imul(scaled, (nx, nx)));
        let cy = isub((u.1, u.1), imul(scaled, (ny, ny)));
        let value = iadd(iadd(imul(cx, dx), imul(cy, dy)), imul(scaled, (r, r))).0;
        best = max(best, value);
    }
    best
}
// Compensated norm following CPython 3.14 mathmodule.c vector_norm.
// Error-free product uses Dekker splitting, without FMA or contraction.
fn product(x: f64, y: f64) -> Iv {
    let tx = x * 134_217_729.0;
    let xh = tx - (tx - x);
    let xl = x - xh;
    let ty = y * 134_217_729.0;
    let yh = ty - (ty - y);
    let yl = y - yh;
    let z = x * y;
    let error = ((xh * yh - z) + xh * yl + xl * yh) + xl * yl;
    (z, error)
}
fn fast_sum(a: f64, b: f64) -> Iv {
    let x = a + b;
    (x, (a - x) + b)
}
fn hypot(x: f64, y: f64) -> f64 {
    let x = x.abs();
    let y = y.abs();
    let m = max(x, y);
    if x.is_infinite() || y.is_infinite() {
        return f64::INFINITY;
    }
    if x.is_nan() || y.is_nan() {
        return f64::NAN;
    }
    if m == 0.0 {
        return m;
    }
    let exponent = ((m.to_bits() >> 52) & 2047) as i32 - 1022;
    if exponent < -1023 || m < f64::MIN_POSITIVE {
        return f64::MIN_POSITIVE * hypot(x / f64::MIN_POSITIVE, y / f64::MIN_POSITIVE);
    }
    let scale = if exponent == 1024 {
        f64::from_bits(1_u64 << 50)
    } else {
        2.0_f64.powi(-exponent)
    };
    let (mut sum, mut f1, mut f2) = (1.0, 0.0, 0.0);
    for v in [x, y] {
        let v = v * scale;
        let p = product(v, v);
        let s = fast_sum(sum, p.0);
        sum = s.0;
        f1 += p.1;
        f2 += s.1;
    }
    let mut h = (sum - 1.0 + (f1 + f2)).sqrt();
    let p = product(-h, h);
    let s = fast_sum(sum, p.0);
    sum = s.0;
    f1 += p.1;
    f2 += s.1;
    let residual = sum - 1.0 + (f1 + f2);
    h += residual / (2.0 * h);
    h / scale
}
fn hull_cuts(planes: &[Plane], dx: Iv, dy: Iv) -> Vec<Plane> {
    let points = planes.iter().flat_map(|&p| clip_box(dx, dy, p)).collect();
    let hull = float_hull(points);
    if hull.len() < 3 {
        return vec![];
    }
    let tolerance = 1e-9 * max(max(dx.1 - dx.0, dy.1 - dy.0), 1e-12);
    let mut cuts = vec![];
    for i in 0..hull.len() {
        let start = hull[i];
        let end = hull[(i + 1) % hull.len()];
        if [(start.0, end.0, dx), (start.1, end.1, dy)]
            .iter()
            .any(|&(s, e, b)| {
                [b.0, b.1]
                    .iter()
                    .any(|&v| (s - v).abs() <= tolerance && (e - v).abs() <= tolerance)
            })
        {
            continue;
        }
        let ex = end.0 - start.0;
        let ey = end.1 - start.1;
        let length = hypot(ex, ey);
        if length <= tolerance {
            continue;
        }
        let u = (-ey / length, ex / length);
        let mut values = planes.iter().map(|&p| plane_min(u, p, dx, dy));
        let Some(first) = values.next() else {
            return vec![];
        };
        let value = values.fold(first, min);
        let box_least = iadd(imul((u.0, u.0), dx), imul((u.1, u.1), dy)).0;
        if value > box_least + tolerance {
            cuts.push((u.0, u.1, value));
        }
    }
    cuts
}
#[pyfunction]
#[pyo3(signature=(columns,exact,exact_rhs,norms,multipliers,spans,cost))]
/// Enclose the dual objective using outward-rounded interval coefficients.
fn dual_bound(
    columns: Vec<Vec<usize>>,
    exact: Vec<Vec<Iv>>,
    exact_rhs: Vec<Iv>,
    norms: Vec<f64>,
    multipliers: Vec<f64>,
    spans: Vec<Iv>,
    cost: Option<(usize, f64)>,
) -> PyResult<f64> {
    dual_bound_impl(
        &columns,
        &exact,
        &exact_rhs,
        &norms,
        &multipliers,
        &spans,
        cost,
    )
}
fn dual_bound_impl(
    columns: &[Vec<usize>],
    exact: &[Vec<Iv>],
    exact_rhs: &[Iv],
    norms: &[f64],
    multipliers: &[f64],
    spans: &[Iv],
    cost: Option<(usize, f64)>,
) -> PyResult<f64> {
    let n = columns.len();
    if [exact.len(), exact_rhs.len(), norms.len(), multipliers.len()]
        .iter()
        .any(|&v| v != n)
    {
        return Err(PyValueError::new_err("row array lengths differ"));
    }
    let mut combined = vec![(0.0, 0.0); spans.len()];
    if let Some((c, s)) = cost {
        if c >= combined.len() {
            return Err(PyIndexError::new_err("cost column out of range"));
        }
        combined[c] = (s, s);
    }
    let mut right = (0.0, 0.0);
    for i in 0..n {
        let weight = multipliers[i];
        if weight <= 0.0 {
            continue;
        }
        if norms[i] == 0.0 {
            return Err(PyZeroDivisionError::new_err("float division by zero"));
        }
        let y = weight / norms[i];
        let scaled = (y, y);
        if columns[i].len() != exact[i].len() {
            return Err(PyValueError::new_err("column/coefficient lengths differ"));
        }
        for (&c, &coefficient) in columns[i].iter().zip(&exact[i]) {
            if c >= combined.len() {
                return Err(PyIndexError::new_err("column out of range"));
            }
            combined[c] = iadd(combined[c], imul(scaled, coefficient));
        }
        right = iadd(right, imul(scaled, exact_rhs[i]));
    }
    let mut least = 0.0;
    for (coefficient, span) in combined.into_iter().zip(spans.iter().copied()) {
        least = dn(least + imul(coefficient, span).0);
    }
    Ok(dn(least - right.1))
}
#[pymodule]
fn n17bb_native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Core>()?;
    m.add_class::<tinylp::TinyLP>()?;
    lp::register(m)?;
    m.add_function(wrap_pyfunction!(dual_bound, m)?)?;
    Ok(())
}
