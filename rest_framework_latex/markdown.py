from CommonMark.render.renderer import Renderer

from rest_framework_latex.utils import escape_latex


class LatexRenderer(Renderer):
    """Renderer which turns CommonMark AST into
    LaTeX
    """
    def __init__(self):
        self.headings = {
            1: "\huge",
            2: "\huge",
            3: "\LARGE",
            4: "\Large",
            5: "\large",
            6: "\large",
        }
        self.normal = '\\normalsize'
        self.list_start = '\\begin{enumerate}'
        self.list_end = '\\end{enumerate}'
        self.list_item = '\\item '

    def text(self, node, entering=None):
        self.out(escape_latex(node.literal))

    def linebreak(self, node=None, entering=None):
        self.out('\n\n')

    def softbreak(self, node=None, entering=None):
        pass

    def strong(self, node, entering):
        if entering:
            self.out('\\textbf{')
        else:
            self.out('}')

    def emph(self, node, entering):
        if entering:
            self.out('\\emph{')
        else:
            self.out('}')

    def paragraph(self, node, entering):
        if not entering:
            self.out('\n\n')

    def heading(self, node, entering):
        if entering:
            self.out('\n{}\n'.format(
                self.headings[node.level]))
        else:
            self.out('\n{}\n'.format(
                self.normal))

    def list(self, node, entering):
        if entering:
            self.out(self.list_start)
        else:
            self.out(self.list_end)

    def item(self, node, entering):
        if entering:
            self.out(self.list_item)
