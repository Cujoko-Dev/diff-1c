# -*- coding: utf-8 -*-
from collections import OrderedDict
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Any

from appdirs import site_data_dir, user_data_dir
from parse_1c_build import Parser
import yaml
import yodl

__version__ = '4.0.0'

APP_AUTHOR = 'util-1c'
APP_NAME = 'diff-1c'


def get_settings() -> OrderedDict:
    # Settings
    settings_file_path = Path('settings.yaml')
    if not settings_file_path.is_file():
        settings_file_path = Path(user_data_dir(APP_NAME, APP_AUTHOR, roaming=True)) / settings_file_path.name
        if not settings_file_path.is_file():
            settings_file_path = Path(site_data_dir(APP_NAME, APP_AUTHOR)) / settings_file_path.name
            if not settings_file_path.is_file():
                raise SettingsException('Settings file does not exist!')

    with settings_file_path.open(encoding='utf-8') as settings_file:
        settings = yaml.load(settings_file, yodl.OrderedDictYAMLLoader)

    return settings


def run(args: Any) -> None:
    settings = get_settings()

    parser = Parser()

    exclude_file_names = settings['General']['ExcludeFiles'].split(':')

    # base
    base_is_excluded = False

    base_file_path = Path(args.base)

    if args.name_format == 'TortoiseGit':
        bname_file_path = Path(args.bname.split(':')[0])
    else:
        bname_file_path = Path(args.bname.split(':')[0])

    if bname_file_path.name not in exclude_file_names:
        base_temp_file, base_temp_file_name = tempfile.mkstemp(base_file_path.suffix)
        os.close(base_temp_file)

        base_temp_file_path = Path(base_temp_file_name)
        shutil.copyfile(str(base_file_path), str(base_temp_file_path))

        base_source_dir_path = Path(tempfile.mkdtemp())

        parser.parse(base_temp_file_path, base_source_dir_path)

        base_temp_file_path.unlink()
    else:
        base_is_excluded = True

    # mine
    mine_is_excluded = False

    mine_file_path = Path(args.mine)

    if args.name_format == 'TortoiseGit':
        yname_file_path = Path(args.yname.split(':')[0])
    else:
        yname_file_path = Path(args.yname.split(':')[0])

    if yname_file_path.name not in exclude_file_names:
        mine_temp_file, mine_temp_file_name = tempfile.mkstemp(mine_file_path.suffix)
        os.close(mine_temp_file)

        mine_temp_file_path = Path(mine_temp_file_name)
        shutil.copyfile(str(mine_file_path), str(mine_temp_file_path))

        mine_source_dir_path = Path(tempfile.mkdtemp())

        parser.parse(mine_temp_file_path, mine_source_dir_path)

        mine_temp_file_path.unlink()
    else:
        mine_is_excluded = True

    tool_args = None
    if args.tool == 'KDiff3':
        tool_file_path = Path(settings['General']['KDiff3'])

        tool_args = [str(tool_file_path)]

        # base
        if base_is_excluded:
            tool_args += ['--cs', 'EncodingForA=UTF-8', str(base_file_path)]
        else:
            tool_args += ['--cs', 'EncodingForA=windows-1251', str(base_source_dir_path)]

        if args.bname is not None:
            tool_args += ['--L1', args.bname]

        # mine
        if mine_is_excluded:
            tool_args += ['--cs', 'EncodingForB=UTF-8', str(mine_file_path)]
        else:
            tool_args += ['--cs', 'EncodingForB=windows-1251', str(mine_source_dir_path)]

        if args.yname is not None:
            tool_args += ['--L2', args.yname]
    elif args.tool == 'AraxisMerge':
        tool_file_path = Path(settings['General']['AraxisMerge'])

        tool_args = [str(tool_file_path), '/max', '/wait']

        # base
        if base_is_excluded:
            tool_args += [str(base_file_path)]
        else:
            tool_args += [str(base_source_dir_path)]

        if args.bname is not None:
            tool_args += ['/title1:{}'.format(args.bname)]

        # mine
        if mine_is_excluded:
            tool_args += [str(mine_file_path)]
        else:
            tool_args += [str(mine_source_dir_path)]

        if args.yname is not None:
            tool_args += ['/title2:{}'.format(args.yname)]
    elif args.tool == 'WinMerge':
        tool_file_path = Path(settings['General']['WinMerge'])

        tool_args = [str(tool_file_path), '-e', '-ub']

        # base
        if base_is_excluded:
            tool_args += [str(base_file_path)]
        else:
            tool_args += [str(base_source_dir_path)]

        if args.bname is not None:
            tool_args += ['-dl', args.bname]

        # mine
        if mine_is_excluded:
            tool_args += [str(mine_file_path)]
        else:
            tool_args += [str(mine_source_dir_path)]

        if args.yname is not None:
            tool_args += ['-dr', args.yname]
    elif args.tool == 'ExamDiff':
        tool_file_path = Path(settings['General']['ExamDiff'])

        tool_args = [str(tool_file_path)]

        # base
        if base_is_excluded:
            tool_args += [str(base_file_path)]
        else:
            tool_args += [str(base_source_dir_path)]

        if args.bname is not None:
            tool_args += ['--left_display_name:{}'.format(args.bname)]

        # mine
        if mine_is_excluded:
            tool_args += [str(mine_file_path)]
        else:
            tool_args += [str(mine_source_dir_path)]

        if args.yname is not None:
            tool_args += ['--right_display_name:{}'.format(args.yname)]

    if tool_args is None:
        raise Exception('Не удалось сравнить файлы {} и {}'.format(str(base_file_path), str(mine_file_path)))

    exit_code = subprocess.check_call(tool_args)
    if not exit_code == 0:
        raise Exception('Не удалось сравнить файлы {} и {}'.format(str(base_file_path), str(mine_file_path)))


class SettingsException(Exception):
    pass
