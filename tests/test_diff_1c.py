# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from diff_1c.cli import get_argparser
from diff_1c.main import run


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = get_argparser()

    def test_run(self):
        args = self.parser.parse_args('data/test.epf data/test.epf'.split())
        run(args)
