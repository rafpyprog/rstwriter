''' Test for RstWriter package '''
import os
import sys


sys.path.append(os.path.join('..', 'rstwriter'))
import pandas as pd
import pytest
from rstwriter import RstWriter


REPORT_FILE = 'report.rst'
TESTS_PATH = os.path.dirname(os.path.realpath(__file__))



@pytest.fixture
def css(scope='module'):
    css_file = 'test.css'
    with open('test.css', 'w') as testcss:
        testcss.write('p {color : blue;}\n')
    yield css_file
    print('Cleaning css test file.')
    os.remove(css_file)


def test_create_rstwriter():
    report = RstWriter(REPORT_FILE)
    assert report.rstfile == REPORT_FILE


def test_write_to_rst_from_list():
    foo_list = ['Test write to rst from list 1.\n',
                'Test write to rst from list 2.\n']
    report = RstWriter(REPORT_FILE)
    assert report.write(foo_list) is True


def test_write_to_rst_from_string():
    foo_list = 'Test write to rst from string.'
    report = RstWriter(REPORT_FILE)
    assert report.write(foo_list) is True


def test_add_blank_line():
    blank_line = '\n'
    report = RstWriter(REPORT_FILE)
    report.add_blank_line()
    with open(REPORT_FILE, 'r') as rst:
        content = rst.read()
    print(content)
    assert content == blank_line


def test_add_ccs_file(css):
    css_file = css
    report = RstWriter(REPORT_FILE)
    report.css = css_file
    assert report.css == css_file


def test_open_header_identation():
    report = RstWriter(REPORT_FILE)
    report.header('open')
    assert report.indent == '   '


def test_close_header_unindent():
    report = RstWriter(REPORT_FILE)
    report.header('close')
    assert report.indent == ''


def load_table(mycsv):
    mycsv = os.path.join(TESTS_PATH, mycsv)
    table = pd.read_csv(mycsv, delimiter=';', encoding="ISO-8859-1")
    return table


def test_table_only_strings_same_width():
    csv = load_table('table1.csv')
    report = RstWriter(REPORT_FILE)
    report.table(csv)
    report.publish('html')


def test_table_only_strings_diff_width():
    csv = load_table('table2.csv')
    report = RstWriter(REPORT_FILE)
    report.table(csv)
    report.publish('html')


def test_table_only_strings_diff_width_header_columns():
    csv = load_table('table3.csv')
    report = RstWriter(REPORT_FILE)
    report.table(csv)
    report.publish('html')


def test_table_with_floats_and_ints():
    csv = load_table('table4.csv')
    csv['COL1'] = csv['COL1'].astype(float)
    csv['COL5_'] = csv['COL5_'].astype(int)
    report = RstWriter(REPORT_FILE)
    report.table(csv)
    report.publish('html')


def test_table_comma_as_decimal():
    decimal = ','
    csv = load_table('table4.csv')
    csv['COL1'] = csv['COL1'].astype(float)
    csv['COL5_'] = csv['COL5_'].astype(int)
    report = RstWriter(REPORT_FILE)
    report.table(csv, decimal=decimal)
    report.publish('html')


def test_table_thousands_separator():
    thousands = True
    csv = load_table('table4.csv')
    csv['COL1'] = csv['COL1'].astype(float)
    csv['COL5_'] = csv['COL5_'].astype(int)
    report = RstWriter(REPORT_FILE)
    report.table(csv, thousands=thousands)
    report.publish('html')


def test_table_decimal_with_thousands_separator():
    decimal = ','
    thousands = True
    csv = load_table('table4.csv')
    csv['COL1'] = csv['COL1'].astype(float)
    csv['COL5_'] = csv['COL5_'].astype(int)
    report = RstWriter(REPORT_FILE)
    report.table(csv, decimal=decimal, thousands=thousands)
    report.publish('html')


def teardown_module():
    os.remove(REPORT_FILE)


