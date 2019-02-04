# -*- coding: utf-8 -*-
import unittest

from diff_1c.cli import get_argparser
from diff_1c.main import run


class MainTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = get_argparser()

    def test_run(self) -> None:
        args = self.parser.parse_args('data/test.epf data/test.epf'.split())
        run(args)
