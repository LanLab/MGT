from time import sleep as sl
import argparse
from pylatex import Document, Section, Subsection, Command, LongTabu, Tabu, MultiColumn, TikZ, Axis, Plot
from pylatex.utils import italic, NoEscape, bold
import pandas as pd



import psycopg2

from os import path
import sys

folder = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(folder)

from Mgt import settings

import matplotlib

matplotlib.use("TkAgg")



class Multistrain(Document):
    def __init__(self,fontclass):
        super().__init__()
        self.preamble.append(Command('usepackage', fontclass))
        #self.preamble.append(NoEscape(r'\usepackage[a4paper, portrait, margin = 1 in]{geometry}'))
        # self.preamble.append(NoEscape(r'\usepackage{geometry}\geometry{a4paper,total={170mm,257mm},left=20mm,top=20mm}'))
        self.preamble.append(Command('title', 'Multilocus Sequence Typing Report for multiple isolates'))
        # self.preamble.append(Command('author', 'Anonymous author'))
        self.preamble.append(Command('date', NoEscape(r'\today')))
        self.append(NoEscape(r'\maketitle'))

    def fill_document(self):
        """Add a section, a subsection and some text to the document."""
        with self.create(Section('A section')):
            self.append('Some regular text and some ')
            self.append(italic('italic text. '))

            with self.create(Subsection('A subsection')):
                self.append('Also some crazy characters: $&#{}')


def general_report(complete, fails, matchIsolates, metadata, metaDf, args):
    newisolates = list(set(matchIsolates).difference(set(complete)))

    """
    todo 
    input dict of id to isolates

    cclis = get_merge_cclis(conn,cc,level,args.appname).split(",")



    """

    doc = Multistrain('tgbonum')

    # Call function to add text
    # doc.fill_document()

    tp = ""
    lev = ""
    if args.stlev:
        tp = "ST"
        lev = args.stlev
    if args.cclev:
        tp = "CC"
        lev = args.cclev
    if args.odclev:
        tp = "ODC"
        lev = args.odclev

    search_restrictions = searchRestrictionList(args)

    # Add stuff to the document timerange="all",year="all",country="all",continent="all"postcode="all",source="all",sourcetype="all",host="all",disease="all"

    if not args.identifier:
        with doc.create(Section('Search Settings')):

            doc.append('Database was searched using {type} at level {lev}{restrict}'.format(type=tp, lev=lev,
                                                                                            restrict=search_restrictions))

            if args.list or args.file:
                with doc.create(Subsection('Input Isolates')):
                    doc.append('Successfully processed isolates:\n {}\n'.format(", ".join(complete)))
                    doc.append('Failed isolates:\n')
                    if len(list(fails.keys())) != 0:

                        fmt = "X[l] X[l]"
                        with doc.create(Tabu(fmt, spread="1pt", pos=["l"])) as data_table:

                            header_row1 = ["Isolate", "Failure Reason"]
                            data_table.add_row(MultiColumn(1, data=header_row1))
                            data_table.add_hline()
                            for reason in fails:
                                for isolate in fails[reason]:
                                    d = [isolate, reason]
                                    data_table.add_row(MultiColumn(2, data=d))
                    else:
                        doc.append('None\n')

            with doc.create(Subsection('Matching Isolates')):
                if len(newisolates) > 40:
                    doc.append(
                        'The above isolates matched to {no} other isolates \n'.format(no=len(newisolates)))
                else:
                    doc.append(
                        'The above isolates matched to the following {no} isolates \n'.format(no=len(newisolates)))
                    fmt = "X[l]X[l]"
                    with doc.create(Tabu(fmt, spread="1pt", pos=["l"])) as data_table:
                        search_level = tp + lev
                        header_row1 = ["Name", search_level]
                        data_table.add_row(MultiColumn(2, data=header_row1))
                        data_table.add_hline()
                        sorted_isolates = sorted(newisolates, key=lambda i: int(metadata['used_id'][i]))
                        print(newisolates)
                        print(sorted_isolates)

                        for i in sorted_isolates:
                            isolate_used_id = metadata['used_id'][i]
                            data = [i, isolate_used_id]
                            data_table.add_row(MultiColumn(2, data=data))

    else:
        with doc.create(Section('Search Settings')):
            doc.append('Database was searched using {type}={ident} at level {lev}{restrict}'.format(type=tp,
                                                                                                    ident=args.identifier,
                                                                                                    lev=lev,
                                                                                                    restrict=search_restrictions))
            with doc.create(Subsection('Matching Isolates')):
                if len(newisolates) > 40:
                    doc.append(
                        'The above settings matched to {no} other isolates \n'.format(no=len(newisolates)))
                else:
                    doc.append(
                        'The above settings matched to the following {no} isolates \n'.format(no=len(newisolates)))
                    doc.append(", ".join(newisolates))
                    fmt = "X[l]X[l]"
                    with doc.create(Tabu(fmt, spread="1pt", pos=["l"])) as data_table:
                        search_level = tp + lev
                        header_row1 = ["Name", search_level]
                        data_table.add_row(MultiColumn(2, data=header_row1))
                        data_table.add_hline()

                        sorted_isolates = sorted(newisolates, key=lambda i: int(metadata['used_id'][i]))
                        print(newisolates)
                        print(sorted_isolates)

                        for i in sorted_isolates:
                            isolate_used_id = metadata['used_id'][i]
                            data = [i, isolate_used_id]
                            data_table.add_row(MultiColumn(2, data=data))

    with doc.create(Section('Graph By Year')):
        with doc.create(TikZ()):
            plot_options = 'height=4cm, width=6cm, grid=major'
            with doc.create(Axis(options=plot_options)) as plot:
                plot.append(Plot(name='model', func='-x^5 - 242'))
                plot.append(Plot(name='estimate', coordinates=coordinates))
    # Generate data table with 'tight' columns

    # with doc.create(Center()) as centered:
    #     with centered.create(Tabu("X[r] X[r]", spread="1in")) as data_table:
    #         header_row1 = ["X", "Y"]
    #         data_table.add_row(header_row1, mapper=[bold])
    #         data_table.add_hline()
    #         row = [randint(0, 1000), randint(0, 1000)]
    #         for i in range(4):
    #             data_table.add_row(row)
    #
    # with doc.create(Center()) as centered:
    #     with centered.create(Tabu("X[r] X[r]", to="4in")) as data_table:
    #         header_row1 = ["X", "Y"]
    #         data_table.add_row(header_row1, mapper=[bold])
    #         data_table.add_hline()
    #         row = [randint(0, 1000), randint(0, 1000)]
    #         for i in range(4):
    #             data_table.add_row(row)

    doc.generate_pdf('MGT report', clean_tex=False)  # make pdf
    tex = doc.dumps()  # make latex file




if __name__ == '__main__':
    main()