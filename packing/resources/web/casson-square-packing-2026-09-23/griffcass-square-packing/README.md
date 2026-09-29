# Squares in squares: 39 improved packings (n = 103–307)

This repository contains packings of `n` unit squares in a square container. For 39 values of `n` between 103 and 307, they have a smaller container side than the best known packings listed in the [squares-in-squares catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares.html). The comparison was made against the catalogue as it stood on **23 September 2026**. The repository also includes the code that found and verified them, and a write-up.

- **2 new arrangements** (n = 106, 123) found by simulated annealing on a GPU, followed by sequential linear programming (SLP).
- **37 improvements** (n = 103 … 307) found by running SLP directly on the published record packings. Those records turned out not to be local minima of the container side. The largest gains are 1.29e-3 (n = 237) and 6.7e-4 (n = 306, 307).
- **Certification:** every packing has at least 1e-10 clearance between any two squares and at least 5e-12 from the walls. Each passes two checks:
  - David Ellsworth's own `check_packing.py`, at 16 digits;
  - an independent 50-digit separating-axis checker (`verify_mp.py`).

  Each one *fails* the 50-digit check when its side is shrunk by 2e-11.

📄 **Paper:** [`paper/paper.pdf`](paper/paper.pdf). It gives the full method, every parameter, the negative controls, and coordinates.

> These are numerically certified upper bounds on s(n), not proofs of optimality. Records change often; check the live catalogue before relying on any single entry. For example, n = 68 and n = 206 were beaten again before this was published and are not included.

## Results

| n | record side (catalogue, 2026-09-23) | our side (rounded up) | difference | how |
|---|---|---|---|---|
| 103 | 10.70378195534367 | 10.70377984436968 | -2.11e-06 | polish |
| 105 | 10.80761933330707 | 10.80758853319603 | -3.08e-05 | polish |
| 106 | 10.82297973416944 | 10.82293693182616 | -4.28e-05 | **new arrangement** |
| 123 | 11.60139979378801 | 11.60138465962088 | -1.51e-05 | **new arrangement** |
| 131 | 11.95652543280926 | 11.95652190193194 | -3.53e-06 | polish |
| 132 | 11.99137344423646 | 11.99134529315215 | -2.82e-05 | polish |
| 152 | 12.83095954472600 | 12.83071880600231 | -2.41e-04 | polish |
| 154 | 12.93166712962655 | 12.93166403111079 | -3.10e-06 | polish |
| 155 | 12.95844711161529 | 12.95820609164225 | -2.41e-04 | polish |
| 156 | 12.98208376048414 | 12.98208269973812 | -1.06e-06 | polish |
| 180 | 13.93508705291129 | 13.93500418116476 | -8.29e-05 | polish |
| 181 | 13.95690672341755 | 13.95679529257279 | -1.11e-04 | polish |
| 182 | 13.97419105332569 | 13.97409071444283 | -1.00e-04 | polish |
| 207 | 14.89395494255333 | 14.89395465342148 | -2.89e-07 | polish |
| 208 | 14.93776656277905 | 14.93761283595917 | -1.54e-04 | polish |
| 209 | 14.95861500087481 | 14.95856148981293 | -5.35e-05 | polish |
| 210 | 14.97413341886404 | 14.97381035691251 | -3.23e-04 | polish |
| 228 | 15.60902282132495 | 15.60895620815940 | -6.66e-05 | polish |
| 236 | 15.87607539315201 | 15.87606262597992 | -1.28e-05 | polish |
| 237 | 15.91421356237309 | 15.91292783720834 | -1.29e-03 | polish |
| 238 | 15.93965520031394 | 15.93958571370621 | -6.95e-05 | polish |
| 239 | 15.95635358406308 | 15.95623903092503 | -1.15e-04 | polish |
| 240 | 15.97556282833087 | 15.97536577224558 | -1.97e-04 | polish |
| 241 | 15.99080517810520 | 15.99043971050730 | -3.65e-04 | polish |
| 259 | 16.60257141234448 | 16.60256850594296 | -2.91e-06 | polish |
| 268 | 16.87931143465371 | 16.87895510935974 | -3.56e-04 | polish |
| 269 | 16.90596764828402 | 16.90596713867400 | -5.10e-07 | polish |
| 270 | 16.94062059800744 | 16.94057158197227 | -4.90e-05 | polish |
| 271 | 16.95499909412532 | 16.95479445810087 | -2.05e-04 | polish |
| 272 | 16.96971602419903 | 16.96944950195849 | -2.67e-04 | polish |
| 273 | 16.98820725030513 | 16.98811467146215 | -9.26e-05 | polish |
| 292 | 17.60257141234448 | 17.60256849240574 | -2.92e-06 | polish |
| 297 | 17.74106074604732 | 17.74092885618565 | -1.32e-04 | polish |
| 301 | 17.86889155557430 | 17.86867840793059 | -2.13e-04 | polish |
| 303 | 17.93125509556197 | 17.93105636462954 | -1.99e-04 | polish |
| 304 | 17.94910783564662 | 17.94880191214548 | -3.06e-04 | polish |
| 305 | 17.96066201401205 | 17.96053668235996 | -1.25e-04 | polish |
| 306 | 17.96913960675661 | 17.96846609160516 | -6.74e-04 | polish |
| 307 | 17.98272201579610 | 17.98205200143470 | -6.70e-04 | polish |

The full table is in [`results/summary.csv`](results/summary.csv). It includes verification status, file hashes, and the first and latest catalogue credit for each record. Every packing is in [`results/packings/`](results/packings), and a side-by-side figure of each one against the record is in [`results/figures/`](results/figures).

Packing files use the catalogue's format: the side on the first line, then one line per square giving its centre and angle, with the origin at the container centre:

```
s: 10.82293693182615435
Square 1: x=-4.91146817267234681, y=4.91146846586836539, deg=-0.00000000454443378
...
```

## Verify a packing yourself

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python verify_mp.py results/packings/n237.txt 237                    # VALID ... min_pair_gap=1.0e-10
python verify_mp.py results/packings/n237.txt 237 --shrink 2e-11     # FAIL (negative control)
```

To use the catalogue maintainer's checker instead:

```bash
git clone https://github.com/Davidebyzero/packing_squares_in_squares__tools tools/ellsworth
python tools/ellsworth/check_packing.py results/packings/n237.txt 16
```

## Reproduce the search

The steps below need Linux, gcc, Python 3.11 or newer, and optionally CUDA for the GPU annealer. We used an RTX 3070 and a Ryzen 7 5800X.

```bash
./build.sh                                   # packing_kernel.so, sa_engine (OpenMP), sa_gpu (if nvcc is found)
python fetch_records.py                      # download current records -> records/ (also fetches tools/ellsworth)
python polish_records.py --min-n 100         # SLP-polish every record; improvements -> runs/n<N>/POLISHED_*.txt
python hunt.py --engine gpu --chains 8192 --minutes 12 --rounds 0 --polishers 12 --n 106 123
tail -f runs/hunt.log                        # the hunt stops when it finds a candidate
python certify.py runs/n106/CANDIDATE_*.txt runs/certified_hunt   # add clearance, check at 16 digits
python render_compare.py 106 runs/n106/CANDIDATE_*.txt n106.svg   # figure
python paper/build.py                        # paper/paper.html + paper.pdf (needs Chromium)
```

## Files

| file | what it does |
|---|---|
| `slp.py` | Sequential linear programming. Minimises the side over every square's x, y and angle, using face-separation constraints solved with HiGHS. |
| `sa_gpu.cu` | CUDA simulated annealing, one single-precision chain per thread, seeded from a record. |
| `sa_engine.c` | The same annealer for the CPU (OpenMP, double precision). |
| `hunt.py` | Runs the annealer, polishes its output with SLP, removes duplicates and flags candidates. |
| `polish_records.py` | Runs SLP on every catalogue record, from the record itself and from slightly perturbed copies. |
| `certify.py` | Adds the 1e-10 / 1e-11 clearances, writes the catalogue format and runs Ellsworth's checker. |
| `verify_mp.py` | Independent 50-digit check: square count, walls, and a separating-axis test on every close pair. |
| `fetch_records.py` | Downloads the current records and converts them to seed files. |
| `render_compare.py` | Draws a record next to one of our packings as an SVG. |
| `basin_hop.py`, `packing_kernel.c` | Geometry helpers (repair by dilation, verification) plus a CPU basin-hopping search, documented in [`docs/basin_hopping.md`](docs/basin_hopping.md). |
| `results/` | The 39 certified packings, the summary CSV, figures and the raw search logs. |
| `paper/` | Source of the write-up (`body.html`, `build.py`, `data.json`) and the built `paper.pdf`. |

Downloaded records (`records/`), third-party tools (`tools/`) and search output (`runs/`) are not tracked; the commands above regenerate them.

## Credits

This builds on the catalogue maintained by David Ellsworth, started by Erich Friedman, and on its many contributors. Their record packings were the starting point for 37 of these results. We also used Ellsworth's [parsing and checking tools](https://github.com/Davidebyzero/packing_squares_in_squares__tools). The work was done by Griffin Casson with the help of Claude (Anthropic).

## License

Code: [MIT](LICENSE). Packings, figures and paper: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). If you use these results, please cite the paper (see [`CITATION.cff`](CITATION.cff)).
