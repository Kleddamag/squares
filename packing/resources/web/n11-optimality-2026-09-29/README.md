# Eleven-Square Optimality Source Packet

[Queuingtheorydotcom/11SquaresOptimal](https://github.com/Queuingtheorydotcom/11SquaresOptimal)
publishes a proposed computer-assisted proof that the known eleven-square packing is
globally optimal under independent rotations and boundary contact.
Its claimed minimum side is the algebraic Trump construction side, about 3.8770835900.
The frontier intake is T-060 at S5/V0/C1: a significant reported claim with a scoped
source review, not complete mathematical or computational confirmation.
Its initial receipt classification was C0; the recorded scoped review raised it to C1.

This packet pins source commit `f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c` and tree
`3fed944c5a0c1dda5e61cb9f45f0dd3d4dc6360c`. The selected files in [`source/`](source/)
are verbatim; [`provenance.json`](provenance.json) records their hashes.
The original `data/INDEX.json` is stored as deterministic
[`INDEX.json.gz`](source/data/INDEX.json.gz); provenance records both its decoded and
stored hashes. Start with the [claim](source/README.md),
[proof exposition](source/PROOF.md),
[reproduction instructions](source/docs/REPRODUCING.md), and
[publication scope](source/docs/PUBLICATION.md).

The published data store uses Git LFS.
[`lfs-pointer-inventory.json.gz`](lfs-pointer-inventory.json.gz) lists 2,638 unresolved
pointer files representing 2,344,331,966 declared bytes at initial intake.
The subsequent [independent symmetry receipt](receipts/d4-independent/result.json)
retains three selected compressed objects totaling 102,046 bytes, with provenance and a
replay script beside it.
The [local residual receipt](receipts/local-dual-residual/result.json) subsequently
retains two further objects totaling 1,560,204 compressed bytes and checks all 8,448
signed-coordinate residuals. Its status remains incomplete: curvature, feature margins
and geometric capture are separate obligations. Adjacent provenance and replay files
bind the inputs and implementation, including shared source primitives.
The later [fixed-T local-isolation receipt](receipts/local-isolation/result.json)
confirms all curvature, feature-margin and nonlinear-branch obligations using the same
two objects. It isolates the labelled Trump pose inside the supplied rectangle;
pose inclusion, capture and global optimality remain unproved here.
The remaining payloads have not been acquired for this packet.
The symmetry check passed conditionally; it does not establish global optimality.
The source’s publication note says the privacy-normalized public derivative has not had
a fresh full geometric replay.
No fetched checker has been executed for this intake.

The construction is credited to Walter Trump, and the bundled `jlevy/squares` source
credits David Ellsworth’s reconstruction diagram.
The source’s [third-party notices](source/THIRD_PARTY_NOTICES.md) assert no blanket
license over the collection; each file retains its applicable terms.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
