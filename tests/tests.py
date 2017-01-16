''' Test for RstWriter package '''
import os
import sys

sys.path.append(os.path.join('..', 'rstwriter'))

from rstwriter import RstWriter


REPORT_FILE = 'report.rst'


def test_create_rstwriter():
    report = RstWriter(REPORT_FILE)
    assert report.rstfile == REPORT_FILE


def test_write_to_rst_from_list():
    foo_list = ['Test write to rst from list 1.\n',
                'Test write to rst from list 2.\n',]
    report = RstWriter(REPORT_FILE)
    assert report.write(foo_list) == True


def test_write_to_rst_from_string():
    foo_list = 'Test write to rst from string.'
    report = RstWriter(REPORT_FILE)
    assert report.write(foo_list) == True


def test_add_blank_line():
    blank_line = '\n'
    report = RstWriter(REPORT_FILE)
    report.add_blank_line()
    with open(REPORT_FILE, 'r') as rst:
        content = rst.read()
    print(content)
    assert content == blank_line


def teardown_module():
    os.remove(REPORT_FILE)
