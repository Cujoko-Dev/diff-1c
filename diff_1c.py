# -*- coding: utf-8 -*-
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Any

from cujoko_commons import get_settings
from parse_1c_build.parse import Parser

__version__ = '4.0.0'

APP_AUTHOR = 'util-1c'
APP_NAME = 'diff-1c'


class DiffParser(Parser):
    def run(self) -> None:
        exclude_file_names = self.settings_general['ExcludeFiles'].split(':')

        # base
        base_is_excluded = False

        base_file_path = Path(self.args.base)

        if self.args.name_format == 'TortoiseGit':
            bname_file_path = Path(self.args.bname.split(':')[0])
        else:
            bname_file_path = Path(self.args.bname.split(':')[0])

        if bname_file_path.name not in exclude_file_names:
            base_temp_file, base_temp_file_name = tempfile.mkstemp(base_file_path.suffix)
            os.close(base_temp_file)

            base_temp_file_path = Path(base_temp_file_name)
            shutil.copyfile(str(base_file_path), str(base_temp_file_path))

            base_source_dir_path = Path(tempfile.mkdtemp())

            self.parse(base_temp_file_path, base_source_dir_path)

            base_temp_file_path.unlink()
        else:
            base_is_excluded = True

        # mine
        mine_is_excluded = False

        mine_file_path = Path(self.args.mine)

        if self.args.name_format == 'TortoiseGit':
            yname_file_path = Path(self.args.yname.split(':')[0])
        else:
            yname_file_path = Path(self.args.yname.split(':')[0])

        if yname_file_path.name not in exclude_file_names:
            mine_temp_file, mine_temp_file_name = tempfile.mkstemp(mine_file_path.suffix)
            os.close(mine_temp_file)

            mine_temp_file_path = Path(mine_temp_file_name)
            shutil.copyfile(str(mine_file_path), str(mine_temp_file_path))

            mine_source_dir_path = Path(tempfile.mkdtemp())

            self.parse(mine_temp_file_path, mine_source_dir_path)

            mine_temp_file_path.unlink()
        else:
            mine_is_excluded = True

        tool_args = None
        if self.args.tool == 'KDiff3':
            tool_file_path = Path(self.settings_general['KDiff3'])

            tool_args = [str(tool_file_path)]

            # base
            if base_is_excluded:
                tool_args += ['--cs', 'EncodingForA=UTF-8', str(base_file_path)]
            else:
                tool_args += ['--cs', 'EncodingForA=windows-1251', str(base_source_dir_path)]

            if self.args.bname is not None:
                tool_args += ['--L1', self.args.bname]

            # mine
            if mine_is_excluded:
                tool_args += ['--cs', 'EncodingForB=UTF-8', str(mine_file_path)]
            else:
                tool_args += ['--cs', 'EncodingForB=windows-1251', str(mine_source_dir_path)]

            if self.args.yname is not None:
                tool_args += ['--L2', self.args.yname]
        elif self.args.tool == 'AraxisMerge':
            tool_file_path = Path(self.settings_general['AraxisMerge'])

            tool_args = [str(tool_file_path), '/max', '/wait']

            # base
            if base_is_excluded:
                tool_args += [str(base_file_path)]
            else:
                tool_args += [str(base_source_dir_path)]

            if self.args.bname is not None:
                tool_args += ['/title1:{}'.format(self.args.bname)]

            # mine
            if mine_is_excluded:
                tool_args += [str(mine_file_path)]
            else:
                tool_args += [str(mine_source_dir_path)]

            if self.args.yname is not None:
                tool_args += ['/title2:{}'.format(self.args.yname)]
        elif self.args.tool == 'WinMerge':
            tool_file_path = Path(self.settings_general['WinMerge'])

            tool_args = [str(tool_file_path), '-e', '-ub']

            # base
            if base_is_excluded:
                tool_args += [str(base_file_path)]
            else:
                tool_args += [str(base_source_dir_path)]

            if self.args.bname is not None:
                tool_args += ['-dl', self.args.bname]

            # mine
            if mine_is_excluded:
                tool_args += [str(mine_file_path)]
            else:
                tool_args += [str(mine_source_dir_path)]

            if self.args.yname is not None:
                tool_args += ['-dr', self.args.yname]
        elif self.args.tool == 'ExamDiff':
            tool_file_path = Path(self.settings_general['ExamDiff'])

            tool_args = [str(tool_file_path)]

            # base
            if base_is_excluded:
                tool_args += [str(base_file_path)]
            else:
                tool_args += [str(base_source_dir_path)]

            if self.args.bname is not None:
                tool_args += ['--left_display_name:{}'.format(self.args.bname)]

            # mine
            if mine_is_excluded:
                tool_args += [str(mine_file_path)]
            else:
                tool_args += [str(mine_source_dir_path)]

            if self.args.yname is not None:
                tool_args += ['--right_display_name:{}'.format(self.args.yname)]

        if tool_args is None:
            raise Exception('Не удалось сравнить файлы {} и {}'.format(str(base_file_path), str(mine_file_path)))

        exit_code = subprocess.check_call(tool_args)
        if not exit_code == 0:
            raise Exception('Не удалось сравнить файлы {} и {}'.format(str(base_file_path), str(mine_file_path)))


def run(args: Any) -> None:
    settings = get_settings(APP_NAME, APP_AUTHOR)
    processor = Parser(args, settings)
    processor.run()
