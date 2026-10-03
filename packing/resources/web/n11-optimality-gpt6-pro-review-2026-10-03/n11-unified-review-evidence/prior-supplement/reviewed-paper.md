# A Review of the Optimality Proof of the Trump Packing of 11 Squares

- From the original proof by **Queuingtheorydotcom**
- [github.com/Queuingtheorydotcom/11SquaresOptimal](https://github.com/Queuingtheorydotcom/11SquaresOptimal)
- Human oversight: [**Joshua Levy**](https://x.com/ojoshe)
- Agents: **GPT-6 Astra** and **GPT-6 Sol**
- Draft v0.1.0
- Original proof September 29, 2026 · Last revised October 1, 2026

This paper explains the computer-assisted optimality proof published by
[Queuingtheorydotcom in **11SquaresOptimal**](https://github.com/Queuingtheorydotcom/11SquaresOptimal).
The original
[mathematical argument](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/PROOF.md),
[verification driver](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/VERIFY.py),
[certificate data](https://github.com/Queuingtheorydotcom/11SquaresOptimal/tree/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/data),
and
[reproduction instructions](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/docs/REPRODUCING.md)
are pinned to the source revision reviewed here.
[Queuingtheorydotcom’s announcement](https://x.com/MathCompSciFTW/status/2104772485816168618)
credits Astra’s work building on the Squares Project and Kleddamag.

The components have distinct provenance:

- **Attaining construction:** Walter Trump’s packing, with
  [David Ellsworth’s reconstruction and exact formulas](https://kingbird.myphotos.cc/packing/square-11.svg),
  retained in the
  [construction source record](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/papers/kingbird-square-11-provenance.svg).
- **Mathematical antecedents:** the Squares Project’s
  [threshold-certificate method](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md)
  and [local-isolation theorem](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/cases/trump11/isolation-theorem.md), together with
  [Kleddamag’s earlier lower-bound proof](https://github.com/Kleddamag/11-squares-certified-bound)
  that $s(11)>31/8$
  ([retained source](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/external-square-certificates-2026-09-22/kleddamag-11/README.md)).
  The original proof’s
  [third-party notices](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/THIRD_PARTY_NOTICES.md)
  identify its incorporated Squares Project revision.
- **Verification and exposition here:** the Squares Project’s
  [T-060 result record](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/frontier/RESULTS.md),
  [retained proof and verification packet](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/README.md),
  and
  [mathematical acceptance review](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance)
  document the confirmation explained in this paper.[^credit]

For a technical review, start with the
[T-060 validation guide](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/VALIDATION.md).
It links the published proof, certificate inputs, independent checks, and accepted
evidence for each obligation.
The guide distinguishes checking retained evidence from a fresh geometric replay and
states the remaining work needed for a standalone executable package.

## The Result

Place eleven unit squares inside a larger square.
Each small square may rotate independently.
Their edges may touch, but their interiors may not overlap.
How small can the container be?

The answer is the side length of Trump’s construction in Figure 1:

$$
s(11)=T=3.8770835900228141773078970601\ldots.
$$

This is an exact algebraic number.
Let $u$ be the unique real root in $(9/25,37/100)$ of

$$
5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1=0.
$$

Then

$$
T=\frac{6u+4}{1+2u-u^2}.
$$

**Theorem.** Eleven congruent unit squares with arbitrary independent rotations and
pairwise disjoint interiors fit in a square of side $T$, and do not fit in any square of
side $S<T$.[^proof]

<figure>
<div class="stage trump"><a href="https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/atlas/rendering/trump11-overview.svg" aria-label="The rendering in the repository"><svg xmlns="http://www.w3.org/2000/svg" xmlns:sqpack="https://github.com/jlevy/thinking-scratchpad/ns/sqpack/v1" viewBox="24 24 560 560" role="img" aria-labelledby="figure-title figure-description" data-static-fallback="final">
  <title id="figure-title">Trump construction of eleven unit squares</title>
  <desc id="figure-description">An SVG illustration rendered from the exact Trump construction. Pixel coordinates are rounded for display; exact algebraic checks establish the witness separately.</desc>
  <rect width="960" height="680" fill="#ffffff" />
  <g id="panel-0" data-panel="Trump n=11">
    <g id="panel-0-fills" data-layer="fills">
      <polygon data-feature="square-fill" data-square="square-00" data-hue-index="0" data-shade-index="2" data-orientation-radians="0.0" points="36,571.9999999999999999999999998 174.2482444741012096770558292,571.9999999999999999999999998 174.2482444741012096770558292,433.7517555258987903229441706 36,433.7517555258987903229441706" fill="#4b9582" fill-opacity="1.0" stroke="none" data-angle-class="0" data-angle-class-residual-radians="0E-59" data-contact-sides="2" data-full-side-contacts="wall-bottom wall-left" data-maximum-contact-residual="0" />
      <polygon data-feature="square-fill" data-square="square-01" data-hue-index="0" data-shade-index="2" data-orientation-radians="0.0" points="433.7517555258987903229441707,571.9999999999999999999999998 571.9999999999999999999999999,571.9999999999999999999999998 571.9999999999999999999999999,433.7517555258987903229441706 433.7517555258987903229441707,433.7517555258987903229441706" fill="#4b9582" fill-opacity="1.0" stroke="none" data-angle-class="0" data-angle-class-residual-radians="0E-59" data-contact-sides="2" data-full-side-contacts="wall-bottom wall-right" data-maximum-contact-residual="0" />
      <polygon data-feature="square-fill" data-square="square-02" data-hue-index="0" data-shade-index="3" data-orientation-radians="0.0" points="316.9976187500726019601504957,174.2482444741012096770558292 455.2458632241738116372063249,174.2482444741012096770558292 455.2458632241738116372063249,36 316.9976187500726019601504957,36" fill="#5fa995" fill-opacity="1.0" stroke="none" data-angle-class="0" data-angle-class-residual-radians="0E-59" data-contact-sides="1" data-full-side-contacts="wall-top" data-maximum-contact-residual="0E-31" />
      <polygon data-feature="square-fill" data-square="square-03" data-hue-index="0" data-shade-index="0" data-orientation-radians="0.0" points="36,174.2482444741012096770558292 174.2482444741012096770558292,174.2482444741012096770558292 174.2482444741012096770558292,36 36,36" fill="#257260" fill-opacity="1.0" stroke="none" data-angle-class="0" data-angle-class-residual-radians="0E-59" data-contact-sides="4" data-full-side-contacts="square-05 square-04 wall-top wall-left" data-maximum-contact-residual="0" />
      <polygon data-feature="square-fill" data-square="square-04" data-hue-index="0" data-shade-index="2" data-orientation-radians="0.0" points="174.2482444741012096770558292,174.2482444741012096770558292 312.4964889482024193541116584,174.2482444741012096770558292 312.4964889482024193541116584,36 174.2482444741012096770558292,36" fill="#4b9582" fill-opacity="1.0" stroke="none" data-angle-class="0" data-angle-class-residual-radians="0E-59" data-contact-sides="2" data-full-side-contacts="wall-top square-03" data-maximum-contact-residual="0E-31" />
      <polygon data-feature="square-fill" data-square="square-05" data-hue-index="0" data-shade-index="2" data-orientation-radians="0.0" points="36,312.4964889482024193541116584 174.2482444741012096770558292,312.4964889482024193541116584 174.2482444741012096770558292,174.2482444741012096770558292 36,174.2482444741012096770558292" fill="#4b9582" fill-opacity="1.0" stroke="none" data-angle-class="0" data-angle-class-residual-radians="0E-59" data-contact-sides="2" data-full-side-contacts="square-03 wall-left" data-maximum-contact-residual="0" />
      <polygon data-feature="square-fill" data-square="square-06" data-hue-index="2" data-shade-index="4" data-orientation-radians="0.7013071055461422228717066139552481194184871905170169886" points="203.6761241695345890955586471,468.5972249785157420538328984 309.2977101789161800297084415,379.3971259369022140919773722 220.0976111373026520678529153,273.7755399275206231578275779 114.4760251279210611337031209,362.975638969134151119683104" fill="#dd87b8" fill-opacity="1.0" stroke="none" data-angle-class="1" data-angle-class-residual-radians="0E-59" data-contact-sides="0" data-full-side-contacts="" />
      <polygon data-feature="square-fill" data-square="square-07" data-hue-index="2" data-shade-index="4" data-orientation-radians="0.7013071055461422228717066139552481194184871905170169886" points="295.5035110517975806458883415,571.9999999999999999999999998 401.1250970611791715800381359,482.7999009583864720381444737 311.9249980195656436181826097,377.1783149490048811039946792 206.3034120101840526840328153,466.3784139906184090658502055" fill="#dd87b8" fill-opacity="1.0" stroke="none" data-angle-class="1" data-angle-class-residual-radians="0E-59" data-contact-sides="0" data-full-side-contacts="" />
      <polygon data-feature="square-fill" data-square="square-08" data-hue-index="2" data-shade-index="4" data-orientation-radians="0.7013071055461422228717066139552481194184871905170169886" points="298.7022898210838199702915584,366.8511185371989955850784568 404.3238758304654109044413528,277.6510194955854676232229307 315.1237767888518829425858266,172.0294334862038766890731362 209.5021907794702920084360322,261.2295325278174046509286623" fill="#dd87b8" fill-opacity="1.0" stroke="none" data-angle-class="1" data-angle-class-residual-radians="0E-59" data-contact-sides="0" data-full-side-contacts="" />
      <polygon data-feature="square-fill" data-square="square-09" data-hue-index="2" data-shade-index="4" data-orientation-radians="0.7013071055461422228717066139552481194184871905170169886" points="390.5296767033468115206212528,470.2538935586832535312455582 496.1512627127284024547710472,381.053794517069725569390032 406.951163671114874492915521,275.4322085076881346352402377 301.3295776617332835587657266,364.6323075493016625970957638" fill="#dd87b8" fill-opacity="1.0" stroke="none" data-angle-class="1" data-angle-class-residual-radians="0E-59" data-contact-sides="0" data-full-side-contacts="" />
      <polygon data-feature="square-fill" data-square="square-10" data-hue-index="2" data-shade-index="4" data-orientation-radians="0.7013071055461422228717066139552481194184871905170169886" points="466.3784139906184090658502054,345.799848211700643238009829 571.9999999999999999999999999,256.5997491700871152761543029 482.7999009583864720381444737,150.9781631607055243420045084 377.1783149490048811039946793,240.1782622023190523038600346" fill="#dd87b8" fill-opacity="1.0" stroke="none" data-angle-class="1" data-angle-class-residual-radians="0E-59" data-contact-sides="0" data-full-side-contacts="" />
    </g>
    <defs data-contact-clip-policy="participating-square-union">
      <polygon id="panel-0-contact-clip-shape-square-00" data-feature="contact-clip-shape" data-square="square-00" points="36,571.9999999999999999999999998 174.2482444741012096770558292,571.9999999999999999999999998 174.2482444741012096770558292,433.7517555258987903229441706 36,433.7517555258987903229441706" />
      <polygon id="panel-0-contact-clip-shape-square-01" data-feature="contact-clip-shape" data-square="square-01" points="433.7517555258987903229441707,571.9999999999999999999999998 571.9999999999999999999999999,571.9999999999999999999999998 571.9999999999999999999999999,433.7517555258987903229441706 433.7517555258987903229441707,433.7517555258987903229441706" />
      <polygon id="panel-0-contact-clip-shape-square-02" data-feature="contact-clip-shape" data-square="square-02" points="316.9976187500726019601504957,174.2482444741012096770558292 455.2458632241738116372063249,174.2482444741012096770558292 455.2458632241738116372063249,36 316.9976187500726019601504957,36" />
      <polygon id="panel-0-contact-clip-shape-square-03" data-feature="contact-clip-shape" data-square="square-03" points="36,174.2482444741012096770558292 174.2482444741012096770558292,174.2482444741012096770558292 174.2482444741012096770558292,36 36,36" />
      <polygon id="panel-0-contact-clip-shape-square-04" data-feature="contact-clip-shape" data-square="square-04" points="174.2482444741012096770558292,174.2482444741012096770558292 312.4964889482024193541116584,174.2482444741012096770558292 312.4964889482024193541116584,36 174.2482444741012096770558292,36" />
      <polygon id="panel-0-contact-clip-shape-square-05" data-feature="contact-clip-shape" data-square="square-05" points="36,312.4964889482024193541116584 174.2482444741012096770558292,312.4964889482024193541116584 174.2482444741012096770558292,174.2482444741012096770558292 36,174.2482444741012096770558292" />
      <polygon id="panel-0-contact-clip-shape-square-06" data-feature="contact-clip-shape" data-square="square-06" points="203.6761241695345890955586471,468.5972249785157420538328984 309.2977101789161800297084415,379.3971259369022140919773722 220.0976111373026520678529153,273.7755399275206231578275779 114.4760251279210611337031209,362.975638969134151119683104" />
      <polygon id="panel-0-contact-clip-shape-square-07" data-feature="contact-clip-shape" data-square="square-07" points="295.5035110517975806458883415,571.9999999999999999999999998 401.1250970611791715800381359,482.7999009583864720381444737 311.9249980195656436181826097,377.1783149490048811039946792 206.3034120101840526840328153,466.3784139906184090658502055" />
      <polygon id="panel-0-contact-clip-shape-square-08" data-feature="contact-clip-shape" data-square="square-08" points="298.7022898210838199702915584,366.8511185371989955850784568 404.3238758304654109044413528,277.6510194955854676232229307 315.1237767888518829425858266,172.0294334862038766890731362 209.5021907794702920084360322,261.2295325278174046509286623" />
      <polygon id="panel-0-contact-clip-shape-square-09" data-feature="contact-clip-shape" data-square="square-09" points="390.5296767033468115206212528,470.2538935586832535312455582 496.1512627127284024547710472,381.053794517069725569390032 406.951163671114874492915521,275.4322085076881346352402377 301.3295776617332835587657266,364.6323075493016625970957638" />
      <polygon id="panel-0-contact-clip-shape-square-10" data-feature="contact-clip-shape" data-square="square-10" points="466.3784139906184090658502054,345.799848211700643238009829 571.9999999999999999999999999,256.5997491700871152761543029 482.7999009583864720381444737,150.9781631607055243420045084 377.1783149490048811039946793,240.1782622023190523038600346" />
      <clipPath id="panel-0-clip-contact-pair-square-00-square-06" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-00 square-06">
        <use href="#panel-0-contact-clip-shape-square-00" data-clip-square="square-00" />
        <use href="#panel-0-contact-clip-shape-square-06" data-clip-square="square-06" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-pair-square-01-square-09" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-01 square-09">
        <use href="#panel-0-contact-clip-shape-square-01" data-clip-square="square-01" />
        <use href="#panel-0-contact-clip-shape-square-09" data-clip-square="square-09" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-pair-square-02-square-08" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-02 square-08">
        <use href="#panel-0-contact-clip-shape-square-02" data-clip-square="square-02" />
        <use href="#panel-0-contact-clip-shape-square-08" data-clip-square="square-08" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-pair-square-02-square-10" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-02 square-10">
        <use href="#panel-0-contact-clip-shape-square-02" data-clip-square="square-02" />
        <use href="#panel-0-contact-clip-shape-square-10" data-clip-square="square-10" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-pair-square-03-square-04" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-03 square-04">
        <use href="#panel-0-contact-clip-shape-square-03" data-clip-square="square-03" />
        <use href="#panel-0-contact-clip-shape-square-04" data-clip-square="square-04" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-pair-square-03-square-05" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-03 square-05">
        <use href="#panel-0-contact-clip-shape-square-03" data-clip-square="square-03" />
        <use href="#panel-0-contact-clip-shape-square-05" data-clip-square="square-05" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-pair-square-04-square-05" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-04 square-05">
        <use href="#panel-0-contact-clip-shape-square-04" data-clip-square="square-04" />
        <use href="#panel-0-contact-clip-shape-square-05" data-clip-square="square-05" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-pair-square-04-square-08" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-04 square-08">
        <use href="#panel-0-contact-clip-shape-square-04" data-clip-square="square-04" />
        <use href="#panel-0-contact-clip-shape-square-08" data-clip-square="square-08" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-pair-square-05-square-06" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-05 square-06">
        <use href="#panel-0-contact-clip-shape-square-05" data-clip-square="square-05" />
        <use href="#panel-0-contact-clip-shape-square-06" data-clip-square="square-06" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-pair-square-06-square-07" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-06 square-07">
        <use href="#panel-0-contact-clip-shape-square-06" data-clip-square="square-06" />
        <use href="#panel-0-contact-clip-shape-square-07" data-clip-square="square-07" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-pair-square-06-square-08" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-06 square-08">
        <use href="#panel-0-contact-clip-shape-square-06" data-clip-square="square-06" />
        <use href="#panel-0-contact-clip-shape-square-08" data-clip-square="square-08" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-pair-square-07-square-09" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-07 square-09">
        <use href="#panel-0-contact-clip-shape-square-07" data-clip-square="square-07" />
        <use href="#panel-0-contact-clip-shape-square-09" data-clip-square="square-09" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-pair-square-08-square-09" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-08 square-09">
        <use href="#panel-0-contact-clip-shape-square-08" data-clip-square="square-08" />
        <use href="#panel-0-contact-clip-shape-square-09" data-clip-square="square-09" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-pair-square-09-square-10" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-09 square-10">
        <use href="#panel-0-contact-clip-shape-square-09" data-clip-square="square-09" />
        <use href="#panel-0-contact-clip-shape-square-10" data-clip-square="square-10" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-wall-square-00-bottom" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-00">
        <use href="#panel-0-contact-clip-shape-square-00" data-clip-square="square-00" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-wall-square-00-left" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-00">
        <use href="#panel-0-contact-clip-shape-square-00" data-clip-square="square-00" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-wall-square-01-bottom" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-01">
        <use href="#panel-0-contact-clip-shape-square-01" data-clip-square="square-01" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-wall-square-01-right" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-01">
        <use href="#panel-0-contact-clip-shape-square-01" data-clip-square="square-01" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-wall-square-02-top" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-02">
        <use href="#panel-0-contact-clip-shape-square-02" data-clip-square="square-02" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-wall-square-03-left" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-03">
        <use href="#panel-0-contact-clip-shape-square-03" data-clip-square="square-03" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-wall-square-03-top" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-03">
        <use href="#panel-0-contact-clip-shape-square-03" data-clip-square="square-03" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-wall-square-04-top" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-04">
        <use href="#panel-0-contact-clip-shape-square-04" data-clip-square="square-04" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-wall-square-05-left" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-05">
        <use href="#panel-0-contact-clip-shape-square-05" data-clip-square="square-05" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-wall-square-07-bottom" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-07">
        <use href="#panel-0-contact-clip-shape-square-07" data-clip-square="square-07" />
      </clipPath>
      <clipPath id="panel-0-clip-contact-wall-square-10-right" clipPathUnits="userSpaceOnUse" data-feature="contact-clip" data-squares="square-10">
        <use href="#panel-0-contact-clip-shape-square-10" data-clip-square="square-10" />
      </clipPath>
    </defs>
    <g id="panel-0-contacts" data-layer="contacts" data-overlay="contacts">
      <circle id="panel-0-contact-pair-square-00-square-06" data-squares="square-00 square-06" clip-path="url(#panel-0-clip-contact-pair-square-00-square-06)" cx="174.2482444741012096770558292" cy="433.7517555258987903229441706" r="5.5" fill="#e3c64a" fill-opacity="0.6" data-feature="contact-point" />
      <circle id="panel-0-contact-pair-square-01-square-09" data-squares="square-01 square-09" clip-path="url(#panel-0-clip-contact-pair-square-01-square-09)" cx="433.7517555258987903229441707" cy="433.7517555258987903229441706" r="5.5" fill="#e3c64a" fill-opacity="0.6" data-feature="contact-point" />
      <circle id="panel-0-contact-pair-square-02-square-08" data-squares="square-02 square-08" clip-path="url(#panel-0-clip-contact-pair-square-02-square-08)" cx="316.9976187500726019601504957" cy="174.2482444741012096770558292" r="5.5" fill="#e3c64a" fill-opacity="0.6" data-feature="contact-point" />
      <circle id="panel-0-contact-pair-square-02-square-10" data-squares="square-02 square-10" clip-path="url(#panel-0-clip-contact-pair-square-02-square-10)" cx="455.2458632241738116372063249" cy="174.2482444741012096770558292" r="5.5" fill="#e3c64a" fill-opacity="0.6" data-feature="contact-point" />
      <line id="panel-0-contact-pair-square-03-square-04" data-squares="square-03 square-04" clip-path="url(#panel-0-clip-contact-pair-square-03-square-04)" x1="174.2482444741012096770558292" y1="174.2482444741012096770558292" x2="174.2482444741012096770558292" y2="36" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <line id="panel-0-contact-pair-square-03-square-05" data-squares="square-03 square-05" clip-path="url(#panel-0-clip-contact-pair-square-03-square-05)" x1="36" y1="174.2482444741012096770558292" x2="174.2482444741012096770558292" y2="174.2482444741012096770558292" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <circle id="panel-0-contact-pair-square-04-square-05" data-squares="square-04 square-05" clip-path="url(#panel-0-clip-contact-pair-square-04-square-05)" cx="174.2482444741012096770558292" cy="174.2482444741012096770558292" r="5.5" fill="#e3c64a" fill-opacity="0.6" data-feature="contact-point" />
      <circle id="panel-0-contact-pair-square-04-square-08" data-squares="square-04 square-08" clip-path="url(#panel-0-clip-contact-pair-square-04-square-08)" cx="312.4964889482024193541116584" cy="174.2482444741012096770558292" r="5.5" fill="#e3c64a" fill-opacity="0.6" data-feature="contact-point" />
      <circle id="panel-0-contact-pair-square-05-square-06" data-squares="square-05 square-06" clip-path="url(#panel-0-clip-contact-pair-square-05-square-06)" cx="174.2482444741012096770558292" cy="312.4964889482024193541116584" r="5.5" fill="#e3c64a" fill-opacity="0.6" data-feature="contact-point" />
      <line id="panel-0-contact-pair-square-06-square-07" data-squares="square-06 square-07" clip-path="url(#panel-0-clip-contact-pair-square-06-square-07)" x1="206.3034120101840526840328153" y1="466.3784139906184090658502055" x2="309.2977101789161800297084415" y2="379.3971259369022140919773722" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <line id="panel-0-contact-pair-square-06-square-08" data-squares="square-06 square-08" clip-path="url(#panel-0-clip-contact-pair-square-06-square-08)" x1="298.7022898210838199702915584" y1="366.8511185371989955850784568" x2="220.0976111373026520678529153" y2="273.7755399275206231578275779" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <line id="panel-0-contact-pair-square-07-square-09" data-squares="square-07 square-09" clip-path="url(#panel-0-clip-contact-pair-square-07-square-09)" x1="311.9249980195656436181826097" y1="377.1783149490048811039946792" x2="390.5296767033468115206212528" y2="470.2538935586832535312455582" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <line id="panel-0-contact-pair-square-08-square-09" data-squares="square-08 square-09" clip-path="url(#panel-0-clip-contact-pair-square-08-square-09)" x1="301.3295776617332835587657266" y1="364.6323075493016625970957638" x2="404.3238758304654109044413528" y2="277.6510194955854676232229307" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <line id="panel-0-contact-pair-square-09-square-10" data-squares="square-09 square-10" clip-path="url(#panel-0-clip-contact-pair-square-09-square-10)" x1="406.951163671114874492915521" y1="275.4322085076881346352402377" x2="466.3784139906184090658502054" y2="345.799848211700643238009829" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <line id="panel-0-contact-wall-square-00-bottom" data-squares="square-00" clip-path="url(#panel-0-clip-contact-wall-square-00-bottom)" data-wall="bottom" x1="36" y1="571.9999999999999999999999998" x2="174.2482444741012096770558292" y2="571.9999999999999999999999998" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <line id="panel-0-contact-wall-square-00-left" data-squares="square-00" clip-path="url(#panel-0-clip-contact-wall-square-00-left)" data-wall="left" x1="36" y1="571.9999999999999999999999998" x2="36" y2="433.7517555258987903229441706" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <line id="panel-0-contact-wall-square-01-bottom" data-squares="square-01" clip-path="url(#panel-0-clip-contact-wall-square-01-bottom)" data-wall="bottom" x1="433.7517555258987903229441707" y1="571.9999999999999999999999998" x2="571.9999999999999999999999999" y2="571.9999999999999999999999998" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <line id="panel-0-contact-wall-square-01-right" data-squares="square-01" clip-path="url(#panel-0-clip-contact-wall-square-01-right)" data-wall="right" x1="571.9999999999999999999999999" y1="571.9999999999999999999999998" x2="571.9999999999999999999999999" y2="433.7517555258987903229441706" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <line id="panel-0-contact-wall-square-02-top" data-squares="square-02" clip-path="url(#panel-0-clip-contact-wall-square-02-top)" data-wall="top" x1="316.9976187500726019601504957" y1="36" x2="455.2458632241738116372063249" y2="36" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <line id="panel-0-contact-wall-square-03-left" data-squares="square-03" clip-path="url(#panel-0-clip-contact-wall-square-03-left)" data-wall="left" x1="36" y1="174.2482444741012096770558292" x2="36" y2="36" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <line id="panel-0-contact-wall-square-03-top" data-squares="square-03" clip-path="url(#panel-0-clip-contact-wall-square-03-top)" data-wall="top" x1="36" y1="36" x2="174.2482444741012096770558292" y2="36" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <line id="panel-0-contact-wall-square-04-top" data-squares="square-04" clip-path="url(#panel-0-clip-contact-wall-square-04-top)" data-wall="top" x1="174.2482444741012096770558292" y1="36" x2="312.4964889482024193541116584" y2="36" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <line id="panel-0-contact-wall-square-05-left" data-squares="square-05" clip-path="url(#panel-0-clip-contact-wall-square-05-left)" data-wall="left" x1="36" y1="312.4964889482024193541116584" x2="36" y2="174.2482444741012096770558292" stroke="#e3c64a" stroke-opacity="0.6" stroke-width="9" stroke-linecap="round" vector-effect="non-scaling-stroke" data-feature="contact-segment" />
      <circle id="panel-0-contact-wall-square-07-bottom" data-squares="square-07" clip-path="url(#panel-0-clip-contact-wall-square-07-bottom)" data-wall="bottom" cx="295.5035110517975806458883415" cy="571.9999999999999999999999998" r="5.5" fill="#e3c64a" fill-opacity="0.6" data-feature="contact-point" />
      <circle id="panel-0-contact-wall-square-10-right" data-squares="square-10" clip-path="url(#panel-0-clip-contact-wall-square-10-right)" data-wall="right" cx="571.9999999999999999999999999" cy="256.5997491700871152761543029" r="5.5" fill="#e3c64a" fill-opacity="0.6" data-feature="contact-point" />
    </g>
    <g id="panel-0-outlines" data-layer="outlines">
      <polygon data-feature="square-outline" data-square="square-00" points="36,571.9999999999999999999999998 174.2482444741012096770558292,571.9999999999999999999999998 174.2482444741012096770558292,433.7517555258987903229441706 36,433.7517555258987903229441706" stroke-linejoin="round" fill="none" stroke="#000000" stroke-width="1.25" vector-effect="non-scaling-stroke" />
      <polygon data-feature="square-outline" data-square="square-01" points="433.7517555258987903229441707,571.9999999999999999999999998 571.9999999999999999999999999,571.9999999999999999999999998 571.9999999999999999999999999,433.7517555258987903229441706 433.7517555258987903229441707,433.7517555258987903229441706" stroke-linejoin="round" fill="none" stroke="#000000" stroke-width="1.25" vector-effect="non-scaling-stroke" />
      <polygon data-feature="square-outline" data-square="square-02" points="316.9976187500726019601504957,174.2482444741012096770558292 455.2458632241738116372063249,174.2482444741012096770558292 455.2458632241738116372063249,36 316.9976187500726019601504957,36" stroke-linejoin="round" fill="none" stroke="#000000" stroke-width="1.25" vector-effect="non-scaling-stroke" />
      <polygon data-feature="square-outline" data-square="square-03" points="36,174.2482444741012096770558292 174.2482444741012096770558292,174.2482444741012096770558292 174.2482444741012096770558292,36 36,36" stroke-linejoin="round" fill="none" stroke="#000000" stroke-width="1.25" vector-effect="non-scaling-stroke" />
      <polygon data-feature="square-outline" data-square="square-04" points="174.2482444741012096770558292,174.2482444741012096770558292 312.4964889482024193541116584,174.2482444741012096770558292 312.4964889482024193541116584,36 174.2482444741012096770558292,36" stroke-linejoin="round" fill="none" stroke="#000000" stroke-width="1.25" vector-effect="non-scaling-stroke" />
      <polygon data-feature="square-outline" data-square="square-05" points="36,312.4964889482024193541116584 174.2482444741012096770558292,312.4964889482024193541116584 174.2482444741012096770558292,174.2482444741012096770558292 36,174.2482444741012096770558292" stroke-linejoin="round" fill="none" stroke="#000000" stroke-width="1.25" vector-effect="non-scaling-stroke" />
      <polygon data-feature="square-outline" data-square="square-06" points="203.6761241695345890955586471,468.5972249785157420538328984 309.2977101789161800297084415,379.3971259369022140919773722 220.0976111373026520678529153,273.7755399275206231578275779 114.4760251279210611337031209,362.975638969134151119683104" stroke-linejoin="round" fill="none" stroke="#000000" stroke-width="1.25" vector-effect="non-scaling-stroke" />
      <polygon data-feature="square-outline" data-square="square-07" points="295.5035110517975806458883415,571.9999999999999999999999998 401.1250970611791715800381359,482.7999009583864720381444737 311.9249980195656436181826097,377.1783149490048811039946792 206.3034120101840526840328153,466.3784139906184090658502055" stroke-linejoin="round" fill="none" stroke="#000000" stroke-width="1.25" vector-effect="non-scaling-stroke" />
      <polygon data-feature="square-outline" data-square="square-08" points="298.7022898210838199702915584,366.8511185371989955850784568 404.3238758304654109044413528,277.6510194955854676232229307 315.1237767888518829425858266,172.0294334862038766890731362 209.5021907794702920084360322,261.2295325278174046509286623" stroke-linejoin="round" fill="none" stroke="#000000" stroke-width="1.25" vector-effect="non-scaling-stroke" />
      <polygon data-feature="square-outline" data-square="square-09" points="390.5296767033468115206212528,470.2538935586832535312455582 496.1512627127284024547710472,381.053794517069725569390032 406.951163671114874492915521,275.4322085076881346352402377 301.3295776617332835587657266,364.6323075493016625970957638" stroke-linejoin="round" fill="none" stroke="#000000" stroke-width="1.25" vector-effect="non-scaling-stroke" />
      <polygon data-feature="square-outline" data-square="square-10" points="466.3784139906184090658502054,345.799848211700643238009829 571.9999999999999999999999999,256.5997491700871152761543029 482.7999009583864720381444737,150.9781631607055243420045084 377.1783149490048811039946793,240.1782622023190523038600346" stroke-linejoin="round" fill="none" stroke="#000000" stroke-width="1.25" vector-effect="non-scaling-stroke" />
      <rect data-feature="container-outline" x="36" y="36" width="535.9999999999999999999999999" height="535.9999999999999999999999999" fill="none" stroke="#000000" stroke-width="1.25" vector-effect="non-scaling-stroke" />
    </g>
  </g>
</svg>
</a></div>
<figcaption><strong>Figure 1.</strong> The attaining construction: six squares are
axis-aligned and five share a tilted orientation. The drawing is rounded for display;
the <a href="https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/cases/trump11/verify_exact.py">exact witness check</a> uses algebraic coordinates.
Touching edges and corners are legal.
The construction reaches both opposite walls in each coordinate direction.</figcaption>
</figure>

An upper bound needs one example: the packing drawn above.
A lower bound must exclude every arrangement in a smaller container, including
unfamiliar contact patterns and eleven independently chosen angles.
Numerical search can suggest a good packing, but failing to find a better one does not
exhaust those possibilities.

Suppose a packing fits in a smaller square, of side $S<T$. The proof must handle that
packing without knowing any of its positions or angles.
It first classifies the centers and uses exact certificates to eliminate impossible
classes. Every survivor, after a symmetry of the container, enters a capture argument
that encloses its positions and angles near the known construction.

The last step connects this global restriction to a local theorem.
The same smaller packing can be placed inside the exact side-$T$ container, within a
checked neighborhood where only the construction is feasible.
But the construction spans $T$, so it cannot fit inside the smaller container.
Figure 2 shows both halves of the proof.

<figure>
<svg xmlns="http://www.w3.org/2000/svg" class="n11-diagram n11-roadmap" width="900" height="629" viewBox="0 36 900 629" role="img" aria-labelledby="n11-roadmap-title n11-roadmap-desc"><title id="n11-roadmap-title">Two routes to the exact eleven-square optimum</title><desc id="n11-roadmap-desc">The exact Trump witness gives the upper bound. For the lower bound, assume a packing with side S smaller than T. Exact case classification, exclusion, symmetry, capture, fixed-T pose inclusion and local isolation force the same packing to be the witness of span T, a contradiction. Counts are case classes, not numbers of packings. The diagram summarizes accepted premises and does not rerun their geometry.</desc><rect x="36" y="48" width="828" height="70" rx="10" fill="var(--kpress-doc-bg)" stroke="var(--kpress-doc-accent)" stroke-width="2"/><text class="n11-diagram-label" x="58" y="77" text-anchor="start" fill="var(--kpress-doc-text)">Exact construction at T</text><text class="n11-diagram-note" x="58" y="103" text-anchor="start" fill="var(--kpress-doc-text)">Eleven unit squares fit: s(11) ≤ T</text><text class="n11-diagram-note" x="450" y="151" text-anchor="middle" fill="var(--kpress-doc-text)">For the lower bound, assume S &lt; T</text><rect x="36" y="170" width="828" height="70" rx="10" fill="var(--kpress-doc-bg)" stroke="var(--kpress-doc-border)" stroke-width="2"/><text class="n11-diagram-label" x="58" y="199" text-anchor="start" fill="var(--kpress-doc-text)">Assume S &lt; T</text><text class="n11-diagram-note" x="58" y="225" text-anchor="start" fill="var(--kpress-doc-text)">The same packing sits inside cap U &gt; T</text><path d="M450 240v20" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><path d="M443 254l7 8 7-8" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><rect x="36" y="263" width="828" height="70" rx="10" fill="var(--kpress-doc-bg)" stroke="var(--kpress-doc-border)" stroke-width="2"/><text class="n11-diagram-label" x="58" y="292" text-anchor="start" fill="var(--kpress-doc-text)">Classify center patterns</text><text class="n11-diagram-note" x="58" y="318" text-anchor="start" fill="var(--kpress-doc-text)">16 closed cells; 2,184 case classes</text><path d="M450 333v20" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><path d="M443 347l7 8 7-8" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><rect x="36" y="356" width="828" height="70" rx="10" fill="var(--kpress-doc-bg)" stroke="var(--kpress-doc-border)" stroke-width="2"/><text class="n11-diagram-label" x="58" y="385" text-anchor="start" fill="var(--kpress-doc-text)">Exclude, then use symmetry</text><text class="n11-diagram-note" x="58" y="411" text-anchor="start" fill="var(--kpress-doc-text)">2,180 excluded; D4 leaves case 438</text><path d="M450 426v20" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><path d="M443 440l7 8 7-8" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><rect x="36" y="449" width="828" height="70" rx="10" fill="var(--kpress-doc-bg)" stroke="var(--kpress-doc-border)" stroke-width="2"/><text class="n11-diagram-label" x="58" y="478" text-anchor="start" fill="var(--kpress-doc-text)">Capture, align, include</text><text class="n11-diagram-note" x="58" y="504" text-anchor="start" fill="var(--kpress-doc-text)">Packing enters fixed-T rectangle</text><path d="M450 519v20" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><path d="M443 533l7 8 7-8" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><rect x="36" y="542" width="828" height="70" rx="10" fill="var(--kpress-doc-bg)" stroke="var(--kpress-doc-accent)" stroke-width="2"/><text class="n11-diagram-label" x="58" y="571" text-anchor="start" fill="var(--kpress-doc-text)">Apply fixed-T local isolation</text><text class="n11-diagram-note" x="58" y="597" text-anchor="start" fill="var(--kpress-doc-text)">Only the witness remains; span T &gt; S</text><text class="n11-diagram-label" x="450" y="642" text-anchor="middle" fill="var(--kpress-doc-text)">No packing has S &lt; T; hence s(11) = T</text></svg>
<figcaption><strong>Figure 2.</strong> Two routes to the exact optimum. The construction
supplies an upper bound. The lower-bound route follows an arbitrary hypothetical
smaller packing through restrictions that preserve every feasible possibility, ending
in a contradiction. The case counts classify continuous families of positions and
angles; they do not count individual packings. The
<a href="https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json">accepted composition</a>
checks the joins between these obligations.</figcaption>
</figure>

The geometric steps are
[center classification](#sixteen-regions-cover-all-possible-centers),
[safe exclusions](#one-geometric-invariant-supports-the-certificates),
[symmetry](#symmetry-reduces-the-four-survivors-to-one), and
[capture](#capture-forces-case-438-near-the-construction).
The [local estimate](#the-local-argument-excludes-every-nonzero-motion) and
[exact frame change](#closing-the-gap-between-the-rational-cap-and-the-exact-optimum)
complete the contradiction.

The Squares Project records this result as **T-060, S5/V3/C3**: a result resolving the
global optimum, supported by exact computational verification and a mapped mathematical
review, machine-checked here with its review record pending.
Under the ladder of 2026-09-30, rung 4 on either axis also needs a second adversarial
review by a distinct reviewer and a retained human oversight record, which this result
awaits. This is a computer-assisted proof with a stated software trust base; a completed
proof-assistant formalization is not claimed.[^review]

## From Weighted Points to a Global Proof

The [earlier explainer][earlier] develops a lower-bound method based on weighted points.
Select a small **core** strictly inside each packed square.
If every possible core must collect at least one unit of weight, eleven disjoint cores
must collect at least eleven units.
A certificate with less than eleven units available proves a contradiction.
Exact coverage checks turn that idea into a theorem about every position and
orientation.

Threshold features strengthen the method by assigning weight when a prescribed condition
on several points holds.
The earlier paper explains the point certificate T-018, the threshold certificate T-025
and T-026’s dilation bound $s(11)\ge3.8264474\ldots$. Kleddamag’s subsequent T-037
establishes $s(11)>31/8=3.875$.[^lineage]

The gap between $3.875$ and $T$ is small, but closeness of two numbers supplies no
geometric information about a hypothetical packing in between.
The optimality proof adds two kinds of information.
It conditions geometric and charge arguments on occupied center regions, so they can
eliminate individual patterns.
For the pattern that survives, it proves where every square must be, then applies a
quantitative local theorem at the exact endpoint.

These are mathematical antecedents, not extra numerical assumptions.
The final proof does not infer equality from a sequence of improving lower bounds.
Nor is wand125’s separate check of certificate row minima, or Tokoharu’s C++
rectangle-density verifier, a verifier of this global optimality argument.
Those tools concern related certificates; the case exclusions, capture and local
endpoint require the additional checks below.[^tools]

## The Construction Gives One Half of the Answer

The algebraic parameter $u$ determines a rotation:

$$
c=\frac{1-u^2}{1+u^2},\qquad s=\frac{2u}{1+u^2},\qquad c^2+s^2=1.
$$

Here $c$ and $s$ are the cosine and sine of the common tilted orientation in Figure 1.
Appendix A gives the placement formulas.
Because a rotation preserves length and right angles, those formulas produce eleven unit
squares.

Feasibility has two finite checks.
Each of the 44 vertices must lie in $[0,T]^2$. Each of the 55 pairs of squares must
admit a **weak separating axis**: a direction in which their projection intervals have
disjoint interiors. For convex polygons it suffices to examine normals to their edges.
A zero gap is accepted, since it represents legal contact.

The calculations take place in the number field $\mathbb Q(u)$. Polynomial expressions
are reduced using the equation defining $u$; the selected root is isolated by rational
bounds. Exact identities establish zero, while rational interval refinement determines
the signs of nonzero expressions.
A small floating-point residual is never substituted for an equality.[^construction]

These checks prove $s(11)\le T$. The wall contacts also prove a fact needed at the end:
the construction’s horizontal and vertical spans are both exactly $T$.

## Sixteen Regions Cover All Possible Centers

Most of the global calculations use the rational number

$$
U=\frac{387708359002281417731}{10^{20}}>T.
$$

This **cap** is slightly larger than the proposed optimum.
If a packing existed in a square of side $S<T$, we could translate its container
concentrically into $[0,U]^2$. Its unit squares would keep their sizes, angles and
relative positions. Thus excluding possibilities in the cap also excludes them for every
smaller container.

A unit square contains an open disk of radius $1/2$ about its center.
Two packed squares therefore have centers at least one unit apart: otherwise those
disks, and hence the square interiors, would overlap.
Also, each center $p$ lies in $[1/2,U-1/2]^2$. Normalize this center domain by writing

$$
z=\frac{p-(1/2,1/2)}{U-1}\in[0,1]^2.
$$

Choose sixteen rational sites.
Assign each point of $[0,1]^2$ to any nearest site, keeping ties.
The resulting **closed Voronoi cells** cover the whole square.
They are the polygons in Figure 3, rather than the squares of a uniform grid.
The exact checker reconstructs them from nearest-site halfplanes and proves

$$
(U-1)^2\operatorname{diam}(C_j)^2<1
\qquad\text{for every cell }C_j.
$$

**Center-cover lemma.** A physical cell contains at most one packed-square center.
Indeed, two centers in it would be less than one unit apart, contradicting the disk
argument. At a cell boundary either containing label may be chosen; the same argument
still prevents two centers from receiving one label.[^cover]

<figure>
<div class="figure-pair">
<svg xmlns="http://www.w3.org/2000/svg" class="n11-diagram n11-cover" width="640" height="640" viewBox="0 0 640 640" role="img" aria-labelledby="n11-cover-title n11-cover-desc"><title id="n11-cover-title">Sixteen exact center-cover Voronoi cells</title><desc id="n11-cover-desc">Sixteen closed rational Voronoi cells partition the normalized square. Their retained exact vertices are converted to SVG pixels only for illustration.</desc><polygon data-cell="0" data-selected="true" points="36.0000,604.0000 155.2919,604.0000 188.3219,502.6563 154.1454,452.1239 36.0000,452.9634" fill="#dcebef"/><polygon data-cell="1" data-selected="true" points="155.2919,604.0000 340.6764,604.0000 304.0693,501.7705 188.3219,502.6563" fill="#dcebef"/><polygon data-cell="2" data-selected="true" points="340.6764,604.0000 451.1341,604.0000 471.4980,472.6249 451.7217,446.7695 341.0024,446.1164 304.0693,501.7705" fill="#dcebef"/><polygon data-cell="3" data-selected="true" points="451.1341,604.0000 604.0000,604.0000 604.0000,487.0390 471.4980,472.6249" fill="#dcebef"/><polygon data-cell="4" data-selected="true" points="36.0000,300.2053 36.0000,452.9634 154.1454,452.1239 187.2495,350.6436 153.7445,302.8944" fill="#dcebef"/><polygon data-cell="5" data-selected="false" points="187.2495,350.6436 154.1454,452.1239 188.3219,502.6563 304.0693,501.7705 341.0024,446.1164 302.6696,347.9129" fill="#dcebef"/><polygon data-cell="6" data-selected="false" points="337.3304,292.0871 302.6696,347.9129 341.0024,446.1164 451.7217,446.7695 486.2555,337.1056 452.7505,289.3564" fill="#dcebef"/><polygon data-cell="7" data-selected="false" points="604.0000,487.0390 604.0000,339.7947 486.2555,337.1056 451.7217,446.7695 471.4980,472.6249" fill="#dcebef"/><polygon data-cell="8" data-selected="true" points="36.0000,152.9610 36.0000,300.2053 153.7445,302.8944 188.2783,193.2305 168.5020,167.3751" fill="#dcebef"/><polygon data-cell="9" data-selected="true" points="188.2783,193.2305 153.7445,302.8944 187.2495,350.6436 302.6696,347.9129 337.3304,292.0871 298.9976,193.8836" fill="#dcebef"/><polygon data-cell="10" data-selected="true" points="335.9307,138.2295 298.9976,193.8836 337.3304,292.0871 452.7505,289.3564 485.8546,187.8761 451.6781,137.3437" fill="#dcebef"/><polygon data-cell="11" data-selected="true" points="604.0000,339.7947 604.0000,187.0366 485.8546,187.8761 452.7505,289.3564 486.2555,337.1056" fill="#dcebef"/><polygon data-cell="12" data-selected="false" points="188.8659,36.0000 36.0000,36.0000 36.0000,152.9610 168.5020,167.3751" fill="#dcebef"/><polygon data-cell="13" data-selected="true" points="299.3236,36.0000 188.8659,36.0000 168.5020,167.3751 188.2783,193.2305 298.9976,193.8836 335.9307,138.2295" fill="#dcebef"/><polygon data-cell="14" data-selected="false" points="484.7081,36.0000 299.3236,36.0000 335.9307,138.2295 451.6781,137.3437" fill="#dcebef"/><polygon data-cell="15" data-selected="true" points="604.0000,187.0366 604.0000,36.0000 484.7081,36.0000 451.6781,137.3437 485.8546,187.8761" fill="#dcebef"/><line x1="36.0000" y1="604.0000" x2="155.2919" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><line x1="155.2919" y1="604.0000" x2="188.3219" y2="502.6563" stroke="#52667a" stroke-width="1.2"/><line x1="188.3219" y1="502.6563" x2="154.1454" y2="452.1239" stroke="#52667a" stroke-width="1.2"/><line x1="154.1454" y1="452.1239" x2="36.0000" y2="452.9634" stroke="#52667a" stroke-width="1.2"/><line x1="36.0000" y1="452.9634" x2="36.0000" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="95.6349" y="528.5023" text-anchor="middle" dominant-baseline="central" fill="#172b3a">0</text><line x1="155.2919" y1="604.0000" x2="340.6764" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><line x1="340.6764" y1="604.0000" x2="304.0693" y2="501.7705" stroke="#52667a" stroke-width="1.2"/><line x1="304.0693" y1="501.7705" x2="188.3219" y2="502.6563" stroke="#52667a" stroke-width="1.2"/><line x1="188.3219" y1="502.6563" x2="155.2919" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="247.9787" y="578.1543" text-anchor="middle" dominant-baseline="central" fill="#172b3a">1</text><line x1="340.6764" y1="604.0000" x2="451.1341" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><line x1="451.1341" y1="604.0000" x2="471.4980" y2="472.6249" stroke="#52667a" stroke-width="1.2"/><line x1="471.4980" y1="472.6249" x2="451.7217" y2="446.7695" stroke="#52667a" stroke-width="1.2"/><line x1="451.7217" y1="446.7695" x2="341.0024" y2="446.1164" stroke="#52667a" stroke-width="1.2"/><line x1="341.0024" y1="446.1164" x2="304.0693" y2="501.7705" stroke="#52667a" stroke-width="1.2"/><line x1="304.0693" y1="501.7705" x2="340.6764" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="395.8970" y="525.1866" text-anchor="middle" dominant-baseline="central" fill="#172b3a">2</text><line x1="451.1341" y1="604.0000" x2="604.0000" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><line x1="604.0000" y1="604.0000" x2="604.0000" y2="487.0390" stroke="#52667a" stroke-width="1.2"/><line x1="604.0000" y1="487.0390" x2="471.4980" y2="472.6249" stroke="#52667a" stroke-width="1.2"/><line x1="471.4980" y1="472.6249" x2="451.1341" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="527.6389" y="545.6073" text-anchor="middle" dominant-baseline="central" fill="#172b3a">3</text><line x1="36.0000" y1="300.2053" x2="36.0000" y2="452.9634" stroke="#52667a" stroke-width="1.2"/><line x1="36.0000" y1="452.9634" x2="154.1454" y2="452.1239" stroke="#52667a" stroke-width="1.2"/><line x1="154.1454" y1="452.1239" x2="187.2495" y2="350.6436" stroke="#52667a" stroke-width="1.2"/><line x1="187.2495" y1="350.6436" x2="153.7445" y2="302.8944" stroke="#52667a" stroke-width="1.2"/><line x1="153.7445" y1="302.8944" x2="36.0000" y2="300.2053" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="94.5554" y="376.5847" text-anchor="middle" dominant-baseline="central" fill="#172b3a">4</text><line x1="187.2495" y1="350.6436" x2="154.1454" y2="452.1239" stroke="#52667a" stroke-width="1.2"/><line x1="154.1454" y1="452.1239" x2="188.3219" y2="502.6563" stroke="#52667a" stroke-width="1.2"/><line x1="188.3219" y1="502.6563" x2="304.0693" y2="501.7705" stroke="#52667a" stroke-width="1.2"/><line x1="304.0693" y1="501.7705" x2="341.0024" y2="446.1164" stroke="#52667a" stroke-width="1.2"/><line x1="341.0024" y1="446.1164" x2="302.6696" y2="347.9129" stroke="#52667a" stroke-width="1.2"/><line x1="302.6696" y1="347.9129" x2="187.2495" y2="350.6436" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="246.8163" y="426.2541" text-anchor="middle" dominant-baseline="central" fill="#172b3a">5</text><line x1="337.3304" y1="292.0871" x2="302.6696" y2="347.9129" stroke="#52667a" stroke-width="1.2"/><line x1="302.6696" y1="347.9129" x2="341.0024" y2="446.1164" stroke="#52667a" stroke-width="1.2"/><line x1="341.0024" y1="446.1164" x2="451.7217" y2="446.7695" stroke="#52667a" stroke-width="1.2"/><line x1="451.7217" y1="446.7695" x2="486.2555" y2="337.1056" stroke="#52667a" stroke-width="1.2"/><line x1="486.2555" y1="337.1056" x2="452.7505" y2="289.3564" stroke="#52667a" stroke-width="1.2"/><line x1="452.7505" y1="289.3564" x2="337.3304" y2="292.0871" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="396.8260" y="367.6992" text-anchor="middle" dominant-baseline="central" fill="#172b3a">6</text><line x1="604.0000" y1="487.0390" x2="604.0000" y2="339.7947" stroke="#52667a" stroke-width="1.2"/><line x1="604.0000" y1="339.7947" x2="486.2555" y2="337.1056" stroke="#52667a" stroke-width="1.2"/><line x1="486.2555" y1="337.1056" x2="451.7217" y2="446.7695" stroke="#52667a" stroke-width="1.2"/><line x1="451.7217" y1="446.7695" x2="471.4980" y2="472.6249" stroke="#52667a" stroke-width="1.2"/><line x1="471.4980" y1="472.6249" x2="604.0000" y2="487.0390" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="542.0187" y="413.4212" text-anchor="middle" dominant-baseline="central" fill="#172b3a">7</text><line x1="36.0000" y1="152.9610" x2="36.0000" y2="300.2053" stroke="#52667a" stroke-width="1.2"/><line x1="36.0000" y1="300.2053" x2="153.7445" y2="302.8944" stroke="#52667a" stroke-width="1.2"/><line x1="153.7445" y1="302.8944" x2="188.2783" y2="193.2305" stroke="#52667a" stroke-width="1.2"/><line x1="188.2783" y1="193.2305" x2="168.5020" y2="167.3751" stroke="#52667a" stroke-width="1.2"/><line x1="168.5020" y1="167.3751" x2="36.0000" y2="152.9610" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="97.9813" y="226.5788" text-anchor="middle" dominant-baseline="central" fill="#172b3a">8</text><line x1="188.2783" y1="193.2305" x2="153.7445" y2="302.8944" stroke="#52667a" stroke-width="1.2"/><line x1="153.7445" y1="302.8944" x2="187.2495" y2="350.6436" stroke="#52667a" stroke-width="1.2"/><line x1="187.2495" y1="350.6436" x2="302.6696" y2="347.9129" stroke="#52667a" stroke-width="1.2"/><line x1="302.6696" y1="347.9129" x2="337.3304" y2="292.0871" stroke="#52667a" stroke-width="1.2"/><line x1="337.3304" y1="292.0871" x2="298.9976" y2="193.8836" stroke="#52667a" stroke-width="1.2"/><line x1="298.9976" y1="193.8836" x2="188.2783" y2="193.2305" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="243.1740" y="272.3008" text-anchor="middle" dominant-baseline="central" fill="#172b3a">9</text><line x1="335.9307" y1="138.2295" x2="298.9976" y2="193.8836" stroke="#52667a" stroke-width="1.2"/><line x1="298.9976" y1="193.8836" x2="337.3304" y2="292.0871" stroke="#52667a" stroke-width="1.2"/><line x1="337.3304" y1="292.0871" x2="452.7505" y2="289.3564" stroke="#52667a" stroke-width="1.2"/><line x1="452.7505" y1="289.3564" x2="485.8546" y2="187.8761" stroke="#52667a" stroke-width="1.2"/><line x1="485.8546" y1="187.8761" x2="451.6781" y2="137.3437" stroke="#52667a" stroke-width="1.2"/><line x1="451.6781" y1="137.3437" x2="335.9307" y2="138.2295" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="393.1837" y="213.7459" text-anchor="middle" dominant-baseline="central" fill="#172b3a">10</text><line x1="604.0000" y1="339.7947" x2="604.0000" y2="187.0366" stroke="#52667a" stroke-width="1.2"/><line x1="604.0000" y1="187.0366" x2="485.8546" y2="187.8761" stroke="#52667a" stroke-width="1.2"/><line x1="485.8546" y1="187.8761" x2="452.7505" y2="289.3564" stroke="#52667a" stroke-width="1.2"/><line x1="452.7505" y1="289.3564" x2="486.2555" y2="337.1056" stroke="#52667a" stroke-width="1.2"/><line x1="486.2555" y1="337.1056" x2="604.0000" y2="339.7947" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="545.4446" y="263.4153" text-anchor="middle" dominant-baseline="central" fill="#172b3a">11</text><line x1="188.8659" y1="36.0000" x2="36.0000" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><line x1="36.0000" y1="36.0000" x2="36.0000" y2="152.9610" stroke="#52667a" stroke-width="1.2"/><line x1="36.0000" y1="152.9610" x2="168.5020" y2="167.3751" stroke="#52667a" stroke-width="1.2"/><line x1="168.5020" y1="167.3751" x2="188.8659" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="112.3611" y="94.3927" text-anchor="middle" dominant-baseline="central" fill="#172b3a">12</text><line x1="299.3236" y1="36.0000" x2="188.8659" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><line x1="188.8659" y1="36.0000" x2="168.5020" y2="167.3751" stroke="#52667a" stroke-width="1.2"/><line x1="168.5020" y1="167.3751" x2="188.2783" y2="193.2305" stroke="#52667a" stroke-width="1.2"/><line x1="188.2783" y1="193.2305" x2="298.9976" y2="193.8836" stroke="#52667a" stroke-width="1.2"/><line x1="298.9976" y1="193.8836" x2="335.9307" y2="138.2295" stroke="#52667a" stroke-width="1.2"/><line x1="335.9307" y1="138.2295" x2="299.3236" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="244.1030" y="114.8134" text-anchor="middle" dominant-baseline="central" fill="#172b3a">13</text><line x1="484.7081" y1="36.0000" x2="299.3236" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><line x1="299.3236" y1="36.0000" x2="335.9307" y2="138.2295" stroke="#52667a" stroke-width="1.2"/><line x1="335.9307" y1="138.2295" x2="451.6781" y2="137.3437" stroke="#52667a" stroke-width="1.2"/><line x1="451.6781" y1="137.3437" x2="484.7081" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="392.0213" y="61.8457" text-anchor="middle" dominant-baseline="central" fill="#172b3a">14</text><line x1="604.0000" y1="187.0366" x2="604.0000" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><line x1="604.0000" y1="36.0000" x2="484.7081" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><line x1="484.7081" y1="36.0000" x2="451.6781" y2="137.3437" stroke="#52667a" stroke-width="1.2"/><line x1="451.6781" y1="137.3437" x2="485.8546" y2="187.8761" stroke="#52667a" stroke-width="1.2"/><line x1="485.8546" y1="187.8761" x2="604.0000" y2="187.0366" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="544.3651" y="111.4977" text-anchor="middle" dominant-baseline="central" fill="#172b3a">15</text><line x1="36" y1="36" x2="604" y2="36" stroke="#334155" stroke-width="2"/><line x1="604" y1="36" x2="604" y2="604" stroke="#334155" stroke-width="2"/><line x1="604" y1="604" x2="36" y2="604" stroke="#334155" stroke-width="2"/><line x1="36" y1="604" x2="36" y2="36" stroke="#334155" stroke-width="2"/></svg>
<svg xmlns="http://www.w3.org/2000/svg" class="n11-diagram n11-mask" width="640" height="640" viewBox="0 0 640 640" role="img" aria-labelledby="n11-mask-title n11-mask-desc"><title id="n11-mask-title">Case 438 selects eleven of the sixteen center cells</title><desc id="n11-mask-desc">The eleven selected Voronoi cells of case 438 are teal; the other five are gray. Cell vertices are exact rational proof input, converted to SVG pixels for illustration. Selection is cell membership, not an owned-hull diagram.</desc><polygon data-cell="0" data-selected="true" points="36.0000,604.0000 155.2919,604.0000 188.3219,502.6563 154.1454,452.1239 36.0000,452.9634" fill="#1d7874"/><polygon data-cell="1" data-selected="true" points="155.2919,604.0000 340.6764,604.0000 304.0693,501.7705 188.3219,502.6563" fill="#1d7874"/><polygon data-cell="2" data-selected="true" points="340.6764,604.0000 451.1341,604.0000 471.4980,472.6249 451.7217,446.7695 341.0024,446.1164 304.0693,501.7705" fill="#1d7874"/><polygon data-cell="3" data-selected="true" points="451.1341,604.0000 604.0000,604.0000 604.0000,487.0390 471.4980,472.6249" fill="#1d7874"/><polygon data-cell="4" data-selected="true" points="36.0000,300.2053 36.0000,452.9634 154.1454,452.1239 187.2495,350.6436 153.7445,302.8944" fill="#1d7874"/><polygon data-cell="5" data-selected="false" points="187.2495,350.6436 154.1454,452.1239 188.3219,502.6563 304.0693,501.7705 341.0024,446.1164 302.6696,347.9129" fill="#e2e8f0"/><polygon data-cell="6" data-selected="false" points="337.3304,292.0871 302.6696,347.9129 341.0024,446.1164 451.7217,446.7695 486.2555,337.1056 452.7505,289.3564" fill="#e2e8f0"/><polygon data-cell="7" data-selected="false" points="604.0000,487.0390 604.0000,339.7947 486.2555,337.1056 451.7217,446.7695 471.4980,472.6249" fill="#e2e8f0"/><polygon data-cell="8" data-selected="true" points="36.0000,152.9610 36.0000,300.2053 153.7445,302.8944 188.2783,193.2305 168.5020,167.3751" fill="#1d7874"/><polygon data-cell="9" data-selected="true" points="188.2783,193.2305 153.7445,302.8944 187.2495,350.6436 302.6696,347.9129 337.3304,292.0871 298.9976,193.8836" fill="#1d7874"/><polygon data-cell="10" data-selected="true" points="335.9307,138.2295 298.9976,193.8836 337.3304,292.0871 452.7505,289.3564 485.8546,187.8761 451.6781,137.3437" fill="#1d7874"/><polygon data-cell="11" data-selected="true" points="604.0000,339.7947 604.0000,187.0366 485.8546,187.8761 452.7505,289.3564 486.2555,337.1056" fill="#1d7874"/><polygon data-cell="12" data-selected="false" points="188.8659,36.0000 36.0000,36.0000 36.0000,152.9610 168.5020,167.3751" fill="#e2e8f0"/><polygon data-cell="13" data-selected="true" points="299.3236,36.0000 188.8659,36.0000 168.5020,167.3751 188.2783,193.2305 298.9976,193.8836 335.9307,138.2295" fill="#1d7874"/><polygon data-cell="14" data-selected="false" points="484.7081,36.0000 299.3236,36.0000 335.9307,138.2295 451.6781,137.3437" fill="#e2e8f0"/><polygon data-cell="15" data-selected="true" points="604.0000,187.0366 604.0000,36.0000 484.7081,36.0000 451.6781,137.3437 485.8546,187.8761" fill="#1d7874"/><line x1="36.0000" y1="604.0000" x2="155.2919" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><line x1="155.2919" y1="604.0000" x2="188.3219" y2="502.6563" stroke="#52667a" stroke-width="1.2"/><line x1="188.3219" y1="502.6563" x2="154.1454" y2="452.1239" stroke="#52667a" stroke-width="1.2"/><line x1="154.1454" y1="452.1239" x2="36.0000" y2="452.9634" stroke="#52667a" stroke-width="1.2"/><line x1="36.0000" y1="452.9634" x2="36.0000" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="95.6349" y="528.5023" text-anchor="middle" dominant-baseline="central" fill="#fff">0</text><line x1="155.2919" y1="604.0000" x2="340.6764" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><line x1="340.6764" y1="604.0000" x2="304.0693" y2="501.7705" stroke="#52667a" stroke-width="1.2"/><line x1="304.0693" y1="501.7705" x2="188.3219" y2="502.6563" stroke="#52667a" stroke-width="1.2"/><line x1="188.3219" y1="502.6563" x2="155.2919" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="247.9787" y="578.1543" text-anchor="middle" dominant-baseline="central" fill="#fff">1</text><line x1="340.6764" y1="604.0000" x2="451.1341" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><line x1="451.1341" y1="604.0000" x2="471.4980" y2="472.6249" stroke="#52667a" stroke-width="1.2"/><line x1="471.4980" y1="472.6249" x2="451.7217" y2="446.7695" stroke="#52667a" stroke-width="1.2"/><line x1="451.7217" y1="446.7695" x2="341.0024" y2="446.1164" stroke="#52667a" stroke-width="1.2"/><line x1="341.0024" y1="446.1164" x2="304.0693" y2="501.7705" stroke="#52667a" stroke-width="1.2"/><line x1="304.0693" y1="501.7705" x2="340.6764" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="395.8970" y="525.1866" text-anchor="middle" dominant-baseline="central" fill="#fff">2</text><line x1="451.1341" y1="604.0000" x2="604.0000" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><line x1="604.0000" y1="604.0000" x2="604.0000" y2="487.0390" stroke="#52667a" stroke-width="1.2"/><line x1="604.0000" y1="487.0390" x2="471.4980" y2="472.6249" stroke="#52667a" stroke-width="1.2"/><line x1="471.4980" y1="472.6249" x2="451.1341" y2="604.0000" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="527.6389" y="545.6073" text-anchor="middle" dominant-baseline="central" fill="#fff">3</text><line x1="36.0000" y1="300.2053" x2="36.0000" y2="452.9634" stroke="#52667a" stroke-width="1.2"/><line x1="36.0000" y1="452.9634" x2="154.1454" y2="452.1239" stroke="#52667a" stroke-width="1.2"/><line x1="154.1454" y1="452.1239" x2="187.2495" y2="350.6436" stroke="#52667a" stroke-width="1.2"/><line x1="187.2495" y1="350.6436" x2="153.7445" y2="302.8944" stroke="#52667a" stroke-width="1.2"/><line x1="153.7445" y1="302.8944" x2="36.0000" y2="300.2053" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="94.5554" y="376.5847" text-anchor="middle" dominant-baseline="central" fill="#fff">4</text><line x1="187.2495" y1="350.6436" x2="154.1454" y2="452.1239" stroke="#52667a" stroke-width="1.2"/><line x1="154.1454" y1="452.1239" x2="188.3219" y2="502.6563" stroke="#52667a" stroke-width="1.2"/><line x1="188.3219" y1="502.6563" x2="304.0693" y2="501.7705" stroke="#52667a" stroke-width="1.2"/><line x1="304.0693" y1="501.7705" x2="341.0024" y2="446.1164" stroke="#52667a" stroke-width="1.2"/><line x1="341.0024" y1="446.1164" x2="302.6696" y2="347.9129" stroke="#52667a" stroke-width="1.2"/><line x1="302.6696" y1="347.9129" x2="187.2495" y2="350.6436" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="246.8163" y="426.2541" text-anchor="middle" dominant-baseline="central" fill="#172b3a">5</text><line x1="337.3304" y1="292.0871" x2="302.6696" y2="347.9129" stroke="#52667a" stroke-width="1.2"/><line x1="302.6696" y1="347.9129" x2="341.0024" y2="446.1164" stroke="#52667a" stroke-width="1.2"/><line x1="341.0024" y1="446.1164" x2="451.7217" y2="446.7695" stroke="#52667a" stroke-width="1.2"/><line x1="451.7217" y1="446.7695" x2="486.2555" y2="337.1056" stroke="#52667a" stroke-width="1.2"/><line x1="486.2555" y1="337.1056" x2="452.7505" y2="289.3564" stroke="#52667a" stroke-width="1.2"/><line x1="452.7505" y1="289.3564" x2="337.3304" y2="292.0871" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="396.8260" y="367.6992" text-anchor="middle" dominant-baseline="central" fill="#172b3a">6</text><line x1="604.0000" y1="487.0390" x2="604.0000" y2="339.7947" stroke="#52667a" stroke-width="1.2"/><line x1="604.0000" y1="339.7947" x2="486.2555" y2="337.1056" stroke="#52667a" stroke-width="1.2"/><line x1="486.2555" y1="337.1056" x2="451.7217" y2="446.7695" stroke="#52667a" stroke-width="1.2"/><line x1="451.7217" y1="446.7695" x2="471.4980" y2="472.6249" stroke="#52667a" stroke-width="1.2"/><line x1="471.4980" y1="472.6249" x2="604.0000" y2="487.0390" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="542.0187" y="413.4212" text-anchor="middle" dominant-baseline="central" fill="#172b3a">7</text><line x1="36.0000" y1="152.9610" x2="36.0000" y2="300.2053" stroke="#52667a" stroke-width="1.2"/><line x1="36.0000" y1="300.2053" x2="153.7445" y2="302.8944" stroke="#52667a" stroke-width="1.2"/><line x1="153.7445" y1="302.8944" x2="188.2783" y2="193.2305" stroke="#52667a" stroke-width="1.2"/><line x1="188.2783" y1="193.2305" x2="168.5020" y2="167.3751" stroke="#52667a" stroke-width="1.2"/><line x1="168.5020" y1="167.3751" x2="36.0000" y2="152.9610" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="97.9813" y="226.5788" text-anchor="middle" dominant-baseline="central" fill="#fff">8</text><line x1="188.2783" y1="193.2305" x2="153.7445" y2="302.8944" stroke="#52667a" stroke-width="1.2"/><line x1="153.7445" y1="302.8944" x2="187.2495" y2="350.6436" stroke="#52667a" stroke-width="1.2"/><line x1="187.2495" y1="350.6436" x2="302.6696" y2="347.9129" stroke="#52667a" stroke-width="1.2"/><line x1="302.6696" y1="347.9129" x2="337.3304" y2="292.0871" stroke="#52667a" stroke-width="1.2"/><line x1="337.3304" y1="292.0871" x2="298.9976" y2="193.8836" stroke="#52667a" stroke-width="1.2"/><line x1="298.9976" y1="193.8836" x2="188.2783" y2="193.2305" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="243.1740" y="272.3008" text-anchor="middle" dominant-baseline="central" fill="#fff">9</text><line x1="335.9307" y1="138.2295" x2="298.9976" y2="193.8836" stroke="#52667a" stroke-width="1.2"/><line x1="298.9976" y1="193.8836" x2="337.3304" y2="292.0871" stroke="#52667a" stroke-width="1.2"/><line x1="337.3304" y1="292.0871" x2="452.7505" y2="289.3564" stroke="#52667a" stroke-width="1.2"/><line x1="452.7505" y1="289.3564" x2="485.8546" y2="187.8761" stroke="#52667a" stroke-width="1.2"/><line x1="485.8546" y1="187.8761" x2="451.6781" y2="137.3437" stroke="#52667a" stroke-width="1.2"/><line x1="451.6781" y1="137.3437" x2="335.9307" y2="138.2295" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="393.1837" y="213.7459" text-anchor="middle" dominant-baseline="central" fill="#fff">10</text><line x1="604.0000" y1="339.7947" x2="604.0000" y2="187.0366" stroke="#52667a" stroke-width="1.2"/><line x1="604.0000" y1="187.0366" x2="485.8546" y2="187.8761" stroke="#52667a" stroke-width="1.2"/><line x1="485.8546" y1="187.8761" x2="452.7505" y2="289.3564" stroke="#52667a" stroke-width="1.2"/><line x1="452.7505" y1="289.3564" x2="486.2555" y2="337.1056" stroke="#52667a" stroke-width="1.2"/><line x1="486.2555" y1="337.1056" x2="604.0000" y2="339.7947" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="545.4446" y="263.4153" text-anchor="middle" dominant-baseline="central" fill="#fff">11</text><line x1="188.8659" y1="36.0000" x2="36.0000" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><line x1="36.0000" y1="36.0000" x2="36.0000" y2="152.9610" stroke="#52667a" stroke-width="1.2"/><line x1="36.0000" y1="152.9610" x2="168.5020" y2="167.3751" stroke="#52667a" stroke-width="1.2"/><line x1="168.5020" y1="167.3751" x2="188.8659" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="112.3611" y="94.3927" text-anchor="middle" dominant-baseline="central" fill="#172b3a">12</text><line x1="299.3236" y1="36.0000" x2="188.8659" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><line x1="188.8659" y1="36.0000" x2="168.5020" y2="167.3751" stroke="#52667a" stroke-width="1.2"/><line x1="168.5020" y1="167.3751" x2="188.2783" y2="193.2305" stroke="#52667a" stroke-width="1.2"/><line x1="188.2783" y1="193.2305" x2="298.9976" y2="193.8836" stroke="#52667a" stroke-width="1.2"/><line x1="298.9976" y1="193.8836" x2="335.9307" y2="138.2295" stroke="#52667a" stroke-width="1.2"/><line x1="335.9307" y1="138.2295" x2="299.3236" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="244.1030" y="114.8134" text-anchor="middle" dominant-baseline="central" fill="#fff">13</text><line x1="484.7081" y1="36.0000" x2="299.3236" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><line x1="299.3236" y1="36.0000" x2="335.9307" y2="138.2295" stroke="#52667a" stroke-width="1.2"/><line x1="335.9307" y1="138.2295" x2="451.6781" y2="137.3437" stroke="#52667a" stroke-width="1.2"/><line x1="451.6781" y1="137.3437" x2="484.7081" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="392.0213" y="61.8457" text-anchor="middle" dominant-baseline="central" fill="#172b3a">14</text><line x1="604.0000" y1="187.0366" x2="604.0000" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><line x1="604.0000" y1="36.0000" x2="484.7081" y2="36.0000" stroke="#52667a" stroke-width="1.2"/><line x1="484.7081" y1="36.0000" x2="451.6781" y2="137.3437" stroke="#52667a" stroke-width="1.2"/><line x1="451.6781" y1="137.3437" x2="485.8546" y2="187.8761" stroke="#52667a" stroke-width="1.2"/><line x1="485.8546" y1="187.8761" x2="604.0000" y2="187.0366" stroke="#52667a" stroke-width="1.2"/><text class="n11-diagram-label" x="544.3651" y="111.4977" text-anchor="middle" dominant-baseline="central" fill="#fff">15</text><line x1="36" y1="36" x2="604" y2="36" stroke="#334155" stroke-width="2"/><line x1="604" y1="36" x2="604" y2="604" stroke="#334155" stroke-width="2"/><line x1="604" y1="604" x2="36" y2="604" stroke="#334155" stroke-width="2"/><line x1="36" y1="604" x2="36" y2="36" stroke="#334155" stroke-width="2"/></svg>
</div>
<figcaption><strong>Figure 3.</strong> Left: the sixteen closed Voronoi cells, drawn
from rational vertices bound by the
<a href="https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json">retained cover receipt</a>.
Right: the eleven occupied cell labels of
case 438. A highlighted cell specifies where a center may be; it is not a small
square or an owned inner hull. Shared cell boundaries remain in the proof.</figcaption>
</figure>

<figure>
<svg xmlns="http://www.w3.org/2000/svg" class="n11-diagram n11-capacity" width="301" height="311" viewBox="20 27 301 311" role="img" aria-labelledby="n11-capacity-title n11-capacity-desc"><title id="n11-capacity-title">One center per cell</title><desc id="n11-capacity-desc">Two hypothetical centers in exact cell 9 would have overlapping open radius-one-half disks. This illustrates the capacity lemma, not an actual packing.</desc><polygon data-capacity-cell="9" data-diameter-squared="196471698868229799711490263426870840158942905163933003300260799468114337241449583804816613/206619277667778980378105359478676124500000000000000000000000000000000000000000000000000000" points="112.830,96.987 77.845,208.083 111.788,256.456 228.715,253.690 263.828,197.135 224.995,97.649" fill="#e2e8f0" stroke="#52667a" stroke-width="2"/><circle data-hypothetical-center="0" cx="155.707" cy="162.997" r="100" fill="#1d7874" fill-opacity="0.12" stroke="#1d7874" stroke-width="2" stroke-dasharray="6 4"/><circle cx="155.707" cy="162.997" r="4" fill="#172b3a"/><circle data-hypothetical-center="1" cx="184.679" cy="202.172" r="100" fill="#1d7874" fill-opacity="0.12" stroke="#1d7874" stroke-width="2" stroke-dasharray="6 4"/><circle cx="184.679" cy="202.172" r="4" fill="#172b3a"/></svg>
<figcaption><strong>Figure 4.</strong> Why a center cell has capacity one. Two
hypothetical centers in the same cell would be less than one unit apart, so their open
radius-1/2 disks would overlap. Each disk lies inside its unit square, independent of
the square’s angle, so the squares’ interiors would overlap too. The selected cell,
cell 9, comes from the exact cover; the centers illustrate
the lemma and are not a candidate packing. The
<a href="https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_d4.py">cell checker</a>
proves the strict diameter bound for all sixteen closed cells.</figcaption>
</figure>

An eleven-square packing therefore chooses eleven different labels among sixteen.
There are

$$
\binom{16}{11}=4368
$$

possible subsets, called **masks**. A half-turn maps cell $j$ to cell $15-j$. No
eleven-element mask is fixed by this pairing, since a fixed mask would have even size.
Choosing one representative from each half-turn pair leaves 2,184 cases.
These representatives are sorted and numbered starting at zero.

The center-cover reduction permits every orientation.
For each square separately, write $t=\tan(\theta/2)$, with $0\le\theta\le\pi/2$. Then

$$
0\le t\le1,\qquad
\cos\theta=\frac{1-t^2}{1+t^2},\qquad
\sin\theta=\frac{2t}{1+t^2}.
$$

This rational parameterization makes interval calculations exact.
Both endpoints are retained, even though they describe the same square orientation.
Each certificate row covers a whole closed interval of $t$, not a sampled angle.

## One Geometric Invariant Supports the Certificates

Fix an occupied-cell pattern.
A **pose** is a square’s center and angle.
An **owner** is the square assigned to an occupied cell.
Although the packing is unknown, we can maintain two kinds of rigorous information about
each owner:

- An **outer pose cover** contains every center and angle still possible for that
  square. It consists of closed angle intervals with associated center polygons.
- An **owned hull** lies strictly inside that square in every valid packing under the
  current assumptions.
  It records points that the square must contain, even while its position is uncertain.

The first is an overestimate of possibilities; the second is a guaranteed interior.
In every valid packing under the current assumptions, each square’s pose belongs to its
outer cover and its interior contains its owned hull.
The outer cover may also retain artificial poses that no valid packing realizes.
The same invariant supports case exclusion and, later, capture near the construction.

### Removing poses that force overlap

Suppose another square must contain a small inner region.
A proposed position of our square is impossible if it forces their interiors to overlap.
We can reject a whole region of centers at once, provided the collision is guaranteed
for every angle in the row.
All other positions remain available until a further argument excludes them.

<figure>
<svg xmlns="http://www.w3.org/2000/svg" class="n11-diagram n11-mechanism-pose" width="740" height="312" viewBox="0 0 740 312" role="img" aria-labelledby="n11-mechanism-pose-title n11-mechanism-pose-desc"><title id="n11-mechanism-pose-title">Possible centers and guaranteed strict cores</title><desc id="n11-mechanism-pose-desc">Schematic of the ownership collision lemma. D and K minus Q are center-position regions; Q contains offsets relative to a square center. The implication concerns valid packings under accepted prior ownership and a whole-angle strict Q core.</desc><rect x="24" y="54" width="330" height="245" rx="8" fill="#f8fafc" stroke="#94a3b8"/><rect x="386" y="54" width="330" height="245" rx="8" fill="#f8fafc" stroke="#94a3b8"/><text class="n11-diagram-label" x="40.00" y="42.00" text-anchor="start" fill="#172b3a">Candidate center positions</text><text class="n11-diagram-label" x="402.00" y="42.00" text-anchor="start" fill="#172b3a">Offsets inside each physical square</text><path d="M65 220 L100 108 L278 105 L322 228 Z" fill="#dcebef" stroke="#1d7874" stroke-width="2"/><path d="M114 183 L155 135 L255 148 L274 212 L175 240 Z" fill="#f5bf65" fill-opacity=".65" stroke="#a15a00" stroke-width="2"/><circle cx="210" cy="189" r="5" fill="#172b3a"/><text class="n11-diagram-note" x="71.00" y="278.00" text-anchor="start" fill="#172b3a">D: possible centers</text><text class="n11-diagram-note" x="139.00" y="171.00" text-anchor="start" fill="#172b3a">K − Q</text><rect x="510" y="151" width="86" height="86" fill="#e2e8f0" stroke="#52667a" stroke-width="2"/><path d="M527 194 L553 168 L579 194 L553 220 Z" fill="#f5bf65" stroke="#a15a00" stroke-width="2"/><text class="n11-diagram-note" x="513.00" y="279.00" text-anchor="start" fill="#172b3a">Q: strict core offsets</text></svg>
<figcaption><strong>Figure 5.</strong> A schematic of one safe exclusion. A possible-center
region records uncertainty; a guaranteed inner region records what a valid packing must
contain. A translated strict core meeting the other square’s owned hull forces overlap:
if $x \in K - Q$, a core point meets the owned hull $K$. $Q$ stays strictly inside the
square throughout the angle row, $K$ is owned in every valid packing under the accepted
prior, and a shared interior forbids even a boundary center $x$.
The forbidden centers can be discarded, while the retained region remains an
overestimate. The drawing illustrates the
<a href="https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_generic_fresh.py">geometric checker’s</a>
invariant; it is not a certificate for the displayed schematic.</figcaption>
</figure>

For an angle interval, choose a convex core $Q$ around the origin that lies strictly
inside the centered unit square at every angle in the interval.
After substituting the half-angle formulas, the needed inequalities reduce to signs of
rational quadratic polynomials.
Checking endpoints and any interior minimum establishes the inequality over the entire
interval.

Let $K$ be an owned hull of another square.
A proposed center $x$ is forbidden if

$$
x\in K+(-Q)=\{k-q:k\in K,\ q\in Q\}.
$$

For such a center, $k=x+q$ belongs to both squares’ interiors.
This proves overlap.
The strict interior guarantees justify rejecting even the boundary of this closed
forbidden region.
If the cores merely touched the squares’ boundaries, the same rejection
could incorrectly remove a legal touching configuration.

<figure>
<svg xmlns="http://www.w3.org/2000/svg" class="n11-diagram n11-mechanism-row" width="740" height="614" viewBox="0 0 740 614" role="img" aria-labelledby="n11-mechanism-row-title n11-mechanism-row-desc"><title id="n11-mechanism-row-title">A source-bound owner-update row in case 2095</title><desc id="n11-mechanism-row-desc">Accepted case 2095, step 1, owner 10, row 17, closed half-angle interval 17/32 through 9/16. Field-scaled coordinates are used throughout. The legal center domain has six vertices, strict square-relative core has eight, and one tiny triangular residual remains. Three of ten reconstructed owned-hull Minkowski obstacles overlap this domain. Ownership promotion requires the complete angular cover, common-core and compression checks; this one row is an illustration.</desc><rect x="20" y="58" width="330" height="252" rx="8" fill="#f8fafc" stroke="#94a3b8"/><rect x="380" y="58" width="330" height="252" rx="8" fill="#f8fafc" stroke="#94a3b8"/><rect x="20" y="348" width="330" height="252" rx="8" fill="#f8fafc" stroke="#94a3b8"/><rect x="380" y="348" width="330" height="252" rx="8" fill="#f8fafc" stroke="#94a3b8"/><text class="n11-diagram-label" x="34.00" y="42.00" text-anchor="start" fill="#172b3a">1 · Possible centers</text><text class="n11-diagram-label" x="394.00" y="42.00" text-anchor="start" fill="#172b3a">2 · Core and owned hull</text><text class="n11-diagram-label" x="34.00" y="332.00" text-anchor="start" fill="#172b3a">3 · Forbidden centers</text><text class="n11-diagram-label" x="394.00" y="332.00" text-anchor="start" fill="#172b3a">4 · Retained triangle</text><polygon data-row-domain="2095-1-10-17" points="96.000,175.156 132.516,268.704 242.465,266.103 274.000,169.433 241.444,121.296 131.182,122.139" fill="#dcebef" fill-opacity="1.00" stroke="#203b50" stroke-width="2" stroke-linejoin="round"/><polygon  points="96.000,465.156 132.516,558.704 242.465,556.103 274.000,459.433 241.444,411.296 131.182,412.139" fill="#f8fafc" fill-opacity="1.00" stroke="#203b50" stroke-width="2" stroke-linejoin="round"/><polygon data-obstacle-owner="6" points="96.000,465.156 132.516,558.704 242.465,556.103 250.623,531.096 202.296,498.484 123.788,450.759 102.795,454.917" fill="#db7458" fill-opacity="0.45" stroke="#203b50" stroke-width="2" stroke-linejoin="round"/><polygon data-obstacle-owner="11" points="166.407,557.902 242.465,556.103 274.000,459.433 250.499,424.685 214.132,478.577 166.407,557.086" fill="#c98e33" fill-opacity="0.45" stroke="#203b50" stroke-width="2" stroke-linejoin="round"/><polygon data-obstacle-owner="14" points="103.486,453.875 134.193,474.597 212.701,522.322 264.078,446.189 264.534,445.437 241.444,411.296 131.182,412.139" fill="#b35f8d" fill-opacity="0.45" stroke="#203b50" stroke-width="2" stroke-linejoin="round"/><polygon data-residual-vertices="3" points="102.795,454.917 104.523,454.575 103.486,453.875" fill="#1d7874" fill-opacity="1.00" stroke="#203b50" stroke-width="2" stroke-linejoin="round"/><polygon data-core-vertices="8" points="498.472,185.184 526.393,204.026 555.184,221.528 574.026,193.607 591.528,164.816 563.607,145.974 534.816,128.472 515.974,156.393" fill="#f5bf65" fill-opacity="1.00" stroke="#203b50" stroke-width="2" stroke-linejoin="round"/><polygon data-prior-owner="11" points="506.518,261.003 527.935,271.086 554.397,280.595 586.356,259.661 583.479,249.801 558.164,233.338 526.687,244.325 506.518,253.756" fill="#dcebef" fill-opacity="1.00" stroke="#203b50" stroke-width="2" stroke-linejoin="round"/><text class="n11-diagram-note" x="393.00" y="295.00" text-anchor="start" fill="#172b3a">Q offsets; K₁₁ interior (zoom)</text><polygon data-residual-zoom="true" points="472.500,521.710 617.500,492.990 530.514,434.290" fill="#1d7874" fill-opacity="1.00" stroke="#203b50" stroke-width="2" stroke-linejoin="round"/><text class="n11-diagram-note" x="35.00" y="295.00" text-anchor="start" fill="#172b3a">D: field center region</text><text class="n11-diagram-note" x="35.00" y="585.00" text-anchor="start" fill="#172b3a">3 obstacles; 7 miss D</text><text class="n11-diagram-note" x="395.00" y="585.00" text-anchor="start" fill="#172b3a">Triangle magnified</text></svg>
<figcaption><strong>Figure 6.</strong> One accepted row: case 2095, step 1, owner 10,
row 17, over the complete interval $17/32 \le t \le 9/16$. The panels use retained exact
geometry, rounded only for display, and distinguish field center coordinates from
square-relative core offsets. This row is one of 32 in its update and
contributes one triangular residual to it. A complete
ownership update must also check every other row, closed angular coverage, common-core
inclusion and compression. The
<a href="https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/generic-mask2095-intake/full-result.json">accepted case result</a>
and <a href="https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_generic_fresh.py">independent checker</a>
supply the evidence: 5 complete updates exclude case 2095.
This is an excluded noncandidate case, not the case-438 capture.</figcaption>
</figure>

A stronger collision check compares a proposed pose against another square’s entire
possible pose cover.
It may exclude the proposal only when collision is forced for every partner row,
including the endpoints of its angle intervals.

### Keeping everything else

Removing a list of forbidden polygons is insufficient unless the remainder is accounted
for. After independently justified wall and self-containment cuts, each update checks
that the accepted predecessor domain is covered by verified forbidden regions together
with the retained residual regions.
A larger proposed domain may contain impossible points that those necessary cuts already
remove. Exact arrangement checks include segments, singleton points and zero-area
intersections.
An area sum alone cannot detect a missing segment where a touching packing
might live.

After the complete surviving angle cover has been checked, points that lie strictly
inside the square for every surviving pose can be used as new owned points.
The corresponding convex hull is also strictly inside.
These points can then constrain the other squares.
Initial owned points need their own proofs, using open inscribed disks, wall
inequalities or independently checked seeds.

**Pose-preservation lemma.** Starting from a valid outer cover and valid ownership, each
accepted update preserves every actual packing under its stated assumptions.
If an occupied square’s complete pose cover becomes empty, the case is impossible.
If two independently established owned hulls intersect, the two square interiors overlap
and the case is again impossible.[^geometry]

The order of updates matters.
A point cannot be used as owned before the check establishing its ownership.
Parent and child states must match, and parallel updates must refer to their declared
common prior. The certificate consumers check these dependencies as well as the local
inequalities.

## Charge Budgets Exclude Many Patterns at Once

The weighted-point idea becomes more selective when the occupied cells are known.
A field certificate specifies a charge function on strict inner cores.
It proves that a square centered in cell $i$ must receive charge at least $q_i$, unless
it would collide with an already proved owned hull.
In a legal packing the collision alternative is unavailable, so the charge lower bound
must hold.

One useful charge is defined by five sites.
For each projection direction, consider the median of the five projected sites.
A core receives charge one when its projection interval contains that median in every
direction. The certificate reduces this condition to finitely many direction
inequalities. For the square cores used by these field certificates, directions parallel
to the core’s axes and normals to site-pair lines divide the directions into sectors.
Within each sector the median site and the signs in the core’s support function stay
fixed, so the inequalities are linear in the direction normal; the bounding directions
suffice. This definition concerns median projections; it does not say that the core
contains three of the five sites.

Two disjoint strict cores cannot both receive that charge.
A strictly separating direction gives them disjoint projection intervals, which cannot
both contain the same median.
The charge therefore has capacity one.
A checked example forces the squares in two occupied cells each to receive charge one,
giving $2>1$. Owned-point collision regions help prove that each cell must be charged,
but those collision regions add nothing to the charge budget.[^field]

<figure>
<svg xmlns="http://www.w3.org/2000/svg" class="n11-diagram n11-mechanism-charge" width="740" height="466" viewBox="0 0 740 466" role="img" aria-labelledby="n11-mechanism-charge-title n11-mechanism-charge-desc"><title id="n11-mechanism-charge-title">A median projection capacity and a strict field budget</title><desc id="n11-mechanism-charge-desc">Upper panel is a schematic one-direction median projection. Lower panel quotes accepted canonical-mask-zero field data: required owners 0,1,2,3,6 are present in mask 0 through 10; charged cells 1 and 2 each carry charge one, exceeding budget one. The exact checker establishes the required all-direction statements.</desc><text class="n11-diagram-label" x="28.00" y="38.00" text-anchor="start" fill="#172b3a">A separating projection · capacity-one lemma</text><line x1="78" y1="150" x2="650" y2="150" stroke="#52667a" stroke-width="2"/><rect x="104" y="112" width="165" height="76" rx="8" fill="#dcebef" stroke="#1d7874" stroke-width="2"/><rect x="368" y="112" width="174" height="76" rx="8" fill="#f5dfb8" stroke="#a15a00" stroke-width="2"/><line x1="328" y1="92" x2="328" y2="217" stroke="#172b3a" stroke-width="2"/><text class="n11-diagram-label" x="186.00" y="139.00" text-anchor="middle" fill="#172b3a">core A</text><text class="n11-diagram-label" x="455.00" y="139.00" text-anchor="middle" fill="#172b3a">core B</text><text class="n11-diagram-note" x="328.00" y="239.00" text-anchor="middle" fill="#172b3a">median m</text><g transform="translate(0 -52)"><line x1="28" y1="322" x2="705" y2="322" stroke="#cbd5e1"/><text class="n11-diagram-label" x="28.00" y="358.00" text-anchor="start" fill="#172b3a">Accepted field example · canonical mask 0</text><text class="n11-diagram-label" x="28.00" y="393.00" text-anchor="start" fill="#172b3a">Required owners O = {0,1,2,3,6}</text><text class="n11-diagram-label" x="28.00" y="422.00" text-anchor="start" fill="#172b3a">Mask J = {0,…,10}; O ⊆ J</text><text class="n11-diagram-label" x="28.00" y="451.00" text-anchor="start" fill="#172b3a">Charged cells P ∩ J = {1,2}</text><text class="n11-diagram-label" x="28.00" y="480.00" text-anchor="start" fill="#172b3a">q₁ = q₂ = 1; budget b = 1</text><rect x="450" y="385" width="240" height="113" rx="9" fill="#dcebef" stroke="#1d7874" stroke-width="2"/><text class="n11-diagram-label" x="570.00" y="440.00" text-anchor="middle" fill="#172b3a">q₁ + q₂ = 2 &gt; 1 = b</text></g></svg>
<figcaption><strong>Figure 7.</strong> Median-projection charge as a capacity argument.
In a separating direction, two disjoint strict cores have disjoint projection
intervals, so both cannot contain the same median. Receiving charge one requires the
median condition in every direction; a single projection illustrates the capacity
argument, not that full test. Required owners and a strict excess over the budget are
necessary for the
<a href="https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/shared-field-mask0/summary.json">accepted field certificate</a>
to transfer to another mask. The exact checker certifies every required direction; the
drawing does not show three sites inside a core.</figcaption>
</figure>

Suppose the charge function has total capacity $b$ across disjoint cores.
A certificate may require certain owner cells $O$ to be present and assign lower bounds
to cells in a set $P$. It excludes a mask $J$ only when

$$
O\subseteq J,
\qquad
\sum_{i\in P\cap J}q_i>b.
$$

This explains why one checked certificate can exclude many masks.
The masks must contain its required owners, and each must satisfy the strict budget
inequality. Neither an equal budget nor an unsupported transfer to a larger mask
suffices.

The accepted exclusion inventory combines **1,904 cases excluded by field certificates
and 276 other cases**. Its conclusion is the exact set equality

$$
E=\{0,\ldots,2183\}\setminus\{438,999,1462,1659\}.
$$

The check compares case identities and dependencies, not only the number 2,180. The
publisher groups the same excluded set by provenance as $1931+76+173$. These are
different groupings of the same obligation, not different totals or additional
exclusions.[^exclusions]

Some exclusions have extra assumptions that must be discharged.
In particular, the symmetry cuts used in cases 2175 and 2176 depend on the original
1,931-case baseline.
They cannot use the final four-survivor reduction to prove its own premise.
Case 1383 requires both sides of a closed center split at $y_{13}=4/3$. Here
$y_{13}=p_y-U/2$ is the centered physical height of the square assigned to cell 13.
Those branches and their common parent remain part of the accepted proof, even though
the common geometric invariant lets us describe them briefly.

## Symmetry Reduces the Four Survivors to One

Rotating or reflecting the entire container preserves feasibility.
It is tempting to rotate the cell labels and declare the four surviving masks
equivalent, but the irregular Voronoi cover does not permit that shortcut.
A quarter-turn or reflection need not send a whole cell to another cell.

Instead, consider four views of each normalized center:

$$
(x,y),\quad(1-x,y),\quad(1-y,x),\quad(y,x).
$$

Together with half-turns these represent the eight symmetries of a square, usually
called $D_4$. Intersect the inverse images of the cells in the four views.
The result is a finite overlay of 220 nonempty closed regions: 212 polygons and eight
singleton points. A center in one overlay region has a specified allowable label in each
view.

<figure>
<svg xmlns="http://www.w3.org/2000/svg" class="n11-diagram n11-mechanism-symmetry" width="740" height="216" viewBox="0 50 740 216" role="img" aria-labelledby="n11-mechanism-symmetry-title n11-mechanism-symmetry-desc"><title id="n11-mechanism-symmetry-title">Four point views on a fixed irregular cell cover</title><desc id="n11-mechanism-symmetry-desc">The same exact rational point from retained D4 overlay region 9 has fixed-cover cell labels 0,7,3,5 under four coordinate views.</desc><rect x="28" y="66" width="156" height="156" fill="#f8fafc" stroke="#94a3b8"/><polygon data-view="0" data-cell="0" points="36.000,214.000 65.403,214.000 73.544,189.021 65.120,176.566 36.000,176.773" fill="#dcebef" fill-opacity="1.00" stroke="#1d7874" stroke-width="2" stroke-linejoin="round"/><polygon data-view="0" data-cell="1" points="65.403,214.000 111.096,214.000 102.073,188.803 73.544,189.021" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="0" data-cell="2" points="102.073,188.803 111.096,214.000 138.322,214.000 143.341,181.619 138.467,175.246 111.177,175.085" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="0" data-cell="3" points="138.322,214.000 176.000,214.000 176.000,185.172 143.341,181.619" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="0" data-cell="4" points="36.000,176.773 65.120,176.566 73.280,151.553 65.022,139.784 36.000,139.121" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="0" data-cell="5" points="65.120,176.566 73.544,189.021 102.073,188.803 111.177,175.085 101.728,150.880 73.280,151.553" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="0" data-cell="6" points="101.728,150.880 111.177,175.085 138.467,175.246 146.978,148.216 138.720,136.447 110.272,137.120" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="0" data-cell="7" points="138.467,175.246 143.341,181.619 176.000,185.172 176.000,148.879 146.978,148.216" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="0" data-cell="8" points="36.000,139.121 65.022,139.784 73.533,112.754 68.659,106.381 36.000,102.828" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="0" data-cell="9" points="65.022,139.784 73.280,151.553 101.728,150.880 110.272,137.120 100.823,112.915 73.533,112.754" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="0" data-cell="10" points="100.823,112.915 110.272,137.120 138.720,136.447 146.880,111.434 138.456,98.979 109.927,99.197" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="0" data-cell="11" points="138.720,136.447 146.978,148.216 176.000,148.879 176.000,111.227 146.880,111.434" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="0" data-cell="12" points="36.000,102.828 68.659,106.381 73.678,74.000 36.000,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="0" data-cell="13" points="68.659,106.381 73.533,112.754 100.823,112.915 109.927,99.197 100.904,74.000 73.678,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="0" data-cell="14" points="100.904,74.000 109.927,99.197 138.456,98.979 146.597,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="0" data-cell="15" points="138.456,98.979 146.880,111.434 176.000,111.227 176.000,74.000 146.597,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><circle data-view-point="0" cx="68.310" cy="181.369" r="5" fill="#a15a00"/><text class="n11-diagram-label" x="106.00" y="247.00" text-anchor="middle" fill="#172b3a">view 1: cell 0</text><rect x="202" y="66" width="156" height="156" fill="#f8fafc" stroke="#94a3b8"/><polygon data-view="1" data-cell="0" points="210.000,214.000 239.403,214.000 247.544,189.021 239.120,176.566 210.000,176.773" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="1" data-cell="1" points="239.403,214.000 285.096,214.000 276.073,188.803 247.544,189.021" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="1" data-cell="2" points="276.073,188.803 285.096,214.000 312.322,214.000 317.341,181.619 312.467,175.246 285.177,175.085" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="1" data-cell="3" points="312.322,214.000 350.000,214.000 350.000,185.172 317.341,181.619" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="1" data-cell="4" points="210.000,176.773 239.120,176.566 247.280,151.553 239.022,139.784 210.000,139.121" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="1" data-cell="5" points="239.120,176.566 247.544,189.021 276.073,188.803 285.177,175.085 275.728,150.880 247.280,151.553" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="1" data-cell="6" points="275.728,150.880 285.177,175.085 312.467,175.246 320.978,148.216 312.720,136.447 284.272,137.120" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="1" data-cell="7" points="312.467,175.246 317.341,181.619 350.000,185.172 350.000,148.879 320.978,148.216" fill="#dcebef" fill-opacity="1.00" stroke="#1d7874" stroke-width="2" stroke-linejoin="round"/><polygon data-view="1" data-cell="8" points="210.000,139.121 239.022,139.784 247.533,112.754 242.659,106.381 210.000,102.828" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="1" data-cell="9" points="239.022,139.784 247.280,151.553 275.728,150.880 284.272,137.120 274.823,112.915 247.533,112.754" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="1" data-cell="10" points="274.823,112.915 284.272,137.120 312.720,136.447 320.880,111.434 312.456,98.979 283.927,99.197" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="1" data-cell="11" points="312.720,136.447 320.978,148.216 350.000,148.879 350.000,111.227 320.880,111.434" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="1" data-cell="12" points="210.000,102.828 242.659,106.381 247.678,74.000 210.000,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="1" data-cell="13" points="242.659,106.381 247.533,112.754 274.823,112.915 283.927,99.197 274.904,74.000 247.678,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="1" data-cell="14" points="274.904,74.000 283.927,99.197 312.456,98.979 320.597,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="1" data-cell="15" points="312.456,98.979 320.880,111.434 350.000,111.227 350.000,74.000 320.597,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><circle data-view-point="1" cx="317.690" cy="181.369" r="5" fill="#a15a00"/><text class="n11-diagram-label" x="280.00" y="247.00" text-anchor="middle" fill="#172b3a">view 2: cell 7</text><rect x="376" y="66" width="156" height="156" fill="#f8fafc" stroke="#94a3b8"/><polygon data-view="2" data-cell="0" points="384.000,214.000 413.403,214.000 421.544,189.021 413.120,176.566 384.000,176.773" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="2" data-cell="1" points="413.403,214.000 459.096,214.000 450.073,188.803 421.544,189.021" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="2" data-cell="2" points="450.073,188.803 459.096,214.000 486.322,214.000 491.341,181.619 486.467,175.246 459.177,175.085" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="2" data-cell="3" points="486.322,214.000 524.000,214.000 524.000,185.172 491.341,181.619" fill="#dcebef" fill-opacity="1.00" stroke="#1d7874" stroke-width="2" stroke-linejoin="round"/><polygon data-view="2" data-cell="4" points="384.000,176.773 413.120,176.566 421.280,151.553 413.022,139.784 384.000,139.121" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="2" data-cell="5" points="413.120,176.566 421.544,189.021 450.073,188.803 459.177,175.085 449.728,150.880 421.280,151.553" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="2" data-cell="6" points="449.728,150.880 459.177,175.085 486.467,175.246 494.978,148.216 486.720,136.447 458.272,137.120" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="2" data-cell="7" points="486.467,175.246 491.341,181.619 524.000,185.172 524.000,148.879 494.978,148.216" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="2" data-cell="8" points="384.000,139.121 413.022,139.784 421.533,112.754 416.659,106.381 384.000,102.828" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="2" data-cell="9" points="413.022,139.784 421.280,151.553 449.728,150.880 458.272,137.120 448.823,112.915 421.533,112.754" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="2" data-cell="10" points="448.823,112.915 458.272,137.120 486.720,136.447 494.880,111.434 486.456,98.979 457.927,99.197" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="2" data-cell="11" points="486.720,136.447 494.978,148.216 524.000,148.879 524.000,111.227 494.880,111.434" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="2" data-cell="12" points="384.000,102.828 416.659,106.381 421.678,74.000 384.000,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="2" data-cell="13" points="416.659,106.381 421.533,112.754 448.823,112.915 457.927,99.197 448.904,74.000 421.678,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="2" data-cell="14" points="448.904,74.000 457.927,99.197 486.456,98.979 494.597,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="2" data-cell="15" points="486.456,98.979 494.880,111.434 524.000,111.227 524.000,74.000 494.597,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><circle data-view-point="2" cx="491.369" cy="181.690" r="5" fill="#a15a00"/><text class="n11-diagram-label" x="454.00" y="247.00" text-anchor="middle" fill="#172b3a">view 3: cell 3</text><rect x="550" y="66" width="156" height="156" fill="#f8fafc" stroke="#94a3b8"/><polygon data-view="3" data-cell="0" points="558.000,214.000 587.403,214.000 595.544,189.021 587.120,176.566 558.000,176.773" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="3" data-cell="1" points="587.403,214.000 633.096,214.000 624.073,188.803 595.544,189.021" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="3" data-cell="2" points="624.073,188.803 633.096,214.000 660.322,214.000 665.341,181.619 660.467,175.246 633.177,175.085" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="3" data-cell="3" points="660.322,214.000 698.000,214.000 698.000,185.172 665.341,181.619" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="3" data-cell="4" points="558.000,176.773 587.120,176.566 595.280,151.553 587.022,139.784 558.000,139.121" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="3" data-cell="5" points="587.120,176.566 595.544,189.021 624.073,188.803 633.177,175.085 623.728,150.880 595.280,151.553" fill="#dcebef" fill-opacity="1.00" stroke="#1d7874" stroke-width="2" stroke-linejoin="round"/><polygon data-view="3" data-cell="6" points="623.728,150.880 633.177,175.085 660.467,175.246 668.978,148.216 660.720,136.447 632.272,137.120" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="3" data-cell="7" points="660.467,175.246 665.341,181.619 698.000,185.172 698.000,148.879 668.978,148.216" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="3" data-cell="8" points="558.000,139.121 587.022,139.784 595.533,112.754 590.659,106.381 558.000,102.828" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="3" data-cell="9" points="587.022,139.784 595.280,151.553 623.728,150.880 632.272,137.120 622.823,112.915 595.533,112.754" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="3" data-cell="10" points="622.823,112.915 632.272,137.120 660.720,136.447 668.880,111.434 660.456,98.979 631.927,99.197" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="3" data-cell="11" points="660.720,136.447 668.978,148.216 698.000,148.879 698.000,111.227 668.880,111.434" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="3" data-cell="12" points="558.000,102.828 590.659,106.381 595.678,74.000 558.000,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="3" data-cell="13" points="590.659,106.381 595.533,112.754 622.823,112.915 631.927,99.197 622.904,74.000 595.678,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="3" data-cell="14" points="622.904,74.000 631.927,99.197 660.456,98.979 668.597,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><polygon data-view="3" data-cell="15" points="660.456,98.979 668.880,111.434 698.000,111.227 698.000,74.000 668.597,74.000" fill="#f8fafc" fill-opacity="1.00" stroke="#cbd5e1" stroke-width="2" stroke-linejoin="round"/><circle data-view-point="3" cx="590.631" cy="181.690" r="5" fill="#a15a00"/><text class="n11-diagram-label" x="628.00" y="247.00" text-anchor="middle" fill="#172b3a">view 4: cell 5</text></svg>
<figcaption><strong>Figure 8.</strong> Four views of a center against the fixed cell
cover. The point changes position under square symmetries; the irregular cell polygons
are not permuted by those transformations. An overlay region records the allowed
cell labels in every view. One strict distance ban, for illustration: the maximum
squared physical center distance of overlay regions 9 and 12 is below 1.
This illustration explains the construction used by the
<a href="https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json">accepted symmetry check</a>;
its exhaustive assignment search, including boundary ties and strict distance bans,
is a separate obligation, over 220 closed regions and 1,572 bans.</figcaption>
</figure>

For two overlay regions, exact vertex calculations sometimes prove that every pair of
points, one in each region, is less than one unit apart in physical coordinates.
Such a pair cannot contain two centers.
The check retains 1,572 strict distance bans; a distance equal to one is not banned.

**Symmetry lemma.** Once the 2,180 exclusions hold, some square symmetry of every
remaining packing admits case 438. To prove this, suppose every view avoids 438 and its
half-turn. Each view must then have a mask from the other three candidates and their
half-turns. Exhaustive finite enumeration tries the compatible overlay assignments,
requiring distinct occupied labels in each view and respecting all distance bans.
None exists.[^symmetry]

Every genuine packing would supply such an assignment by choosing containing closed
cells in each view. Their nonexistence proves the lemma, including all boundary ties.
The enumeration may allow geometric arrangements that no real packing realizes; that
only makes its impossibility conclusion stronger.

## Capture Forces Case 438 Near the Construction

Case 438 specifies the occupied cells

$$
\{0,1,2,3,4,8,9,10,11,13,15\}.
$$

The pose-preservation invariant now serves a different purpose.
Rather than emptying every pose domain, the checks progressively enclose surviving poses
near the exact construction.
Initial ownership, fourteen root rounds and the subsequent capture graph are all
verified before the local theorem is invoked.

Three closed splits produce four possibilities.
Here square subscripts denote owner-cell labels; $y_{15}$ is a centered physical height
and $t_i$ is the half-angle parameter of the square assigned to cell $i$.

| Branch assumptions | Checked conclusion |
| --- | --- |
| $y_{15}\le5/4$ | Contradiction |
| $y_{15}\ge5/4$, $t_{13}\le147/512$ | Contradiction |
| $y_{15}\ge5/4$, $t_{13}\ge147/512$, $t_2\le183/512$ | Contradiction |
| $y_{15}\ge5/4$, $t_{13}\ge147/512$, $t_2\ge183/512$ | Enclosure in the local neighborhood |

Equality belongs to both sides of every split.
The overlap is harmless and prevents a missing boundary branch.

<figure>
<svg xmlns="http://www.w3.org/2000/svg" class="n11-diagram n11-capture" width="840" height="676" viewBox="0 0 840 676" role="img" aria-labelledby="n11-capture-title n11-capture-desc"><title id="n11-capture-title">The closed case-438 capture tree</title><desc id="n11-capture-desc">The accepted ten-node source-parent tree ends at three contradiction leaves and one near leaf discharged by pose inclusion and local isolation. This is a dependency diagram, not a drawing of the geometric search domains.</desc><line x1="283.8" y1="70" x2="100.0" y2="170" stroke="#94a3b8" stroke-width="2.5"/><line x1="283.8" y1="70" x2="467.5" y2="170" stroke="#94a3b8" stroke-width="2.5"/><line x1="467.5" y1="170" x2="310.0" y2="270" stroke="#94a3b8" stroke-width="2.5"/><line x1="310.0" y1="270" x2="310.0" y2="370" stroke="#94a3b8" stroke-width="2.5"/><line x1="467.5" y1="170" x2="625.0" y2="270" stroke="#94a3b8" stroke-width="2.5"/><line x1="625.0" y1="270" x2="625.0" y2="370" stroke="#94a3b8" stroke-width="2.5"/><line x1="625.0" y1="370" x2="520.0" y2="470" stroke="#94a3b8" stroke-width="2.5"/><line x1="625.0" y1="370" x2="730.0" y2="470" stroke="#94a3b8" stroke-width="2.5"/><line x1="730.0" y1="470" x2="730.0" y2="570" stroke="#94a3b8" stroke-width="2.5"/><text class="n11-diagram-note" data-closed-cut="y₁₅ ≤ 5/4" x="273.8" y="120.0" text-anchor="end" fill="#172b3a" stroke="white" stroke-width="7" stroke-linejoin="round" paint-order="stroke">y₁₅ ≤ 5/4</text><text class="n11-diagram-note" data-closed-cut="y₁₅ ≥ 5/4" x="293.8" y="120.0" text-anchor="start" fill="#172b3a" stroke="white" stroke-width="7" stroke-linejoin="round" paint-order="stroke">y₁₅ ≥ 5/4</text><text class="n11-diagram-note" data-closed-cut="t₁₃ ≤ 147/512" x="457.5" y="220.0" text-anchor="end" fill="#172b3a" stroke="white" stroke-width="7" stroke-linejoin="round" paint-order="stroke">t₁₃ ≤ 147/512</text><text class="n11-diagram-note" data-closed-cut="t₁₃ ≥ 147/512" x="477.5" y="220.0" text-anchor="start" fill="#172b3a" stroke="white" stroke-width="7" stroke-linejoin="round" paint-order="stroke">t₁₃ ≥ 147/512</text><text class="n11-diagram-note" data-closed-cut="t₂ ≤ 183/512" x="615.0" y="420.0" text-anchor="end" fill="#172b3a" stroke="white" stroke-width="7" stroke-linejoin="round" paint-order="stroke">t₂ ≤ 183/512</text><text class="n11-diagram-note" data-closed-cut="t₂ ≥ 183/512" x="635.0" y="420.0" text-anchor="start" fill="#172b3a" stroke="white" stroke-width="7" stroke-linejoin="round" paint-order="stroke">t₂ ≥ 183/512</text><rect x="44.0" y="146.0" width="112" height="48" rx="12" fill="#fce9e7" stroke="#52667a" stroke-width="1.5"/><text class="n11-diagram-label" x="100.0" y="175.0" text-anchor="middle" fill="#17324a">far15</text><text class="n11-diagram-note" x="100.0" y="213.0" text-anchor="middle" fill="#34465a">contradiction</text><rect x="254.0" y="346.0" width="112" height="48" rx="12" fill="#fce9e7" stroke="#52667a" stroke-width="1.5"/><text class="n11-diagram-label" x="310.0" y="375.0" text-anchor="middle" fill="#17324a">far13</text><text class="n11-diagram-note" x="310.0" y="413.0" text-anchor="middle" fill="#34465a">contradiction</text><rect x="254.0" y="246.0" width="112" height="48" rx="12" fill="#e9eff7" stroke="#52667a" stroke-width="1.5"/><text class="n11-diagram-label" x="310.0" y="275.0" text-anchor="middle" fill="#17324a">r10</text><rect x="464.0" y="446.0" width="112" height="48" rx="12" fill="#fce9e7" stroke="#52667a" stroke-width="1.5"/><text class="n11-diagram-label" x="520.0" y="475.0" text-anchor="middle" fill="#17324a">far2</text><text class="n11-diagram-note" x="520.0" y="513.0" text-anchor="middle" fill="#34465a">contradiction</text><rect x="674.0" y="546.0" width="112" height="48" rx="12" fill="#e4f3ee" stroke="#52667a" stroke-width="1.5"/><text class="n11-diagram-label" x="730.0" y="575.0" text-anchor="middle" fill="#17324a">near</text><text class="n11-diagram-note" x="730.0" y="613.0" text-anchor="middle" fill="#34465a">local enclosure</text><rect x="674.0" y="446.0" width="112" height="48" rx="12" fill="#e9eff7" stroke="#52667a" stroke-width="1.5"/><text class="n11-diagram-label" x="730.0" y="475.0" text-anchor="middle" fill="#17324a">r111</text><rect x="569.0" y="346.0" width="112" height="48" rx="12" fill="#e9eff7" stroke="#52667a" stroke-width="1.5"/><text class="n11-diagram-label" x="625.0" y="375.0" text-anchor="middle" fill="#17324a">r11</text><rect x="569.0" y="246.0" width="112" height="48" rx="12" fill="#e9eff7" stroke="#52667a" stroke-width="1.5"/><text class="n11-diagram-label" x="625.0" y="275.0" text-anchor="middle" fill="#17324a">near13</text><rect x="411.5" y="146.0" width="112" height="48" rx="12" fill="#e9eff7" stroke="#52667a" stroke-width="1.5"/><text class="n11-diagram-label" x="467.5" y="175.0" text-anchor="middle" fill="#17324a">r1</text><rect x="227.8" y="46.0" width="112" height="48" rx="12" fill="#e9eff7" stroke="#52667a" stroke-width="1.5"/><text class="n11-diagram-label" x="283.8" y="75.0" text-anchor="middle" fill="#17324a">root</text><text class="n11-diagram-note" x="730.0" y="638.0" text-anchor="middle" fill="#34465a">fixed-T theorem follows</text></svg>
<figcaption><strong>Figure 9.</strong> The accepted ten-node capture ancestry.
Intermediate nodes propagate a checked state; three far leaves end in contradiction
and the near leaf encloses every surviving pose. Edges denote proof dependencies,
not trajectories of moving squares. Here $y_{15} = p_y - U/2$ is a physical centered height
and $t_i = \tan(\theta_i/2)$ is an owner’s half-angle parameter.
Edge labels give each new closed split condition;
the branch table collects the inherited conditions. Both sides retain equality.
The near leaf is an enclosure; the fixed-T local theorem is still needed.
The fourteen root rounds precede the descendants shown here; the descendants’ parent
edges are bound by the
<a href="https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json">accepted source graph</a>.</figcaption>
</figure>

The final near state contains 136 live closed angular rows and 1,542 center vertices.
The inclusion checker proves that all their center polygons and all their angle
intervals lie inside the same local rectangle.
Convexity extends center bounds from vertices to whole polygons.
Exact bounds for $2\arctan(t)$ convert interval endpoints to angular displacements in
radians; intervals near the quarter-turn seam use the chart change $(t-1)/(t+1)$. A
half-angle parameter is never substituted for a radian angle.
The accepted ten nodes and nine parent edges bind this enclosure to the original
unconditional case, rather than to an assumed favorable starting pose.[^capture]

## The Local Argument Excludes Every Nonzero Motion

Fix the container as $[0,T]^2$ and label the eleven squares as in the exact
construction. A perturbation has 33 coordinates:

$$
h=(\Delta x_0,\Delta y_0,\Delta\theta_0,\ldots,
\Delta x_{10},\Delta y_{10},\Delta\theta_{10}).
$$

The checked local neighborhood is a rectangle $|h_j|\le r_j$, with positive coordinate
radii $r_j$. Different coordinates have different radii, allowing the rectangle to fit
the captured domains.
All radii lie within the analytic working box of radius $1/64$.

The local theorem excludes any nonzero displacement in this rectangle that remains
feasible in the fixed-$T$ container.
Its mechanism is quantitative: the linear gap constraints obstruct motion, and an exact
bound on their curvature proves that the nonlinear terms cannot overcome that
obstruction anywhere in the rectangle.

Write $\tau$ for the largest displacement as a fraction of its allowed coordinate
radius. A nonzero displacement has $0<\tau\le1$. The certificate for a coordinate
attaining that maximum forces $\tau\le c_j\tau^2$, with $c_j<1$. This is impossible:
throughout that interval, $c_j\tau^2<\tau$.

<figure>
<svg xmlns="http://www.w3.org/2000/svg" class="n11-diagram n11-local" width="760" height="324" viewBox="0 80 760 324" role="img" aria-labelledby="n11-local-title n11-local-desc"><title id="n11-local-title">A nonzero displacement cannot satisfy the fixed-T local inequality</title><desc id="n11-local-desc">Algebraic schematic of y equal to tau and y equal to c tau squared on zero to one. The latter stays strictly below the former because the accepted fixed-T local checker proves c is below one for every signed-coordinate branch. The drawn curve uses the largest exact accepted ratio only for display; the complete 8,448 exact margins prove the result. This is not a projection of the 33-dimensional pose space or a global uniqueness claim.</desc><path d="M104 100V350H660" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><path d="M104 350L660 100" fill="none" stroke="var(--kpress-doc-text)" stroke-width="3"/><polyline points="104,350 121,350 139,349 156,349 174,347 191,346 208,344 226,342 243,339 260,337 278,333 295,330 312,326 330,322 347,318 365,313 382,308 399,302 417,296 434,290 452,284 469,277 486,270 504,263 521,255 538,247 556,238 573,230 590,221 608,211 625,201 643,191 660,181" fill="none" stroke="var(--kpress-doc-accent)" data-accepted-ratio="30315723733143223399760381935768897915102781/44812254755124354970141130383955000000000000" stroke-width="3" stroke-dasharray="8 5"/><text class="n11-diagram-label" x="539" y="113" text-anchor="middle" fill="var(--kpress-doc-text)">τ</text><text class="n11-diagram-label" x="556" y="246" text-anchor="middle" fill="var(--kpress-doc-text)">cτ²</text><text class="n11-diagram-note" x="104" y="385" text-anchor="middle" fill="var(--kpress-doc-text)">0</text><text class="n11-diagram-note" x="660" y="385" text-anchor="middle" fill="var(--kpress-doc-text)">1</text></svg>
<figcaption><strong>Figure 10.</strong> The local contradiction. The upper line is
$\tau$ and the lower curve is $c\tau^2$, with a coefficient $c$ below one, on
$0 < \tau \le 1$. A feasible nonzero displacement would require the line to lie at or
below the curve, so there is none. This is an
algebraic illustration of the
<a href="https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json">accepted exact inequalities</a>,
8,448 exact margins over 128 branches,
not a projection of the 33-dimensional feasible set. The theorem applies in the checked
rectangle inside the fixed side-T container, which capture and inclusion reach first.</figcaption>
</figure>

### Covering all possible local contact patterns

Nearby squares can change which edges separate them, so the proof must consider more
than one contact pattern.
The construction has fourteen contacting pairs.
Each pair has eight possible separation features: choose which square supplies the axis,
one of its two edge-normal directions, and a separation order.
There are 112 features altogether.
Exact signs show 24 available at the construction and 88 unavailable.
Taylor bounds prove that those 88 remain unavailable throughout the full rectangle.

For the remaining features, the check enumerates 512 raw choices, reducing identical
derivative systems to 128 branches.
Each has 42 necessary tied inequalities, including wall inequalities.
Omitting the constraints of pairs that do not touch at the construction weakens this
necessary system; it cannot discard a feasible packing.
Conversely, every feasible perturbation must select one of the checked branches.[^local]

### From a linear obstruction to a finite neighborhood

Let $g_i(h)$ be a gap that must be nonnegative in a chosen branch, with $g_i(0)=0$.
Write its linear part as $A_i h$. A linear calculation alone would describe only
infinitesimal motion.
To control an actual displacement, the proof bounds the quadratic remainder.

Normalize the size of a hypothetical nonzero displacement by

$$
\tau=\max_j\frac{|h_j|}{r_j},\qquad 0<\tau\le1,
\qquad R=\max_j r_j.
$$

The checked curvature bounds $K_i$ give the necessary inequalities

$$
A_i h\ge-\frac{\tau^2K_i}{2}.
$$

Choose a coordinate $j$ attaining $|h_j|=\tau r_j$, and choose the sign $\sigma$
opposite to $h_j$. A certificate supplies nonnegative rational weights $\lambda_i$ such
that

$$
\left\|\lambda^{\top}A-\sigma e_j^{\top}\right\|_1
\le\epsilon_j.
$$

Here $e_j$ selects coordinate $j$, and the norm sums absolute coefficient errors.
The weighted combination nearly isolates $\sigma h_j=-\tau r_j$. Its residual
contributes at most $\epsilon_j\tau R$. Multiplying the gap inequalities by the
nonnegative weights yields

$$
\tau r_j\le\epsilon_j\tau R+\frac{\tau^2M_j}{2},
\qquad M_j=\sum_i\lambda_iK_i.
$$

Every one of the $128\times33\times2=8,448$ certificates verifies the strict margin

$$
M_j<2(r_j-\epsilon_jR).
$$

The quantity $2(r_j-\epsilon_jR)$ is positive.
Rearranging gives

$$
\tau\le c_j\tau^2,
\qquad
c_j=\frac{M_j}{2(r_j-\epsilon_jR)}<1.
$$

This is impossible for $0<\tau\le1$: dividing by $\tau$ would give $1\le c_j\tau<1$. The
largest certified ratio is approximately $0.676505208$; the proof uses exact strict
comparisons, not this rounded display value.

**Local-isolation lemma.** The zero perturbation is the only feasible packing in the
declared labeled rectangle inside the fixed container $[0,T]^2$. The quadratic bounds
make this a theorem about a finite neighborhood, including its boundary.
Appendix B describes the curvature and negative-feature checks.

## Closing the Gap Between the Rational Cap and the Exact Optimum

The global geometry was computed at $U>T$, while isolation holds at the exact side $T$.
The conclusion needs a precise connection between the two frames.

Some certificates use field coordinates $p_f=Bp$, where

$$
L=191/50,\qquad B=L/U.
$$

In that frame the container has side $L$ and each small square has side $B$. This is a
change of coordinates; it is not a claim that eleven unit squares fit in a side-$L$
square.

Let $Q(x,y)=(-y,x)$ be the checked quarter-turn; undo it to align the captured case with
the construction. The local center corresponding to a field center is

$$
p_T=Q^{-1}\!\left(\frac{p_f}{B}-(U/2,U/2)\right)+(T/2,T/2).
$$

After undoing the field scale, this is a rigid rotation and translation.
An original side-$S$ container centered inside $U$ becomes

$$
[(T-S)/2,(T+S)/2]^2\subset[0,T]^2
\qquad(S<T).
$$

Its small squares are still unit squares.
The complete capture and inclusion checks place their labeled poses in the local
rectangle, and they are feasible in the fixed-$T$ container.
The local-isolation lemma forces them to be the exact construction.
But that construction spans $T$, so it cannot lie in a square of side $S<T$. This
contradiction excludes every smaller side directly.
Together with the exact witness, it proves $s(11)=T$.[^endpoint]

<figure>
<svg xmlns="http://www.w3.org/2000/svg" class="n11-diagram n11-endpoint" width="900" height="482" viewBox="0 78 900 482" role="img" aria-labelledby="n11-endpoint-title n11-endpoint-desc"><title id="n11-endpoint-title">Why a smaller container contradicts the exact witness span</title><desc id="n11-endpoint-desc">A hypothetical packing P in side S less than T is centered inside the larger rational cap U. Undoing the field coordinate conversion and then rigidly aligning it places the same physical unit squares inside the fixed-T container. Checked capture and pose inclusion put P in the local rectangle, where the fixed-T local theorem forces the exact Trump witness. That witness spans T in both directions, so it cannot fit inside side S. The drawn container gaps are schematic and not to scale; no claim of uniqueness for all optimal packings is made.</desc><rect x="65" y="118" width="260" height="260" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><rect x="105" y="158" width="180" height="180" fill="none" stroke="var(--kpress-doc-accent)" stroke-width="3" stroke-dasharray="8 5"/><text class="n11-diagram-label" x="195" y="109" text-anchor="middle" fill="var(--kpress-doc-text)">Rational cap U &gt; T</text><text class="n11-diagram-label" x="195" y="256" text-anchor="middle" fill="var(--kpress-doc-text)">packing in S &lt; T</text><path d="M345 243h185" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><path d="M520 235l12 8-12 8" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><text class="n11-diagram-note" x="437" y="187" text-anchor="middle" fill="var(--kpress-doc-text)">Undo field frame B</text><text class="n11-diagram-note" x="437" y="216" text-anchor="middle" fill="var(--kpress-doc-text)">rigidly align</text><text class="n11-diagram-note" x="437" y="286" text-anchor="middle" fill="var(--kpress-doc-text)">No physical shrinking</text><rect x="575" y="118" width="260" height="260" fill="none" stroke="var(--kpress-doc-text)" stroke-width="2"/><rect x="615" y="158" width="180" height="180" fill="none" stroke="var(--kpress-doc-accent)" stroke-width="3" stroke-dasharray="8 5"/><text class="n11-diagram-label" x="705" y="109" text-anchor="middle" fill="var(--kpress-doc-text)">Fixed-T container</text><text class="n11-diagram-label" x="705" y="256" text-anchor="middle" fill="var(--kpress-doc-text)">same packing</text><text class="n11-diagram-note" x="450" y="419" text-anchor="middle" fill="var(--kpress-doc-text)">Capture + inclusion locate packing</text><path d="M450 430v20" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><path d="M443 444l7 8 7-8" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><text class="n11-diagram-label" x="450" y="477" text-anchor="middle" fill="var(--kpress-doc-text)">Fixed-T local theorem forces witness</text><path d="M450 488v20" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><path d="M443 502l7 8 7-8" fill="none" stroke="var(--kpress-doc-muted)" stroke-width="2"/><text class="n11-diagram-label" x="450" y="538" text-anchor="middle" fill="var(--kpress-doc-text)">Witness spans T &gt; S: contradiction</text></svg>
<figcaption><strong>Figure 11.</strong> Why the rational cap settles the exact endpoint.
The same hypothetical side-S container, with $S < T$, fits concentrically inside the cap
and then inside the fixed side-T container after the checked rigid alignment. Its
unit squares keep their size. Capture and
<a href="https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json">pose inclusion</a>
put the packing in the local rectangle; isolation forces the construction, whose span
T contradicts its containment in side S. Gaps are exaggerated for visibility;
the drawing does not depict a feasible smaller packing.</figcaption>
</figure>

This deduction does not rule out perturbations in the larger cap $U$. It needs only the
impossibility of a smaller packing.
It also makes no separate claim of global uniqueness of all optimal packings.

## What Was Verified, and What the Verification Means

The public proof source is
[Queuingtheorydotcom/11SquaresOptimal](https://github.com/Queuingtheorydotcom/11SquaresOptimal/tree/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c),
linked at the revision that was confirmed.
The Squares Project’s confirmation uses independently written consumers of its proposed
certificate data and a mathematical review of the implications above.
The accepted computation covers the required proof ensemble, including all 2,180
exclusions and all ten capture nodes.[^review]

| Mathematical obligation | Accepted evidence |
| --- | --- |
| Exact endpoint and matching upper bound | Algebraic root, unit-square construction, 44 vertex containment checks, 55 pair checks, $T<U$, opposite-wall span |
| Exhaustive global classification | Sixteen closed cells, 4,368 masks, 2,184 half-turn representatives |
| Noncandidate impossibility | Exact 2,180-case exclusion set with discharged conditional premises |
| Reduction to case 438 | Closed symmetry overlay and exhaustive assignment check |
| Capture | Complete root induction, ten nodes, nine parent joins and all four closed leaves |
| Local isolation and inclusion | Complete feature census, 8,448 dual checks, nonlinear bounds and enclosure of the accepted near state |
| Final theorem | Composition of those premises with the rigid smaller-container embedding |

Search programs may choose promising cuts, cores or dual weights.
They need not be trusted to find correct ones: a certificate checker recomputes the
finite conditions that make each proposal sound.
The review must still establish why those conditions imply the continuous geometric
claim. Reexecution tests reproducibility; it does not, by itself, prove that a checker
implements a sound mathematical rule.

The independence has limits.
The local construction, derivative calculations and exact arithmetic include shared
first-party primitives.
The confirmation follows the same mathematical argument, rather than supplying a
distinct proof method.
V3/C3 consequently means a machine certificate replayed here with its review record
pending, not distinct-method confirmation, not the adversarially reviewed and
human-overseen rung 4, and not V5 formal verification.
The trust base includes the reviewed mathematical reductions, checker source, arithmetic
libraries, runtime and executing system.

The final composition receipt reconciles the completed geometric executions and their
reviewed dependencies.
It does **not** rerun those calculations.
Four stale final-state digest bindings in the publisher’s packet prevented accepting its
unchanged full runner as a successful replay; the independent confirmation uses freshly
observed component executions and checked state joins instead.
A fresh one-command rerun of the entire independent ensemble still needs a reviewed way
to rebind newly generated parent receipts, whose timing fields change their bytes.
That automation issue is tracked separately from the completed mathematical
obligations.[^reproduce]

The [T-060 validation guide][reproduction] separates fast checks of retained evidence
from fresh geometric replay, and links each checker, source binding and recorded
execution. It is the place to reproduce a component; merely rerunning the final composer
is not an independent end-to-end proof run.

## Appendix A: Exact Placement Formulas

For a direct construction, let $A(a,b)=[a,a+1]\times[b,b+1]$, and define

$$
\begin{aligned}
\rho&=1-(T-3)c, &
\eta&=\frac{(1+\rho)c-1}{s},\\
v&=c-s, &
\zeta&=\frac{T-1}{s}-\rho-(3+\eta)\frac{c}{s},\\
x_0&=1+\frac{2}{c}-(T-2)\frac{s}{c}.
\end{aligned}
$$

The six axis-aligned squares are

$$
\begin{gathered}
A(0,0),\quad A(T-1,0),\quad A(x_0,T-1),\\
A(0,T-1),\quad A(1,T-1),\quad A(0,T-2).
\end{gathered}
$$

Define the rigid map

$$
F(x,y)=(1,1)+
\begin{pmatrix}c&-s\\s&c\end{pmatrix}(x,y-\rho).
$$

The remaining five squares are the images under $F$ of

$$
\begin{gathered}
A(0,0),\quad A(\eta,-1),\quad A(1,v),\\
A(\eta+1,v-1),\quad A(\eta+2,-\zeta).
\end{gathered}
$$

All quantities are elements of $\mathbb Q(u)$. These formulas, together with the
isolated root, specify the construction without relying on coordinates read from a
drawing.[^construction]

## Appendix B: The Nonlinear Estimates

For a pair gap, let square $o$ supply the separating axis and square $p$ supply the
tested corner. Put $w_i=r_{3i+2}$ for square $i$’s angular radius.
A bound on the second derivative along any direction in the coordinate rectangle is

$$
\begin{aligned}
K={}&D_{op}w_o^2\\
&+2\sqrt{(r_{3o}+r_{3p})^2+(r_{3o+1}+r_{3p+1})^2}\,w_o\\
&+\frac{(w_o+w_p)^2}{\sqrt2}.
\end{aligned}
$$

Here $D_{op}$ bounds center separation throughout the analytic working box.
The terms bound the rotation of the center projection, the mixed translation–rotation
derivative and the relative rotation of the corner.
A wall gap has $K=w_i^2/\sqrt2$. Checked rational upper bounds replace the square roots.
When several elementary gap functions share one gradient, the checker uses the largest
applicable curvature bound.

An unavailable separation feature has a corner gap $g$ with $g(0)<0$. The checker
establishes

$$
g(0)+\sum_j|\partial_jg(0)|r_j+K/2<0.
$$

Taylor’s theorem then keeps that corner gap negative throughout the closed rectangle.
The feature cannot become available there.
These 88 exclusions, the exhaustive remaining feature choices, and the
curvature-weighted dual inequalities supply the nonlinear premises of local
isolation.[^local]

## Sources and Verification Record

The [simplification review][simplification] freezes the dependency map used in this
exposition. It consolidates repeated geometric rules and the endpoint argument without
claiming fewer necessary cases, rounds or branches.
The figures are explanatory renderings of retained data; their rounded screen
coordinates are not inputs to certificate acceptance.

[^credit]: [T-060 attribution and evidence](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/frontier/results.yaml);
    [upstream source and third-party credits](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/README.md).
    Trump’s construction is credited to Walter Trump; the bundled exact reconstruction
    credits David Ellsworth’s diagram.
    This paper explains the imported proof and the repository’s confirmation, rather
    than claiming a new global argument.

[^proof]: [Original proof, §1: exact statement](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#1-statement-and-exact-endpoint)
    and
    [§10: final deduction](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#10-deduction-of-the-optimum);
    [whole-proof acceptance review](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance).

[^review]: [T-060](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/frontier/results.yaml);
    [current review disposition](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/reviews/review-2026-09-29-n11-optimality.md);
    [whole-proof acceptance](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance);
    [verification and confirmation levels](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/epistemics.md).

[^lineage]: [Historical T-018/T-025/T-026 explainer](https://jlevy.github.io/squares/);
    [n = 11 result history](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/frontier/n-011.md);
    [result register](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/frontier/results.yaml).

[^tools]: [Tooling overview and scope of independent verification](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/verification-tooling.md).
    T-059 concerns reported row-minimum equality, while T-060 concerns global
    optimality. A rectangle-density or row-minimum check cannot substitute for the
    latter’s complete case and capture argument.

[^construction]: [Exact construction source](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/cases/trump11/packing.py);
    [exact feasibility checker](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/cases/trump11/verify_exact.py);
    [original proof, §2: construction and upper bound](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#2-exact-construction-and-upper-bound).

[^cover]: [Original proof, §4: closed center cover and masks](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#4-closed-center-cover-and-the-2184-cases);
    [exact cover consumer](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_d4.py);
    [independent cover receipt](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json);
    [case census](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/case-census/result.json).

[^geometry]: [Original proof, §5: case-exclusion implications](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#5-what-an-exact-case-exclusion-certificate-proves);
    [independent row geometry checker](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_capture_transition_pilot.py) and
    [first-row receipt](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/capture-transition-row0/result.json);
    [complete ownership update](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/capture-step0/result.json).
    The
    [mathematical transition review](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#first-complete-capture-owner-update)
    separates a checked row from a promoted complete step.

[^field]: [Original proof, §5: field charges and transfer](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#5-what-an-exact-case-exclusion-certificate-proves);
    [exact field consumer](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_field_mask0.py);
    [accepted mask-0 field receipt](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/shared-field-mask0/summary.json);
    [mathematical review of the five-site charge](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#first-independent-field-exclusion-mask-0).

[^exclusions]: [Complete exclusion inventory](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/exclusion-inventory.json);
    [case census, which counts the field certificates](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/case-census/result.json);
    [original proof, §9: accepted global obligations](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#9-accepted-global-verification-obligations);
    [independent exclusion and conditional-premise review](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#complete-exclusion-execution-census).

[^symmetry]: [Closed-overlay checker](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_d4.py),
    [accepted symmetry receipt](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json)
    and
    [original proof, §6: the D4 implication](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#6-the-exact-d4-reduction-to-case438).

[^capture]: [Capture ancestry](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json);
    [fourteen-round root chain](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/capture-root-chain/result.json);
    [accepted near node](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/capture-child-near/result.json)
    and
    [pose-inclusion receipt](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json);
    [original proof, §8: capture and frame bridge](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#8-complete-case438-capture-and-the-exact-u-to-t-bridge).

[^local]: [Exact local-isolation checker](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/devtools/check_n11_optimality_local_isolation.py)
    and
    [accepted local-isolation receipt](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json);
    [original proof, §7: contact branches and finite rectangle](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#7-local-contact-analysis-and-the-focused-isolation-rectangle).
    The focused rectangle is distinct from the earlier uniform-radius local theorem.

[^endpoint]: [Original proof, §10: deduction of the optimum](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#10-deduction-of-the-optimum);
    [endpoint and final-composition review](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance);
    [accepted final composition](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json).

[^reproduce]: [Reproduction guide and disclosed limits](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/README.md#reproducing-the-independent-checks);
    [tooling overview](https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/verification-tooling.md).
    The final composition has `geometry_rerun: false`; it binds the observed executions
    rather than replacing them.

[earlier]: https://jlevy.github.io/squares/
[reproduction]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/packing/resources/web/n11-optimality-2026-09-29/VALIDATION.md
[simplification]: https://github.com/jlevy/squares/blob/ea0a3b19a70085683c3b65946cded03ffe4e2415/docs/project/reviews/review-2026-09-30-n11-expository-simplification.md

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
