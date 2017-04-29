#! python3.6
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from appdirs import user_data_dir
from configparser import RawConfigParser
import os
from parse_1c_build import Parser
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


__version__ = '3.1.1'

APP_AUTHOR = 'util-1c'
APP_NAME = 'diff-1c'


def get_setting(section, key):
    settings_config_file_path = Path('settings.ini')
    if not settings_config_file_path.exists():
        settings_config_file_path = Path(user_data_dir(APP_NAME, APP_AUTHOR, roaming=True)) / \
                                        settings_config_file_path
        if not settings_config_file_path.exists():
            raise Exception('Файл настроек не существует!')
    config = RawConfigParser()
    config.optionxform = lambda option: option
    config.read(str(settings_config_file_path), 'utf-8')

    return config[section][key]  # fixme


def main():
    argparser = ArgumentParser()

    argparser.add_argument('-v', '--version', action='version', version='%(prog)s, ver. {}'.format(__version__))
    argparser.add_argument('--debug', action='store_true', default=False, help='if this option exists '
                                                                               'then debug mode is enabled')
    argparser.add_argument('--tool', choices=['KDiff3', 'AraxisMerge', 'WinMerge', 'ExamDiff'], default='KDiff3',
                           help='external diff program')
    argparser.add_argument('--bname', help='the window title for the base file')
    argparser.add_argument('--yname', help='the window title for your file')
    argparser.add_argument('base', help='the original file without your changes')
    argparser.add_argument('mine', help='your own file, with your changes')

    args = argparser.parse_args()

    if args.debug:
        import sys
        sys.path.append('C:\\Python34\\pycharm-debug-py3k.egg')

        import pydevd
        pydevd.settrace(port=10050)

    parser = Parser()

    # base
    base_file_path = Path(args.base)

    base_temp_file, base_temp_file_name = tempfile.mkstemp(base_file_path.suffix)
    os.close(base_temp_file)

    base_temp_file_path = Path(base_temp_file_name)
    shutil.copyfile(str(base_file_path), str(base_temp_file_path))

    base_source_dir_path = Path(tempfile.mkdtemp())

    parser.parse(base_temp_file_path, base_source_dir_path)

    base_temp_file_path.unlink()

    # mine
    mine_file_path = Path(args.mine)

    mine_temp_file, mine_temp_file_name = tempfile.mkstemp(mine_file_path.suffix)
    os.close(mine_temp_file)

    mine_temp_file_path = Path(mine_temp_file_name)
    shutil.copyfile(str(mine_file_path), str(mine_temp_file_path))

    mine_source_dir_path = Path(tempfile.mkdtemp())

    parser.parse(mine_temp_file_path, mine_source_dir_path)

    mine_temp_file_path.unlink()

    tool_args = None
    if args.tool == 'KDiff3':
        tool_file_path = Path(get_setting('General', 'KDiff3'))
        tool_args = [
            str(tool_file_path),
            '--cs',
            'EncodingForA=windows-1251',
            '--cs',
            'EncodingForB=windows-1251',
            str(base_source_dir_path),
            str(mine_source_dir_path)
        ]
        if args.bname is not None:
            tool_args += [
                '--L1',
                args.bname
            ]
        if args.yname is not None:
            tool_args += [
                '--L2',
                args.yname
            ]
    elif args.tool == 'AraxisMerge':
        tool_file_path = Path(get_setting('General', 'AraxisMerge'))
        tool_args = [
            str(tool_file_path),
            '/max',
            '/wait',
            str(base_source_dir_path),
            str(mine_source_dir_path)
        ]
        if args.bname is not None:
            tool_args += [
                '/title1:{}'.format(args.bname)
            ]
        if args.yname is not None:
            tool_args += [
                '/title2:{}'.format(args.yname)
            ]
    elif args.tool == 'WinMerge':
        tool_file_path = Path(get_setting('General', 'WinMerge'))
        tool_args = [
            str(tool_file_path),
            '-e',
            '-ub',
            str(base_source_dir_path),
            str(mine_source_dir_path)
        ]
        if args.bname is not None:
            tool_args += [
                '-dl',
                args.bname
            ]
        if args.yname is not None:
            tool_args += [
                '-dr',
                args.yname
            ]
    elif args.tool == 'ExamDiff':
        tool_file_path = Path(get_setting('General', 'ExamDiff'))
        tool_args = [
            str(tool_file_path),
            str(base_source_dir_path),
            str(mine_source_dir_path)
        ]
        if args.bname is not None:
            tool_args += [
                '--left_display_name:{}'.format(args.bname)
            ]
        if args.yname is not None:
            tool_args += [
                '--right_display_name:{}'.format(args.yname)
            ]

    if tool_args is None:
        raise Exception('Не удалось сравнить файлы {} и {}'.format(str(base_file_path), str(mine_file_path)))

    exit_code = subprocess.check_call(tool_args)
    if not exit_code == 0:
        raise Exception('Не удалось сравнить файлы {} и {}'.format(str(base_file_path), str(mine_file_path)))


if __name__ == '__main__':
    sys.exit(main())
