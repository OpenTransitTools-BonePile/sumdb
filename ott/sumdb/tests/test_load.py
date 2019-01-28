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
        # self.db = self.load_pgsql() if self.DO_PG else self.load_sqlite()
        pass

    def test_load_zipcar(self):
        c = True
        self.assertTrue(c)
