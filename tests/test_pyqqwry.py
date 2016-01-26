# -*- coding: utf8 -*-
"""
    tests.test_pyqqwry
    ~~~~~~~~~~~~~~~~~~

    Pyqqwry unittests
"""

import os
import unittest
from pyqqwry.qqwry import QQWry


class TestQQWry(unittest.TestCase):

    qqwry = None

    @classmethod
    def setUpClass(cls):
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, "qqwry.dat")
        cls.qqwry = QQWry(path)

    def test_query(self):
        """Test `QQWry.query` method.
        """
        rst = self.qqwry.query("101.81.24.18")
        self.assertEqual(len(rst), 2)
        self.assertEqual(rst[0], "上海市徐汇区")
        self.assertEqual(rst[1], "电信")

    def test_query_one_two(self):
        """Test redirect from one to region two.
        """
        rst = self.qqwry.query("122.100.128.17")
        self.assertEqual(len(rst), 2)
        self.assertEqual(rst[0], "澳门")
        self.assertEqual(rst[1], "特别行政区")
