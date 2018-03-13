# -*- coding: utf-8 -*-
import unittest

from diff_1c import run
from diff_1c.cli import get_argparser


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = get_argparser()

    def test_run(self):
        args = self.parser.parse_args('data/test.epf data/test.epf'.split())

        run(args)