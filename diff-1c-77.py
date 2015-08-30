#!/usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from configparser import RawConfigParser
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


__version__ = '0.1.0'


def get_setting(section, key):
    settings_config_file_path_rel = Path('diff-1c-77.ini')
    if not settings_config_file_path_rel.exists():
        settings_config_file_path_rel = Path(__file__).parent / settings_config_file_path_rel
        if not settings_config_file_path_rel.exists():
            raise Exception('Файл настроек не существует!')
    config = RawConfigParser()
    config.optionxform = lambda option: option
    config.read(str(settings_config_file_path_rel), 'utf-8')
    return config[section][key]


def main():
    argparser = ArgumentParser()
    argparser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__version__))
    argparser.add_argument('file1')
    argparser.add_argument('file2')
    argparser.add_argument('--debug', action='store_true', default=False)
    args = argparser.parse_args()

    if args.debug:
        import sys
        sys.path.append('C:\\Python34\\pycharm-debug-py3k.egg')

        import pydevd
        pydevd.settrace(port=10050)  # todo

    gcomp = Path(get_setting('General', 'GComp'))

    # file1
    file1 = Path(args.file1)
    file1_temp = Path(tempfile.mktemp(file1.suffix))
    shutil.copyfile(str(file1), str(file1_temp))

    file1_source_folder = Path(tempfile.mktemp())
    if not file1_source_folder.exists():
        file1_source_folder.mkdir(parents=True)
    else:
        shutil.rmtree(str(file1_source_folder), ignore_errors=True)  # fixme

    file1_bat_file = Path(tempfile.mktemp('.bat'))
    with file1_bat_file.open('w', encoding='cp866') as file1_bat_file_temp:
        file1_bat_file_temp.write('@echo off\n')
        file1_bat_file_temp.write('"{}" -d -F "{}" -DD "{}"'.format(  # fixme
            str(gcomp),
            str(file1_temp),
            str(file1_source_folder)
        ))
    exit_code = subprocess.check_call(['cmd.exe', '/C', str(file1_bat_file)])  # fixme
    if not exit_code == 0:
        raise Exception('Не удалось разобрать файл {}'.format(str(file1)))  # fixme

    # file2
    file2 = Path(args.file2)
    file2_temp = Path(tempfile.mktemp(file2.suffix))
    shutil.copyfile(str(file2), str(file2_temp))

    file2_source_folder = Path(tempfile.mktemp())
    if not file2_source_folder.exists():
        file2_source_folder.mkdir(parents=True)
    else:
        shutil.rmtree(str(file2_source_folder), ignore_errors=True)  # fixme

    file2_bat_file = Path(tempfile.mktemp('.bat'))
    with file2_bat_file.open('w', encoding='cp866') as file2_bat_file_temp:
        file2_bat_file_temp.write('@echo off\n')
        file2_bat_file_temp.write('"{}" -d -F "{}" -DD "{}"'.format(  # fixme
            str(gcomp),
            str(file2_temp),
            str(file2_source_folder)
        ))
    exit_code = subprocess.check_call(['cmd.exe', '/C', str(file2_bat_file)])  # fixme
    if not exit_code == 0:
        raise Exception('Не удалось разобрать файл {}'.format(str(file2)))  # fixme

    kdiff3 = Path(get_setting('General', 'KDiff3'))
    exit_code = subprocess.check_call([str(kdiff3), str(file1_source_folder), str(file2_source_folder)])
    if not exit_code == 0:
        raise Exception('Не удалось сравнить файлы {} и {}'.format(str(file1), str(file2)))  # fixme


if __name__ == '__main__':
    sys.exit(main())