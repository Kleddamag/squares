// A script whose text reads like a link attribute, ` href="a.html"`, which rebasing a
// page's links must leave alone: a script's and a style's text are not markup
// (`render_case_pages.rebase_links`).
() => ' href="a.html" src="b.png"';
