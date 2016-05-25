from unittest import TestCase

from rest_framework_latex.markdown import LatexRenderer

from CommonMark import Parser, ASTtoJSON


class MarkdownTestCase(TestCase):
    def test_paragraphs(self):
        case = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Nullam augue felis, eleifend at quam id, molestie placerat felis.
Nunc laoreet sapien tellus, ac blandit arcu lobortis eu. Etiam sit amet ex commodo, condimentum felis quis, suscipit nunc. Duis eu egestas diam, sed placerat arcu. Aliquam vestibulum consectetur ipsum a ullamcorper. Integer pretium eros a nisl cursus tristique. Cras in molestie nisi, nec dictum 
nunc. Phasellus ultrices euismod tortor, vel molestie mi cursus
eu. Integer blandit et urna vel molestie. Pellentesque et est
et arcu tincidunt maximus.

Morbi dignissim, risus ac ornare accumsan, ex magna accumsam
diam, ac interdum nisl enim nec justo. Donec efficitur, tortor
non ornare sagittis, sapien tellus rutrum neque, quis lobortis sapien
urna vitae magna. Pellentesque dictum magna eu urna commodo,
a vulputate massa fringilla. Sed egestas sodales libero, sed blandit
dui gravida sit amet. Mauris egestas consectetur leo in tincidunt.
Vivamus bibendum sodales risus. Maecenas bibendum justo non auctor
ullamcorper. Sed felis ipsum,
viverra non justo id, congue fringilla neque. Proin a facilisis lectus.

Suspendisse potenti. Proin vitae diam sem. Nam accumsan nisi vel
diam accumsan, at porta dui tempus. In in nunc pellentesque ligula
porta iaculis. Aenean ultricies ante ex, nec fringilla felis
sollicitudin non. Ut diam est, varius a mi id, commodo tincidunt dui.
Donec et ante consequat, consequat elit vitae, rutrum justo. Ut mattis
ex porta nibh porta mattis. Suspendisse sit amet est turpis. Donec a
fermentum diam, semper dapibus ipsum. Duis volutpat libero et quam
rutrum porta.

Nulla nec suscipit nunc. Duis ut ligula ac neque condimentum commodo.
Donec eu ullamcorper felis. Ut rhoncus lectus vel sapien blandit varius.
Ut aliquet odio ligula, sit amet viverra augue interdum nec. Donec
sodales, turpis sed suscipit euismod, ex erat venenatis neque, ut
dictum ipsum ante ac urna. Vestibulum at magna id lacus luctus
fermentum. Pellentesque nisi purus, tempus eu faucibus sed, fringilla
sit amet justo. In laoreet, nisl sed posuere vulputate, lorem augue
placerat ipsum, at facilisis quam odio ut est. Proin eget enim dui.
Morbi id feugiat mauris, in faucibus odio. Nam quis venenatis quam.
Fusce leo velit, ullamcorper in leo vestibulum, ultricies pulvinar
neque. Suspendisse semper eros sit amet diam bibendum fringilla.
Vestibulum consectetur venenatis erat a faucibus. Integer tristique
eleifend mauris.
        """
        parser = Parser()
        ast = parser.parse(case)
        lr = LatexRenderer()
        latex = lr.render(ast)
        self.assertEquals(latex.count('\n\n'), 4)

    def test_headings(self):
        case = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

##### Heading 6
        """
        parser = Parser()
        ast = parser.parse(case)
        lr = LatexRenderer()
        latex = lr.render(ast)

        self.assertEquals(latex.count('\huge'), 2)
        self.assertEquals(latex.count('\LARGE'), 1)
        self.assertEquals(latex.count('\Large'), 1)
        self.assertEquals(latex.count('\large'), 2)

    def test_escape(self):
        case = """
\\begin{parahrah}
    \\textt{NO}
\\end{paragraph}
        """
        parser = Parser()
        ast = parser.parse(case)
        lr = LatexRenderer()
        latex = lr.render(ast)
        self.assertEquals(latex, (
            '\\textbackslash{}begin\{parahrah\}\\textbackslash'
            '{}textt\{NO\}\\textbackslash{}end\{paragraph\}\n\n'
        ))

    def test_inline_formatting(self):
        case = """
The **quick** brown _fox_ jumped over the __lazy__ cow.
        """
        parser = Parser()
        ast = parser.parse(case)
        lr = LatexRenderer()
        latex = lr.render(ast)
        self.assertEquals(latex, (
            'The \\textbf{quick} brown \\emph{fox} jumped over'
            ' the \\textbf{lazy} cow.\n\n'
        ))

    def test_list(self):
        case = """
Shopping list:

* Eggs
* Cheese
* Lager
        """
        parser = Parser()
        ast = parser.parse(case)
        lr = LatexRenderer()
        latex = lr.render(ast)
        self.assertEquals(latex, (
            'Shopping list:\n\n\\begin{enumerate}\\item Eggs\n\n'
            '\\item Cheese\n\n\\item Lager\n\n\\end{enumerate}'
        ))
