''' RST report writer for the pandas Library.'''
import os

import locale
from docutils.core import publish_cmdline


class RstWriter():
    ''' Writes titles, paragraphs and tables into a rst document
    set on init. User can publish document to html file.'''
    def __init__(self, rstfile):
        self.indent = ('')
        self.css = None
        self.containers = ('header', 'footnote')
        self.header_status = ('closed')
        self.rstfile = rstfile
        self.create_rst()

    def create_rst(self):
        ''' Creates an empty rst file '''
        createrst = open(self.rstfile, 'w').close
        return createrst

    def write(self, text):
        ''' Writes content in the .rst file '''
        with open(self.rstfile, 'a') as rstfile:
            if isinstance(text, list) or isinstance(text, tuple):
                for txt in text:
                    rstfile.write(txt)
            else:
                rstfile.write(text)
        return True

    def style(self, styles, text):
        ''' Use this class to style an element with a CSS class '''
        container_elements = ('header', 'footnote')
        styles = styles.strip().split(' ')

        if len(styles) > 1:
            for styleindex, style in enumerate(styles):
                if style in container_elements:
                    container = styles.pop(styleindex)
                    countcss = len(styles)
                    if countcss == 0:
                        return '.. {}:: {}'.format(container, text)
                    else:
                        css = ' '.join(styles)
                        return '.. class:: {}\n\n   {}'.format(css, text)
        else:
            return '{}.. class:: {}\n\n{}'.format(self.indent, styles[0], text)

    def add_blank_line(self):
        ''' Writes a blank line in the rst file '''
        self.write('\n')

    def add_line_break(self, text):
        ''' Adds a line break at the end of the text '''
        return text + '\n'

    def set_identation(self, level):
        ''' Sets indentation for nested elements. '''
        self.indent = ' ' * 3 * level

    def header(self, status):
        ' Opens an close a header container'
        if status == 'open':
            self.write('.. header::\n')
            self.set_identation(1)
        elif status == 'close':
            self.set_identation(0)

    def paragraph(self, text, style=None):
        ' Writes a text paragraph in the rst document.'
        text = self.indent + text + '\n\n'
        if style is None:
            self.write(text)
        else:
            text = self.style(style, text)
            self.write(text)

    def title(self, header, text):
        ''' Writes a title in the document, using the level of the
        header received.'''
        headers = {'h1': '=', 'h2': '-', 'h3': '`', 'h4': ':',
                   'h5': '.', 'h6': "'"}
        try:
            assert header in headers
        except AssertionError:
            print('''{} is not valid header. Shoul be h1, h2, h3, h4, h5,
                  h6'''.format(header))
        textsize = len(text)
        text = self.add_line_break(text)
        titlemark = self.add_line_break(headers[header] * textsize)
        self.write([text, titlemark])

    def table(self, dataframe, thousands=False, decimal='.'):
        ''' Parse Pandas dataFrame, convert to rst and writes to file '''

        def column_to_float(column, thousands=False, decimal='.'):
            ''' Convert column with float type values to formated string '''
            if os.name == 'posix':
                locales = {'pt_BR': 'pt_BR.UTF-8', 'en_US': 'en_US.UTF-8'}
            else:
                locales = {'pt_PT': 'Portuguese', 'en_US': 'English'}

            if decimal == ',':
                locale.setlocale(locale.LC_ALL, locales['pt_PT'])
            else:
                locale.setlocale(locale.LC_ALL, locales['en_US'])

            # Converts float to formated string
            column = column.map(lambda x: locale.format('%.2f', x, thousands))
            return column

        dfcopy = dataframe.copy()
        # converts all table to string type
        for column in dfcopy:
            if dfcopy[column].dtype == 'float64':
                dfcopy[column] = column_to_float(dfcopy[column], thousands,
                                                 decimal)
            else:
                dfcopy[column] = dfcopy[column].map(str)

        # get table header and apply bold format
        headers = list(dfcopy.columns.values)
        tableheader = ['**' + th + '**' for th in headers]

        # get table data lines
        tablelines = dfcopy.iterrows()
        tabledata = []
        for line in tablelines:
            tabledata.append(list(line[1]))
        tabledata.insert(0, tableheader)

        # width of each columns based on biggest cell
        cols = list(zip(*tabledata))
        colswidth = [len(item) for item in [max(col, key=len) for col in cols]]

        # writes table to rst, add 4 to with because of * to bold the header
        tableborder = ' '.join('=' * width for width in colswidth) + '\n'
        self.write(tableborder)

        for line in tabledata:
            for cellindex, cell in enumerate(line):
                if cellindex > 0:
                    # number of white spaces to align the value on column
                    # add 4 because of * in headers
                    spaces = (colswidth[cellindex - 1] -
                              len(line[cellindex - 1]) + 1)
                    self.write(' ' * spaces + cell)
                else:
                    self.write(cell)
            self.write('\n')
        self.write(tableborder + '\n')

    def publish(self, filetype):
        ''' Creates final report from the .rst file '''
        outputfile = '{}.{}'.format(self.rstfile.split('.')[0], filetype)
        description = 'rstWriter'
        if self.css is None:
            cssarg = '--stylesheet=html4css1.css'
        else:
            cssarg = '--stylesheet=html4css1.css, {}'.format(self.css)
        publish_cmdline(writer_name=filetype, description=description,
                        argv=[self.rstfile, outputfile, cssarg])
