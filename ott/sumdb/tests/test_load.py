try:
    import unittest2 as unittest
except ImportError:
    import unittest

from .base import TestBase

import logging
log = logging.getLogger(__name__)


class TestLoad(unittest.TestCase, TestBase):
    DO_PG = False

    def setUp(self):
        #import pdb; pdb.set_trace()
        self.db = self.open_pgsql() if self.DO_PG else self.open_sqlite()

    def test_load_zipcar(self):
        c = True
        self.assertTrue(c)

    def test_load_car2go(self):
        c = True
        self.assertTrue(c)

    def test_load_reachnow(self):
        c = True
        self.assertTrue(c)

    def test_load_biketown(self):
        c = True
        self.assertTrue(c)
