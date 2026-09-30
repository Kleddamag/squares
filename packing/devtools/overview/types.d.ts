/** Types shared by the site's table script and its Node tests. */

type SiteTableSortType = "num" | "text";

interface SiteTableFilter {
  key: string;
  kind: "equals" | "flag" | "min" | "max";
  value: string;
}

interface SiteTableApi {
  compareKeys(left: string, right: string, type: SiteTableSortType): number;
  sortOrder(
    keys: readonly string[],
    type: SiteTableSortType,
    direction: "ascending" | "descending",
  ): number[];
  rowMatches(
    row: Readonly<Record<string, string | undefined>>,
    filters: readonly SiteTableFilter[],
  ): boolean;
  countText(shown: number, total: number, noun: string): string;
  controlParam(key: string, bound: string | null): string;
  init(): void;
}

declare var SiteTable: SiteTableApi;
