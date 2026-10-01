/** Types shared by the site's table script and its Node tests. */

type SiteTableSortType = "num" | "text";

interface SiteTableFilter {
  key: string;
  /**
   * How the control's value is held against the row's: equal to it, a flag that must be
   * set, a numeric bound, a bound on text that orders as it reads (an ISO date), or a
   * number the row's list of numbers and ranges must hold.
   */
  kind: "equals" | "flag" | "min" | "max" | "from" | "to" | "covers";
  value: string;
}

interface SiteTableApi {
  compareKeys(left: string, right: string, type: SiteTableSortType): number;
  sortOrder(
    keys: readonly string[],
    type: SiteTableSortType,
    direction: "ascending" | "descending",
  ): number[];
  covers(list: string, value: number): boolean;
  rowMatches(
    row: Readonly<Record<string, string | undefined>>,
    filters: readonly SiteTableFilter[],
  ): boolean;
  rowsShown(headings: readonly boolean[], passes: readonly boolean[], grouped: boolean): boolean[];
  countText(shown: number, total: number, noun: string): string;
  controlParam(key: string, bound: string | null): string;
  init(): void;
}

declare var SiteTable: SiteTableApi;

/** The render-time sentinel `kpress-client.js` stands in for kpress's flattened client
 * (`render_overview.kpress_client_script`), as the explainer's own frame declares it. */
declare function __SQUARES_KPRESS_CLIENT_JS__(): void;

/** kpress's math enhancement, a classic script's top-level function. */
declare function enhanceMath(): Promise<void> | undefined;

/** One bound's source as the film cites it: the reference and this project's note. */
interface AtlasCitation {
  text: string;
  note: string | null;
}

/** What the ascent film's panel says about one case, as `atlas_film_facts` writes it. */
interface AtlasFact {
  n: number;
  exact: boolean;
  upper: string;
  lower: string | null;
  star: boolean;
  badges: [glyph: string, style: string, label: string][];
  open: string[];
  record: string;
  cite: { lower: AtlasCitation | null; upper: AtlasCitation | null };
}
