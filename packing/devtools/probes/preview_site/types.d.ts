// The site pages' global `preview_site`'s probes read, beyond the math runtime's in
// `probes/explainer.d.ts`. `site-math.js` installs it; `overview/types.d.ts` declares the
// same shape for the pages' own program.

interface Window {
  siteMath?: { typeset(root: ParentNode): Promise<void> };
}
