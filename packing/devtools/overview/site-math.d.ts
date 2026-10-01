/** The page globals the site's math driver, `math.js`, reads and installs. A browser-only
 * declaration file: the Node program that shares `types.d.ts` has no DOM. */

/**
 * The explainer's math host adapter, `squaresMath`, which every page inlines after KPress's
 * runtime (`render_n11_lower_bounds_explainer.katex_js`); the site's pages use the part `math.js` drives.
 */
interface SiteSquaresMath {
  render(el: Element, source: string, display?: boolean): Promise<boolean>;
  batch(jobs: ReadonlyArray<() => unknown>): Promise<void>;
  settled(): Promise<void>;
}

/** KPress's shared math runtime: the page-wide completion marker `math.js` clears. */
interface SiteKpressMathText {
  complete(): void;
}

/** The site's math driver, `math.js`: queue what is still untypeset under a root. */
interface SiteMath {
  typeset(root: ParentNode, all?: boolean): Promise<void>;
}

declare var squaresMath: SiteSquaresMath | undefined;
declare var kpressMathText: SiteKpressMathText | undefined;
declare var siteMath: SiteMath | undefined;
