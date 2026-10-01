// Wait until the page has stopped working: no long task for `calm` milliseconds, or
// `most` milliseconds at the longest. The overview frames other pages in its cards'
// previews and loads them as they near the window; one that is still typesetting its
// math shares the main thread and would be timed as part of a move. Returns how long
// the wait was and whether the page went calm.
(/** @type {{calm: number, most: number}} */ { calm, most }) =>
  new Promise((resolve) => {
    const start = performance.now();
    let last = start;
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        last = Math.max(last, entry.startTime + entry.duration);
      }
    });
    observer.observe({ entryTypes: ["longtask"] });
    const check = () => {
      const now = performance.now();
      if (now - last >= calm || now - start >= most) {
        observer.disconnect();
        resolve({ waited_ms: Math.round(now - start), calm: now - last >= calm });
        return;
      }
      setTimeout(check, 100);
    };
    check();
  });
