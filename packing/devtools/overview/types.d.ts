/** Globals the site pages' classic scripts read, beyond the math runtime's in `probes/explainer.d.ts`. */
interface Window {
  kpressInitTooltips?: (root: Document, options: { only: string }) => void;
  kpressInitCodeCopy?: (root: Document) => void;
  /** Installed by `site-math.js`: typeset the formulas under one element after load. */
  siteMath?: { typeset(root: ParentNode): Promise<void> };
}
