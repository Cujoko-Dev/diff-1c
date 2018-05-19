# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import shutil
import subprocess
import tempfile

from commons.settings import SettingsError, get_settings
from diff_1c import APP_AUTHOR, APP_NAME
from parse_1c_build.parse import Parser


class Processor:
    def __init__(self, **kwargs):
        settings_file_name = 'settings.yaml'
        if 'settings_file' in kwargs:
            settings_file_name = kwargs['settings_file']
        self.settings = get_settings(settings_file_name, app_name=APP_NAME, app_author=APP_AUTHOR)
        if 'exclude_files' in kwargs:
            self.exclude_file_names = []
        else:
            if 'exclude_files' not in self.settings:
                raise SettingsError('There is no exclude_files in settings!')
            self.exclude_file_names = self.settings['exclude_files']

    def run(self, args):
        # base
        base_is_excluded = False
        base_file_fullname = args.base
        if args.bname:
            if args.name_format.lower() == 'tortoisegit':
                bname_file_fullname = args.bname.split(':')[0]
            else:
                bname_file_fullname = args.bname.split(':')[0]
        else:
            bname_file_fullname = os.getcwd()
        base_source_dir_fullname = None
        if os.path.basename(bname_file_fullname) not in self.exclude_file_names:
            base_file_basename = os.path.basename(base_file_fullname)
            base_file_basename_splitted = base_file_basename.split(os.extsep)
            base_file_fullname_suffix = base_file_basename_splitted[1] if len(base_file_basename_splitted) > 1 else ''
            base_temp_file, base_temp_file_fullname = tempfile.mkstemp(base_file_fullname_suffix)
            os.close(base_temp_file)
            shutil.copyfile(base_file_fullname, base_temp_file_fullname)
            base_source_dir_fullname = tempfile.mkdtemp()
            Parser().run(base_temp_file_fullname, base_source_dir_fullname)
            os.remove(base_temp_file_fullname)
        else:
            base_is_excluded = True
        # mine
        mine_is_excluded = False
        mine_file_fullname = args.mine
        if args.yname:
            if args.name_format.lower() == 'tortoisegit':
                yname_file_fullname = args.yname.split(':')[0]
            else:
                yname_file_fullname = args.yname.split(':')[0]
        else:
            yname_file_fullname = os.getcwd()
        mine_source_dir_fullname = None
        if os.path.basename(yname_file_fullname) not in self.exclude_file_names:
            mine_file_basename = os.path.basename(mine_file_fullname)
            mine_file_basename_splitted = mine_file_basename.split(os.extsep)
            mine_file_fullname_suffix = mine_file_basename_splitted[1] if len(mine_file_basename_splitted) > 1 else ''
            mine_temp_file, mine_temp_file_fullname = tempfile.mkstemp(mine_file_fullname_suffix)
            os.close(mine_temp_file)
            shutil.copyfile(mine_file_fullname, mine_temp_file_fullname)
            mine_source_dir_fullname = tempfile.mkdtemp()
            Parser().run(mine_temp_file_fullname, mine_source_dir_fullname)
            os.remove(mine_temp_file_fullname)
        else:
            mine_is_excluded = True
        tool_args = None
        if args.tool.lower() == 'kdiff3':
            tool_file_fullname = self.settings['kdiff3']
            tool_args = [tool_file_fullname]
            # base
            if base_is_excluded:
                tool_args += ['--cs', 'EncodingForA=UTF-8', base_file_fullname]
            else:
                tool_args += ['--cs', 'EncodingForA=windows-1251', base_source_dir_fullname]
            if args.bname is not None:
                tool_args += ['--L1', args.bname]
            # mine
            if mine_is_excluded:
                tool_args += ['--cs', 'EncodingForB=UTF-8', mine_file_fullname]
            else:
                tool_args += ['--cs', 'EncodingForB=windows-1251', mine_source_dir_fullname]
            if args.yname is not None:
                tool_args += ['--L2', args.yname]
        elif args.tool.lower() == 'araxismerge':
            tool_file_fullname = self.settings['araxismerge']
            tool_args = [tool_file_fullname, '/max', '/wait']
            # base
            if base_is_excluded:
                tool_args += [base_file_fullname]
            else:
                tool_args += [base_source_dir_fullname]
            if args.bname is not None:
                tool_args += ['/title1:{}'.format(args.bname)]
            # mine
            if mine_is_excluded:
                tool_args += [mine_file_fullname]
            else:
                tool_args += [mine_source_dir_fullname]
            if args.yname is not None:
                tool_args += ['/title2:{}'.format(args.yname)]
        elif args.tool.lower() == 'winmerge':
            tool_file_fullname = self.settings['winmerge']
            tool_args = [tool_file_fullname, '-e', '-ub']
            # base
            if base_is_excluded:
                tool_args += [base_file_fullname]
            else:
                tool_args += [base_source_dir_fullname]
            if args.bname is not None:
                tool_args += ['-dl', args.bname]
            # mine
            if mine_is_excluded:
                tool_args += [mine_file_fullname]
            else:
                tool_args += [mine_source_dir_fullname]
            if args.yname is not None:
                tool_args += ['-dr', args.yname]
        elif args.tool.lower() == 'examdiff':
            tool_file_fullname = self.settings['examdiff']
            tool_args = [tool_file_fullname]
            # base
            if base_is_excluded:
                tool_args += [base_file_fullname]
            else:
                tool_args += [base_source_dir_fullname]
            if args.bname is not None:
                tool_args += ['--left_display_name:{}'.format(args.bname)]
            # mine
            if mine_is_excluded:
                tool_args += [mine_file_fullname]
            else:
                tool_args += [mine_source_dir_fullname]
            if args.yname is not None:
                tool_args += ['--right_display_name:{}'.format(args.yname)]
        if tool_args is None:
            raise Exception('Diff files \'{0}\' and \'{1}\' failed'.format(base_file_fullname, mine_file_fullname))
        exit_code = subprocess.check_call(tool_args)
        if not exit_code == 0:
            raise Exception('Diff files \'{0}\' and \'{1}\' failed'.format(base_file_fullname, mine_file_fullname))


def run(args):
    processor = Processor()
    # Args
    processor.run(args)
