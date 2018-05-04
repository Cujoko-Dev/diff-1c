# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from diff_1c.cli import get_argparser


def run():
    argparser = get_argparser()
    args = argparser.parse_args(sys.argv[1:])
    args.func(args)
