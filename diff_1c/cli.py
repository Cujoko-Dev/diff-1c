# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from argparse import ArgumentParser

from diff_1c import __version__
from diff_1c.main import run


def get_argparser():
    parser = ArgumentParser(prog='diff1c', description='Diff utility for 1C:Enterprise files', add_help=False)
    parser.set_defaults(func=run)
    parser.add_argument(
        '-h', '--help',
        action='help',
        help='Show this help message and exit'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s, ver. {0}'.format(__version__),
        help='Show version'
    )
    parser.add_argument(
        '--tool',
        choices=['KDiff3', 'AraxisMerge', 'WinMerge', 'ExamDiff'],
        default='KDiff3',
        help='external diff program'
    )
    parser.add_argument(
        '--name-format',
        choices=['TortoiseGit'],
        default='TortoiseGit',
        help='name format'
    )
    parser.add_argument(
        '--bname',
        help='the window title for the base file'
    )
    parser.add_argument(
        '--yname',
        help='the window title for your file'
    )
    parser.add_argument(
        'base',
        help='the original file without your changes'
    )
    parser.add_argument(
        'mine',
        help='your own file, with your changes'
    )
    return parser
