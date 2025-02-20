# -*- coding: utf-8 -*-

"""Ядро"""


import sys

from cjk_commons.logging_ import add_loggers

from diff_1c import logger
from diff_1c.cli import get_argparser


def run() -> None:
    """Запустить"""

    argparser = get_argparser()
    args = argparser.parse_args(sys.argv[1:])

    add_loggers(args, logger)

    args.func(args)
