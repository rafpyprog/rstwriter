from docutils.core import publish_cmdline, default_description

import pandas as pd


class rstWriter():

    def __init__(self, rstFile):
        self.indent = ('')
        self.css = None
        self.CONTAINERS = ('header', 'footnote')
        self.header_status = ('closed')
        self.rstFile = rstFile
        open(self.rstFile, 'w').close

    def write(self, text):
        with open(self.rstFile, 'a') as rstFile:
            if type(text) is list or type(text) is tuple:
                for txt in text:
                    rstFile.write(txt)
            else:
                rstFile.write(text)

    def check_styles_has_container(self, styles):
        return any([True if s in self.CONTAINERS else False for s in styles])

    def style(self, styles, text):
        CONTAINER_ELEMENTS = ('header', 'footnote')
        styles = styles.strip().split(' ')

        if len(styles) > 1:
            for n, style in enumerate(styles):
                if style in CONTAINER_ELEMENTS:
                    container = styles.pop(n)
                    countCSS = len(styles)
                    if countCSS == 0:
                        return '.. {}:: {}'.format(container, text)
                    else:
                        css = ' '.join(styles)
                        return '.. class:: {}\n\n   {}'.format(container,
                                                               css, text)
        else:
            return '{}.. class:: {}\n\n{}'.format(self.indent, styles[0], text)

    def add_blank_line(self):
        self.write('\n')

    def add_line_break(self, text):
        return text + '\n'

    def set_identation(self, level):
        self.indent = ' ' * 3 * level

    def header(self, status):
        if status == 'open':
            self.write('.. header::\n')
            self.set_identation(1)
        elif status == 'close':
            self.set_identation(0)

    def paragraph(self, text, style=None):
        text = self.indent + text + '\n\n'
        if style is None:
            self.write(text)
        else:
            text = self.style(style, text)
            self.write(text)

    def title(self, header, text):
        headers = {'h1': '=', 'h2': '-', 'h3': '`', 'h4': ':',
                   'h5': '.', 'h6': "'"}
        try:
            assert header in headers
        except:
            print('''{} is not valid header. Shoul be h1, h2, h3, h4, h5,
                  h6'''.format(header))
        textSize = len(text)
        text = self.add_line_break(text)
        titleMark = self.add_line_break(headers[header] * textSize)
        self.write([text, titleMark])

    def table(self, dataFrame):
        # converts all table to strig type
        for column in dataFrame:
            dataFrame[column] = dataFrame[column].map(str)

        # get table header
        tableHeader = list(dataFrame.columns.values)

        # get table data lines
        tableLines = dataFrame.iterrows()
        tableData = []
        for line in tableLines:
            tableData.append(list(line[1]))
        tableData.insert(0, tableHeader)

        # width of each columns based on biggest cell
        cols = list(zip(*tableData))
        colsWidth = [len(item) for item in [max(col, key=len) for col in cols]]
        tableData.pop(0)
        # writes table to rst, add 4 to with because of * to bold the header
        tableBorder = ' '.join('=' * (width + 4) for width in colsWidth) + '\n'
        self.write(tableBorder)
        # table header in bold
        self.write(' '.join('**' + th + '**' for th in tableHeader) + '\n')
        for line in tableData:
            for n, cell in enumerate(line):
                if n > 0:
                    # number of white spaces to align the value on column
                    # add 4 because of * in headers
                    spaces = colsWidth[n - 1] - len(line[n - 1]) + 1 + 4
                    self.write(' ' * spaces + cell)
                else:
                    self.write(cell)
            self.write('\n')
        self.write(tableBorder + '\n')

    def publish(self, format):
        outputFile = '{}.{}'.format(self.rstFile.split('.')[0], format)
        description = 'rstWriter'
        if self.css is None:
            cssarg = '--stylesheet=html4css1.css'
        else:
            cssarg = '--stylesheet=html4css1.css, {}'.format(self.css)
        publish_cmdline(writer_name=format, description=description,
                        argv=[self.rstFile, outputFile, cssarg])
