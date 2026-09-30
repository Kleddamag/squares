# GitHub Math Cases

Where GitHub opens inline math, one case per list item. Each case holds exactly one
formula, $c_{N}$ with its own number, so the formulas GitHub rendered name the cases it
accepted. Each item records what GitHub did, as measured on 30 September 2026: `[math]`,
drawn as written; `[altered]`, drawn with different TeX; `[code]`, left as dollars.
`devtools.check_github_math --probe` fetches this file’s page and reports every case that
has moved from its record, and `tests/test_migrate_math.py` holds `devtools.migrate_math`
to leaving a span as code in every context recorded `[code]` or `[altered]`. A display
block takes the record of the list item that introduces it.

## Before the Opening Dollar

- [math] after a space: x $c_{1}$ y
- [math] at the start of a line:
  $c_{2}$ y
- [code] after a hyphen: side-$c_{3}$ y
- [code] after a slash: 0/$c_{4}$ y
- [math] after an opening parenthesis: x ($c_{5}$) y
- [code] after an opening square bracket, not a link: x [$c_{6}$] y
- [code] after a straight double quote: x "$c_{7}$" y
- [code] after a curly double quote: x “$c_{8}$” y
- [code] after a curly single quote: x ‘$c_{9}$’ y
- [code] after an em dash: x—$c_{10}$ y
- [code] after an en dash: 1–$c_{11}$ y
- [code] after a comma: x,$c_{12}$ y
- [code] after a colon: x:$c_{13}$ y
- [code] after a letter: x$c_{14}$ y
- [code] after a digit: 1$c_{15}$ y
- [math] after bold’s opening stars: **$c_{16}$ y**
- [code] after a closing parenthesis: (x)$c_{17}$ y
- [code] after a plus sign: x+$c_{18}$ y
- [code] after an equals sign: x=$c_{19}$ y

## After the Closing Dollar

- [math] before a space: x $c_{20}$ y
- [math] before a hyphen: x $c_{21}$-fold
- [math] before a slash: x $c_{22}$/2
- [math] before a closing parenthesis: x ($c_{23}$) y
- [math] before a comma, a full stop and a colon: x $c_{24}$, $c_{25}$. $c_{26}$: y
- [math] before a curly apostrophe: x $c_{27}$’s y
- [math] before an em dash: x $c_{28}$— y
- [code] before a letter: x $c_{29}$th y
- [code] before a digit: x $c_{30}$1 y

## Inside Inline Markup

- [code] inside link text: [$c_{31}$](#github-math-cases)
- [code] inside link text after a word: [see $c_{32}$](#github-math-cases)
- [math] inside bold: **x $c_{33}$ y**
- [code] inside italic with stars, on one line: *x $c_{34}$ y*
- [code] inside italic with underscores, on one line: _x $c_{35}$ y_
- [code] inside italic across two lines: *x $c_{36}$ y
  z*
- [code] inside bold italic: ***x $c_{37}$ y***
- [math] inside strikethrough: ~~x $c_{38}$ y~~
- in a heading’s neighbour, a table cell:

| a | b |
| --- | --- |
| [math] x $c_{39}$ y | ($c_{40}$) |

- in a blockquote:

> [math] x $c_{41}$ y

- [math] in a list item after a bold label: **Label:** $c_{42}$ y
- [math] after an image on the same line: ![alt](#github-math-cases) $c_{43}$ y

## Inside the Formula

- [math] a backslash before punctuation: x $\lbrace c_{44} \rbrace$ y
- [altered] an escaped brace: x $\{c_{45}\}$ y
- [math] an underscore pair that could read as emphasis: x $c_{46} + a_b + a_b$ y
- [math] a star pair that could read as emphasis: x $c_{47} a^* b^*$ y
- [math] a less-than before a letter: x $c_{48} < b$ y
- [math] a less-than touching a letter: x $c_{49}<b$ y
- [altered] an ampersand: x $c_{50} \& b$ y
- [altered] a thin space: x $c_{51}\,b$ y
- [altered] a thick space: x $c_{52}\;b$ y
- [altered] a medium space: x $c_{53}\:b$ y
- [altered] a negative thin space: x $c_{54}\!b$ y
- [altered] a double bar: x $\|c_{55}\|$ y
- [altered] an escaped underscore: x $c_{56}\_b$ y
- [math] a subscript star: x $c_{57}L_*$ y
- [altered] a closing brace escape alone: x $c_{58}\}$ y
- [math] the brace commands: x $\lbrace c_{59} \rbrace$ y
- [math] the space commands: x $c_{60}\thinspace b\medspace c\thickspace d$ y
- [math] the double bar command: x $\Vert c_{61} \Vert$ y

## Display Math

- [math] a display block on its own lines:

$$
c_{62} + \frac{1}{2}
$$

- [altered] a display block with a line break:

$$
\begin{aligned} c_{63} &= 1 \\ d &= 2 \end{aligned}
$$

- [altered] a display block with an escaped brace:

$$
\{c_{64}\}
$$

- [altered] a display block with a thin space:

$$
c_{65}\,b
$$

- [math] a display block inside one line: $$c_{66} + 1$$

- [math] a display block breaking lines with `\cr`:

$$
\begin{aligned} c_{67} &= 1 \cr d &= 2 \end{aligned}
$$

- [math] a display block breaking lines with `\newline`:

$$
\begin{aligned} c_{68} &= 1 \newline d &= 2 \end{aligned}
$$

- [code] an inline formula breaking an array with `\cr`: x $\begin{smallmatrix} c_{69} \cr d \end{smallmatrix}$ y

## Across Formulas in One Paragraph

- [code] two starred subscripts, one formula each: x $c_{70}L_*$ y and z $c_{71}L_*$ w
- [math] a starred superscript, then a subscript: x $c_{72}\tau^*(L)$ y and z $c_{73}w_a$ w
- [code] two stars across three formulas: x $c_{74}a^*$ y, $c_{75}$ and $c_{76}b^*$ w
- [math] underscores across formulas: x $c_{77}t_2$ y and $c_{78}t_1$ w
- [math] a closing curly quote after: “for every $c_{79}$” y
- [math] inside parentheses after a word: the degree (x $c_{80}$) and y
- [math] a starred formula then a star in prose: x $c_{81}L_*$ y *z* w
- [math] the same with the star command: x $c_{82}L_{\ast}$ y and z $c_{83}L_{\ast}$ w
- [math] three formulas with the star command: x $c_{84}a^{\ast}$ y, $c_{85}$ and $c_{86}b^{\ast}$ w
