''' Test for RstWriter package '''
import os
import sys

sys.path.append(os.path.join('..', 'rstwriter'))

from rstwriter import RstWriter


REPORT_FILE = 'report.rst'


def test_rstwriter():
    expectedfile = REPORT_FILE
    report = RstWriter(expectedfile)
    assert report.rstfile == REPORT_FILE


def teardown_module():
    os.remove(REPORT_FILE)
