#!/usr/bin/python
"""
This example shows basic document generation functionality.
..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

# begin-doc-include
from pylatex import Document, Section, Subsection, Command, Tabular
from pylatex.utils import italic, NoEscape

print('test')

if __name__ == '__main__':

    # Document with `\maketitle` command activated
    doc = Document()

    doc.preamble.append(Command('title', 'oemof pdf report'))
    doc.preamble.append(Command('author', 'Chrisch'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    with doc.create(Section('Table of Busses')):
        with doc.create(Tabular('r|c|c|c|l')) as table:
            table.add_hline()
            table.add_row(('Bus', 'Component', 'installed capacity',
            'ressources', 'output'))
            table.add_hline()
            table.add_empty_row()
            table.add_row(('b1', 'WKA1', '5MW', 'Sun', '500GWh'))
            table.add_empty_row()
            table.add_row(('b2', 'PV1', '0,8MW', 'Sun', '300MWh'))

    doc.generate_pdf('oemof_table')
    tex = doc.dumps()  # The document as string in LaTeX syntax