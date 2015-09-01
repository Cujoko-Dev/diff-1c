#!/usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from configparser import RawConfigParser
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


__version__ = '1.0.0'


def get_setting(section, key):
    settings_config_file_path_rel = Path('diff-1c.ini')
    if not settings_config_file_path_rel.exists():
        settings_config_file_path_rel = Path(__file__).parent / settings_config_file_path_rel
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

    exe1c = Path(get_setting('General', '1C'))
    if not exe1c.exists():
        raise Exception('Платформа не существует!')
    ib = Path(get_setting('General', 'IB'))
    if not ib.exists():
        raise Exception('Сервисной информационной базы не существует!')
    v8_reader = Path(get_setting('General', 'V8Reader'))
    if not v8_reader.exists():
        raise Exception('V8Reader не существует!')
    gcomp = Path(get_setting('General', 'GComp'))
    if not gcomp.exists():
        raise Exception('GComp не существует!')

    # base
    base_path = Path(args.base)
    base_temp_path = Path(tempfile.mktemp(base_path.suffix))
    shutil.copyfile(str(base_path), str(base_temp_path))

    base_source_path = Path(tempfile.mktemp())
    if not base_source_path.exists():
        base_source_path.mkdir(parents=True)
    else:
        shutil.rmtree(str(base_source_path), ignore_errors=True)

    base_bat_path = Path(tempfile.mktemp('.bat'))
    with base_bat_path.open('w', encoding='cp866') as base_bat:
        base_bat.write('@echo off\n')
        base_path_suffix_lower = base_path.suffix.lower()
        if base_path_suffix_lower in ['.epf', '.erf']:
            base_bat.write('"{}" /F"{}" /DisableStartupMessages /Execute"{}" {}'.format(
                str(exe1c),
                str(ib),
                str(v8_reader),
                '/C"decompile;pathtocf;{};pathout;{};shutdown;convert-mxl2txt;"'.format(
                    str(base_temp_path),
                    str(base_source_path)
                )
            ))
        elif base_path_suffix_lower in ['.ert', '.md']:
            base_bat.write('"{}" -d -F "{}" -DD "{}"'.format(
                str(gcomp),
                str(base_temp_path),
                str(base_source_path)
            ))
    exit_code = subprocess.check_call(['cmd.exe', '/C', str(base_bat_path)])
    if not exit_code == 0:
        raise Exception('Не удалось разобрать файл {}'.format(str(base_path)))

    # mine
    mine_path = Path(args.mine)
    mine_temp_path = Path(tempfile.mktemp(mine_path.suffix))
    shutil.copyfile(str(mine_path), str(mine_temp_path))

    mine_source_path = Path(tempfile.mktemp())
    if not mine_source_path.exists():
        mine_source_path.mkdir(parents=True)
    else:
        shutil.rmtree(str(mine_source_path), ignore_errors=True)

    mine_bat_path = Path(tempfile.mktemp('.bat'))
    with mine_bat_path.open('w', encoding='cp866') as mine_bat:
        mine_bat.write('@echo off\n')
        mine_path_suffix_lower = base_path.suffix.lower()
        if mine_path_suffix_lower in ['.epf', '.erf']:
            mine_bat.write('"{}" /F"{}" /DisableStartupMessages /Execute"{}" {}'.format(
                str(exe1c),
                str(ib),
                str(v8_reader),
                '/C"decompile;pathtocf;{};pathout;{};shutdown;convert-mxl2txt;"'.format(
                    str(mine_temp_path),
                    str(mine_source_path)
                )
            ))
        elif mine_path_suffix_lower in ['.ert', '.md']:
            mine_bat.write('"{}" -d -F "{}" -DD "{}"'.format(
                str(gcomp),
                str(mine_temp_path),
                str(mine_source_path)
            ))
    exit_code = subprocess.check_call(['cmd.exe', '/C', str(mine_bat_path)])
    if not exit_code == 0:
        raise Exception('Не удалось разобрать файл {}'.format(str(mine_path)))

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
    if tool_args == None:
        raise Exception('Не удалось сравнить файлы {} и {}'.format(str(base_path), str(mine_path)))
    exit_code = subprocess.check_call(tool_args)
    if not exit_code == 0:
        raise Exception('Не удалось сравнить файлы {} и {}'.format(str(base_path), str(mine_path)))


if __name__ == '__main__':
    sys.exit(main())