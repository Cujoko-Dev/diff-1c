# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import shutil
import subprocess
import tempfile

from commons.compat import s, u
from commons.settings import SettingsError, get_settings
from diff_1c.__about__ import APP_AUTHOR, APP_NAME
from parse_1c_build import Parser


class Processor(object):
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

    def run(self, base_file_fullname, mine_file_fullname, bname='', yname='', name_format='tortoisegit', tool='kdiff3'):
        # base
        base_is_excluded = False
        if bname:
            if name_format.lower() == 'tortoisegit':
                bname_file_fullname = bname.split(':')[0]
            else:
                bname_file_fullname = bname.split(':')[0]
        else:
            bname_file_fullname = os.getcwd()
        base_source_dir_fullname = None
        if os.path.basename(bname_file_fullname) not in self.exclude_file_names:
            base_file_fullname_suffix = os.path.splitext(base_file_fullname)[1]
            base_temp_file, base_temp_file_fullname = tempfile.mkstemp(base_file_fullname_suffix)
            base_temp_file_fullname = u(base_temp_file_fullname, 'cp1251')
            os.close(base_temp_file)
            shutil.copyfile(base_file_fullname, base_temp_file_fullname)
            base_source_dir_fullname = u(tempfile.mkdtemp(), 'cp1251')
            Parser().run(base_temp_file_fullname, base_source_dir_fullname)
            os.remove(base_temp_file_fullname)
        else:
            base_is_excluded = True
        # mine
        mine_is_excluded = False
        if yname:
            if name_format.lower() == 'tortoisegit':
                yname_file_fullname = yname.split(':')[0]
            else:
                yname_file_fullname = yname.split(':')[0]
        else:
            yname_file_fullname = os.getcwd()
        mine_source_dir_fullname = None
        if os.path.basename(yname_file_fullname) not in self.exclude_file_names:
            mine_file_fullname_suffix = os.path.splitext(mine_file_fullname)[1]
            mine_temp_file, mine_temp_file_fullname = tempfile.mkstemp(mine_file_fullname_suffix)
            mine_temp_file_fullname = u(mine_temp_file_fullname, 'cp1251')
            os.close(mine_temp_file)
            shutil.copyfile(mine_file_fullname, mine_temp_file_fullname)
            mine_source_dir_fullname = u(tempfile.mkdtemp(), 'cp1251')
            Parser().run(mine_temp_file_fullname, mine_source_dir_fullname)
            os.remove(mine_temp_file_fullname)
        else:
            mine_is_excluded = True
        tool_args = None
        if tool.lower() == 'kdiff3':
            tool_file_fullname = self.settings['kdiff3_file']
            tool_args = [tool_file_fullname]
            # base
            if base_is_excluded:
                tool_args += ['--cs', 'EncodingForA=UTF-8', base_file_fullname]
            else:
                tool_args += ['--cs', 'EncodingForA=windows-1251', base_source_dir_fullname]
            if bname is not None:
                tool_args += ['--L1', bname]
            # mine
            if mine_is_excluded:
                tool_args += ['--cs', 'EncodingForB=UTF-8', mine_file_fullname]
            else:
                tool_args += ['--cs', 'EncodingForB=windows-1251', mine_source_dir_fullname]
            if yname is not None:
                tool_args += ['--L2', yname]
        elif tool.lower() == 'araxismerge':
            tool_file_fullname = self.settings['araxismerge_file']
            tool_args = [tool_file_fullname, '/max', '/wait']
            # base
            if base_is_excluded:
                tool_args += [base_file_fullname]
            else:
                tool_args += [base_source_dir_fullname]
            if bname is not None:
                tool_args += ['/title1:{}'.format(bname)]
            # mine
            if mine_is_excluded:
                tool_args += [mine_file_fullname]
            else:
                tool_args += [mine_source_dir_fullname]
            if yname is not None:
                tool_args += ['/title2:{}'.format(yname)]
        elif tool.lower() == 'winmerge':
            tool_file_fullname = self.settings['winmerge_file']
            tool_args = [tool_file_fullname, '-e', '-ub']
            # base
            if base_is_excluded:
                tool_args += [base_file_fullname]
            else:
                tool_args += [base_source_dir_fullname]
            if bname is not None:
                tool_args += ['-dl', bname]
            # mine
            if mine_is_excluded:
                tool_args += [mine_file_fullname]
            else:
                tool_args += [mine_source_dir_fullname]
            if yname is not None:
                tool_args += ['-dr', yname]
        elif tool.lower() == 'examdiff':
            tool_file_fullname = self.settings['examdiff_file']
            tool_args = [tool_file_fullname]
            # base
            if base_is_excluded:
                tool_args += [base_file_fullname]
            else:
                tool_args += [base_source_dir_fullname]
            if bname is not None:
                tool_args += ['--left_display_name:{}'.format(bname)]
            # mine
            if mine_is_excluded:
                tool_args += [mine_file_fullname]
            else:
                tool_args += [mine_source_dir_fullname]
            if yname is not None:
                tool_args += ['--right_display_name:{}'.format(yname)]
        if tool_args is None:
            raise Exception('Diff files \'{0}\' and \'{1}\' failed'.format(base_file_fullname, mine_file_fullname))
        exit_code = subprocess.check_call(s(tool_args, 'cp1251'))
        if not exit_code == 0:
            raise Exception('Diff files \'{0}\' and \'{1}\' failed'.format(base_file_fullname, mine_file_fullname))


def run(args):
    processor = Processor()

    # Args
    base_file_fullname = args.base
    mine_file_fullname = args.mine
    bname = args.bname
    yname = args.yname
    name_format = args.name_format
    tool = args.tool

    processor.run(base_file_fullname, mine_file_fullname, bname, yname, name_format, tool)
