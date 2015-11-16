#! python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from configparser import RawConfigParser
from decompiler1cwrapper import Decompiler
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


__version__ = '2.0.1'


def get_setting(section, key):
    settings_config_file_path_rel = Path('diff1c.ini')
    if not settings_config_file_path_rel.exists():
        settings_config_file_path_rel = Path.home() / settings_config_file_path_rel
        if not settings_config_file_path_rel.exists():
            raise Exception('Файл настроек не существует!')
    config = RawConfigParser()
    config.optionxform = lambda option: option
    config.read(str(settings_config_file_path_rel), 'utf-8')
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

    decompiler = Decompiler()

    # base
    base_path = Path(args.base)
    base_temp_path = Path(tempfile.mktemp(base_path.suffix))
    shutil.copyfile(str(base_path), str(base_temp_path))

    base_source_path = Path(tempfile.mktemp())
    if not base_source_path.exists():
        base_source_path.mkdir(parents=True)
    else:
        shutil.rmtree(str(base_source_path), ignore_errors=True)

    decompiler.perform(base_temp_path, base_source_path)

    base_temp_path.unlink()

    # mine
    mine_path = Path(args.mine)
    mine_temp_path = Path(tempfile.mktemp(mine_path.suffix))
    shutil.copyfile(str(mine_path), str(mine_temp_path))

    mine_source_path = Path(tempfile.mktemp())
    if not mine_source_path.exists():
        mine_source_path.mkdir(parents=True)
    else:
        shutil.rmtree(str(mine_source_path), ignore_errors=True)

    decompiler.perform(mine_temp_path, mine_source_path)

    mine_temp_path.unlink()

    tool_args = None
    if args.tool == 'KDiff3':
        tool_path = Path(get_setting('General', 'KDiff3'))
        tool_args = [
            str(tool_path),
            '--cs',
            'EncodingForA=windows-1251',
            '--cs',
            'EncodingForB=windows-1251',
            str(base_source_path),
            str(mine_source_path)
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
        tool_path = Path(get_setting('General', 'AraxisMerge'))
        tool_args = [
            str(tool_path),
            '/max',
            '/wait',
            str(base_source_path),
            str(mine_source_path)
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
        tool_path = Path(get_setting('General', 'WinMerge'))
        tool_args = [
            str(tool_path),
            '-e',
            '-ub',
            str(base_source_path),
            str(mine_source_path)
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
        tool_path = Path(get_setting('General', 'ExamDiff'))
        tool_args = [
            str(tool_path),
            str(base_source_path),
            str(mine_source_path)
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
        raise Exception('Не удалось сравнить файлы {} и {}'.format(str(base_path), str(mine_path)))
    exit_code = subprocess.check_call(tool_args)
    if not exit_code == 0:
        raise Exception('Не удалось сравнить файлы {} и {}'.format(str(base_path), str(mine_path)))


if __name__ == '__main__':
    sys.exit(main())
