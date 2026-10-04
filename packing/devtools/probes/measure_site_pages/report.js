// What `instrument.js` recorded, with the page's own navigation and paint timings, once
// its measurement is done: every time is milliseconds from navigation start. What it
// moved is the document's and every resource's `transferSize`, which is zero for a file
// the cache answered without asking the server.
() => {
  const state = /** @type {any} */ (window).siteLoadMeasure;
  const navigation = /** @type {PerformanceNavigationTiming | undefined} */ (
    performance.getEntriesByType("navigation")[0]
  );
  const resources = /** @type {PerformanceResourceTiming[]} */ (
    performance.getEntriesByType("resource")
  );
  const paint = Object.fromEntries(
    performance.getEntriesByType("paint").map((entry) => [entry.name, entry.startTime]),
  );
  /** @type {number[][]} */
  const tasks = state.longTasks;
  /** @param {number[]} task */
  const length = (task) => task[1] ?? 0;
  return {
    dcl_ms: navigation?.domContentLoadedEventEnd ?? null,
    load_ms: navigation?.loadEventEnd ?? null,
    fcp_ms: paint["first-contentful-paint"] ?? null,
    visible_math_ms: state.visibleMathMs,
    all_math_ms: state.allMathMs,
    math_ready_ms: state.mathReadyMs,
    long_tasks: tasks.length,
    long_task_ms: tasks.reduce((sum, task) => sum + length(task), 0),
    longest_task_ms: tasks.reduce((most, task) => Math.max(most, length(task)), 0),
    blocking_ms: tasks.reduce((sum, task) => sum + Math.max(0, length(task) - 50), 0),
    bytes: navigation?.decodedBodySize ?? null,
    transfer_bytes: [navigation, ...resources].reduce(
      (sum, entry) => sum + (entry?.transferSize ?? 0),
      0,
    ),
    requests: resources.length + 1,
    fetched_requests: resources.filter((entry) => entry.transferSize > 0).length,
    visible_math: state.visibleMath,
    displayed_math: state.displayedMath,
    readable_math: state.readableMath,
    done: state.done,
  };
};
