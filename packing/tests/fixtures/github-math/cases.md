# GitHub Math Cases

Where GitHub opens inline math, one case per list item. Each case holds exactly one
formula, $c_{N}$ with its own number, so the formulas GitHub rendered name the cases it
accepted. `devtools.check_github_math --probe` fetches this file’s page and reports each
case; `devtools.migrate_math` leaves a span as code in every context marked *code*.

## Before the Opening Dollar

- after a space: x $c_{1}$ y
- at the start of a line:
  $c_{2}$ y
- after a hyphen: side-$c_{3}$ y
- after a slash: 0/$c_{4}$ y
- after an opening parenthesis: x ($c_{5}$) y
- after an opening square bracket, not a link: x [$c_{6}$] y
- after a straight double quote: x "$c_{7}$" y
- after a curly double quote: x “$c_{8}$” y
- after a curly single quote: x ‘$c_{9}$’ y
- after an em dash: x—$c_{10}$ y
- after an en dash: 1–$c_{11}$ y
- after a comma: x,$c_{12}$ y
- after a colon: x:$c_{13}$ y
- after a letter: x$c_{14}$ y
- after a digit: 1$c_{15}$ y
- after bold’s opening stars: **$c_{16}$ y**
- after a closing parenthesis: (x)$c_{17}$ y
- after a plus sign: x+$c_{18}$ y
- after an equals sign: x=$c_{19}$ y

## After the Closing Dollar

- before a space: x $c_{20}$ y
- before a hyphen: x $c_{21}$-fold
- before a slash: x $c_{22}$/2
- before a closing parenthesis: x ($c_{23}$) y
- before a comma, a full stop and a colon: x $c_{24}$, $c_{25}$. $c_{26}$: y
- before a curly apostrophe: x $c_{27}$’s y
- before an em dash: x $c_{28}$— y
- before a letter: x $c_{29}$th y
- before a digit: x $c_{30}$1 y

## Inside Inline Markup

- inside link text: [$c_{31}$](#github-math-cases)
- inside link text after a word: [see $c_{32}$](#github-math-cases)
- inside bold: **x $c_{33}$ y**
- inside italic with stars, on one line: *x $c_{34}$ y*
- inside italic with underscores, on one line: _x $c_{35}$ y_
- inside italic across two lines: *x $c_{36}$ y
  z*
- inside bold italic: ***x $c_{37}$ y***
- inside strikethrough: ~~x $c_{38}$ y~~
- in a heading’s neighbour, a table cell:

| a | b |
| --- | --- |
| x $c_{39}$ y | ($c_{40}$) |

- in a blockquote:

> x $c_{41}$ y

- in a list item after a bold label: **Label:** $c_{42}$ y
- after an image on the same line: ![alt](#github-math-cases) $c_{43}$ y

## Inside the Formula

- a backslash before punctuation: x $\lbrace c_{44} \rbrace$ y
- an escaped brace: x $\{c_{45}\}$ y
- an underscore pair that could read as emphasis: x $c_{46} + a_b + a_b$ y
- a star pair that could read as emphasis: x $c_{47} a^* b^*$ y
- a less-than before a letter: x $c_{48} < b$ y
- a less-than touching a letter: x $c_{49}<b$ y
- an ampersand: x $c_{50} \& b$ y
