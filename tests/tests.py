''' Test for RstWriter package '''
import os
import sys


sys.path.append(os.path.join('..', 'rstwriter'))

import pytest
from rstwriter import RstWriter


REPORT_FILE = 'report.rst'


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


def teardown_module():
    os.remove(REPORT_FILE)
