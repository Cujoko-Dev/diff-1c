# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import subprocess
import tempfile

import shutil

from commons.compat import Path
from commons.settings import SettingsError, get_settings
from diff_1c import APP_AUTHOR, APP_NAME
from parse_1c_build.parse import Parser


class Processor:
    def __init__(self, **kwargs):
        settings_file_path = Path('settings.yaml')
        if 'settings_file' in kwargs:
            settings_file_path = Path(kwargs['settings_file'])
        self.settings = get_settings(settings_file_path, app_name=APP_NAME, app_author=APP_AUTHOR)
        if 'exclude_files' in kwargs:
            self.exclude_file_names = []
        else:
            if 'exclude_files' not in self.settings:
                raise SettingsError('There is no exclude_files in settings!')
            self.exclude_file_names = self.settings['exclude_files']

    def run(self, args):
        # base
        base_is_excluded = False
        base_file_path = Path(args.base)
        if args.bname:
            if args.name_format.lower() == 'tortoisegit':
                bname_file_path = Path(args.bname.split(':')[0])
            else:
                bname_file_path = Path(args.bname.split(':')[0])
        else:
            bname_file_path = Path()
        base_source_dir_path = None
        if bname_file_path.name not in self.exclude_file_names:
            base_temp_file, base_temp_file_name = tempfile.mkstemp(base_file_path.suffix)
            os.close(base_temp_file)
            base_temp_file_path = Path(base_temp_file_name)
            shutil.copyfile(str(base_file_path), str(base_temp_file_path))
            base_source_dir_path = Path(tempfile.mkdtemp())
            Parser().run(base_temp_file_path, base_source_dir_path)
            base_temp_file_path.unlink()
        else:
            base_is_excluded = True
        # mine
        mine_is_excluded = False
        mine_file_path = Path(args.mine)
        if args.yname:
            if args.name_format.lower() == 'tortoisegit':
                yname_file_path = Path(args.yname.split(':')[0])
            else:
                yname_file_path = Path(args.yname.split(':')[0])
        else:
            yname_file_path = Path()
        mine_source_dir_path = None
        if yname_file_path.name not in self.exclude_file_names:
            mine_temp_file, mine_temp_file_name = tempfile.mkstemp(mine_file_path.suffix)
            os.close(mine_temp_file)
            mine_temp_file_path = Path(mine_temp_file_name)
            shutil.copyfile(str(mine_file_path), str(mine_temp_file_path))
            mine_source_dir_path = Path(tempfile.mkdtemp())
            Parser().run(mine_temp_file_path, mine_source_dir_path)
            mine_temp_file_path.unlink()
        else:
            mine_is_excluded = True
        tool_args = None
        if args.tool.lower() == 'kdiff3':
            tool_file_path = Path(self.settings['kdiff3'])
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
        elif args.tool.lower() == 'araxismerge':
            tool_file_path = Path(self.settings['araxismerge'])
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
        elif args.tool.lower() == 'winmerge':
            tool_file_path = Path(self.settings['winmerge'])
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
        elif args.tool.lower() == 'examdiff':
            tool_file_path = Path(self.settings['examdiff'])
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
            raise Exception('Diff files \'{0}\' and \'{1}\' failed'.format(str(base_file_path), str(mine_file_path)))
        exit_code = subprocess.check_call(tool_args)
        if not exit_code == 0:
            raise Exception('Diff files \'{0}\' and \'{1}\' failed'.format(str(base_file_path), str(mine_file_path)))


def run(args):
    processor = Processor()
    # Args
    processor.run(args)
