//! Outward-rounded binary64 arithmetic.
//!
//! Every operation is evaluated in the hardware's round-to-nearest mode and the
//! result is then moved one representable value outward with `next_down` or
//! `next_up`. Lemma I1 of `SOUNDNESS.md` proves that `next_down(fl(x)) <= x <=
//! next_up(fl(x))` for every real `x` whose rounding `fl(x)` is finite, so each
//! helper here returns a valid bound on the exact real result of its operands.
//! Rust performs no implicit fused multiply-add and x86-64 uses SSE2, so every
//! operation is a single correctly rounded IEEE 754 operation.

/// A lower bound on the exact real result `x` from its rounded value.
#[inline]
#[must_use]
pub fn dn(x: f64) -> f64 {
    x.next_down()
}

/// An upper bound on the exact real result `x` from its rounded value.
#[inline]
#[must_use]
pub fn up(x: f64) -> f64 {
    x.next_up()
}

/// A lower bound on `a + b`.
#[inline]
#[must_use]
pub fn add_dn(a: f64, b: f64) -> f64 {
    dn(a + b)
}

/// An upper bound on `a + b`.
#[inline]
#[must_use]
pub fn add_up(a: f64, b: f64) -> f64 {
    up(a + b)
}

/// A lower bound on `a - b`.
#[inline]
#[must_use]
pub fn sub_dn(a: f64, b: f64) -> f64 {
    dn(a - b)
}

/// An upper bound on `a - b`.
#[inline]
#[must_use]
pub fn sub_up(a: f64, b: f64) -> f64 {
    up(a - b)
}

/// A lower bound on `a * b`.
#[inline]
#[must_use]
pub fn mul_dn(a: f64, b: f64) -> f64 {
    dn(a * b)
}

/// An upper bound on `a * b`.
#[inline]
#[must_use]
pub fn mul_up(a: f64, b: f64) -> f64 {
    up(a * b)
}

/// A closed interval `[lo, hi]` of reals, with `lo <= hi` for any interval built
/// by this module from valid operands.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Iv {
    /// Lower endpoint.
    pub lo: f64,
    /// Upper endpoint.
    pub hi: f64,
}

impl Iv {
    /// The degenerate interval holding one representable value exactly.
    #[inline]
    #[must_use]
    pub const fn point(x: f64) -> Self {
        Self { lo: x, hi: x }
    }

    /// An interval from two endpoints.
    #[inline]
    #[must_use]
    pub const fn new(lo: f64, hi: f64) -> Self {
        Self { lo, hi }
    }

    /// The enclosure of a sum.
    #[inline]
    #[must_use]
    pub fn add(self, other: Self) -> Self {
        Self::new(add_dn(self.lo, other.lo), add_up(self.hi, other.hi))
    }

    /// The enclosure of a difference.
    #[inline]
    #[must_use]
    pub fn sub(self, other: Self) -> Self {
        Self::new(sub_dn(self.lo, other.hi), sub_up(self.hi, other.lo))
    }

    /// The enclosure of a product, by the four endpoint products.
    #[inline]
    #[must_use]
    pub fn mul(self, other: Self) -> Self {
        let a = self.lo * other.lo;
        let b = self.lo * other.hi;
        let c = self.hi * other.lo;
        let d = self.hi * other.hi;
        Self::new(dn(a.min(b).min(c.min(d))), up(a.max(b).max(c.max(d))))
    }

    /// The enclosure of the product with a nonnegative interval `k`.
    ///
    /// For `k >= 0` the product is monotone in each factor's sign, which saves
    /// two of the four products.
    #[inline]
    #[must_use]
    pub fn mul_nonneg(self, k: Self) -> Self {
        let lo = if self.lo >= 0.0 {
            self.lo * k.lo
        } else {
            self.lo * k.hi
        };
        let hi = if self.hi >= 0.0 {
            self.hi * k.hi
        } else {
            self.hi * k.lo
        };
        Self::new(dn(lo), up(hi))
    }

    /// The pointwise minimum of two enclosed quantities.
    #[inline]
    #[must_use]
    pub fn min(self, other: Self) -> Self {
        Self::new(self.lo.min(other.lo), self.hi.min(other.hi))
    }

    /// The pointwise maximum of two enclosed quantities.
    #[inline]
    #[must_use]
    pub fn max(self, other: Self) -> Self {
        Self::new(self.lo.max(other.lo), self.hi.max(other.hi))
    }

    /// The enclosure of the positive part `max(x, 0)`.
    #[inline]
    #[must_use]
    pub fn pos(self) -> Self {
        Self::new(self.lo.max(0.0), self.hi.max(0.0))
    }

    /// The largest absolute value in the interval.
    #[inline]
    #[must_use]
    pub fn mag(self) -> f64 {
        self.lo.abs().max(self.hi.abs())
    }

    /// Whether both endpoints are finite and ordered.
    #[inline]
    #[must_use]
    pub fn is_valid(self) -> bool {
        self.lo.is_finite() && self.hi.is_finite() && self.lo <= self.hi
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn directed_steps_bracket_exact_sums() {
        // 0.1 + 0.2 is not representable; the bracket must contain it.
        let lo = add_dn(0.1, 0.2);
        let hi = add_up(0.1, 0.2);
        assert!(lo < hi);
        assert!(lo <= 0.300_000_000_000_000_04);
        assert!(hi >= 0.300_000_000_000_000_04);
    }

    #[test]
    fn interval_product_covers_sign_changes() {
        let a = Iv::new(-2.0, 3.0);
        let b = Iv::new(-5.0, 7.0);
        let p = a.mul(b);
        assert!(p.lo <= -15.0 && p.hi >= 21.0);
        let q = a.mul_nonneg(Iv::new(2.0, 4.0));
        assert!(q.lo <= -8.0 && q.hi >= 12.0);
    }
}
