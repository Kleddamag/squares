// A case's record file, `cases/11.html`, is the record alone and plain: what a reader
// without scripts, or a crawler, reads. A reader with scripts is sent on at once, from
// the file's head, to the record page beside it, `./?n=11`, with the fragment they came
// with; that page fetches this same file and shows its record in the site's design. The
// case is the root element's `data-case`. `?raw` keeps a reader here, and the record page
// asks for it when it cannot fetch a record, so the two never send a reader round in a
// loop. A file read from disk stays too, since the record page could not fetch it there.
(() => {
  const n = document.documentElement.dataset.case;
  if (
    !n ||
    !/^\d+$/.test(n) ||
    location.protocol === "file:" ||
    new URLSearchParams(location.search).has("raw")
  ) {
    return;
  }
  location.replace(`./?n=${n}${location.hash}`);
})();
