# -*- coding: utf-8 -*-
import sys

from cli import get_argparser


def run() -> None:
    argparser = get_argparser()
    args = argparser.parse_args(sys.argv[1:])
    args.func(args)