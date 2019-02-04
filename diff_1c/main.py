# -*- coding: utf-8 -*-
import logging
import os
from pathlib import Path
import subprocess
import tempfile

import shutil

from commons.settings import SettingsError, get_settings
from diff_1c.__about__ import APP_AUTHOR, APP_NAME
from parse_1c_build import Parser

logger: logging.Logger = logging.getLogger(__name__)


class Processor(object):
    def __init__(self, **kwargs):
        settings_file_path = Path('settings.yaml')
        if 'settings_file_path' in kwargs:
            settings_file_path = Path(kwargs['settings_file_path'])
        self.settings = get_settings(settings_file_path, app_name=APP_NAME, app_author=APP_AUTHOR)
        if 'exclude_names' in kwargs:
            self.exclude_file_names = []
        else:
            if 'exclude_names' not in self.settings:
                raise SettingsError('There is no exclude_files in settings!')
            self.exclude_file_names = self.settings['exclude_files']

    def run(
            self, base_file_fullpath: Path, mine_file_fullpath: Path, bname: str = '', yname: str = '',
            name_format: str = 'tortoisegit', tool: str = 'kdiff3') -> None:
        # base
        base_is_excluded = False
        if bname:
            if name_format.lower() == 'tortoisegit':
                bname_file_fullpath = Path(bname.split(':')[0])
            else:
                bname_file_fullpath = Path(bname.split(':')[0])
        else:
            bname_file_fullpath = Path.cwd()
        base_source_dir_fullpath = None
        if bname_file_fullpath.name not in self.exclude_file_names:
            base_file_fullpath_suffix = base_file_fullpath.suffix
            base_temp_file, base_temp_file_fullname = tempfile.mkstemp(base_file_fullpath_suffix)
            os.close(base_temp_file)
            shutil.copyfile(str(base_file_fullpath), base_temp_file_fullname)
            base_source_dir_fullpath = Path(tempfile.mkdtemp())
            Parser().run(Path(base_temp_file_fullname), base_source_dir_fullpath)
            Path(base_temp_file_fullname).unlink()
        else:
            base_is_excluded = True
        # mine
        mine_is_excluded = False
        if yname:
            if name_format.lower() == 'tortoisegit':
                yname_file_fullpath = Path(yname.split(':')[0])
            else:
                yname_file_fullpath = Path(yname.split(':')[0])
        else:
            yname_file_fullpath = Path.cwd()
        mine_source_dir_fullpath = None
        if yname_file_fullpath.name not in self.exclude_file_names:
            mine_file_fullpath_suffix = mine_file_fullpath.suffix
            mine_temp_file, mine_temp_file_fullname = tempfile.mkstemp(mine_file_fullpath_suffix)
            os.close(mine_temp_file)
            shutil.copyfile(str(mine_file_fullpath), mine_temp_file_fullname)
            mine_source_dir_fullpath = Path(tempfile.mkdtemp())
            Parser().run(Path(mine_temp_file_fullname), mine_source_dir_fullpath)
            Path(mine_temp_file_fullname).unlink()
        else:
            mine_is_excluded = True
        tool_args = None
        if tool.lower() == 'kdiff3':
            tool_file_fullpath = Path(self.settings['kdiff3_file_path'])
            tool_args = [tool_file_fullpath]
            # base
            if base_is_excluded:
                tool_args += ['--cs', 'EncodingForA=UTF-8', base_file_fullpath]
            else:
                tool_args += ['--cs', 'EncodingForA=windows-1251', base_source_dir_fullpath]
            if bname is not None:
                tool_args += ['--L1', bname]
            # mine
            if mine_is_excluded:
                tool_args += ['--cs', 'EncodingForB=UTF-8', mine_file_fullpath]
            else:
                tool_args += ['--cs', 'EncodingForB=windows-1251', mine_source_dir_fullpath]
            if yname is not None:
                tool_args += ['--L2', yname]
        elif tool.lower() == 'araxismerge':
            tool_file_fullpath = Path(self.settings['araxismerge_file_path'])
            tool_args = [tool_file_fullpath, '/max', '/wait']
            # base
            if base_is_excluded:
                tool_args += [base_file_fullpath]
            else:
                tool_args += [base_source_dir_fullpath]
            if bname is not None:
                tool_args += ['/title1:{}'.format(bname)]
            # mine
            if mine_is_excluded:
                tool_args += [mine_file_fullpath]
            else:
                tool_args += [mine_source_dir_fullpath]
            if yname is not None:
                tool_args += ['/title2:{}'.format(yname)]
        elif tool.lower() == 'winmerge':
            tool_file_fullpath = Path(self.settings['winmerge_file_path'])
            tool_args = [tool_file_fullpath, '-e', '-ub']
            # base
            if base_is_excluded:
                tool_args += [base_file_fullpath]
            else:
                tool_args += [base_source_dir_fullpath]
            if bname is not None:
                tool_args += ['-dl', bname]
            # mine
            if mine_is_excluded:
                tool_args += [mine_file_fullpath]
            else:
                tool_args += [mine_source_dir_fullpath]
            if yname is not None:
                tool_args += ['-dr', yname]
        elif tool.lower() == 'examdiff':
            tool_file_fullpath = Path(self.settings['examdiff_file_path'])
            tool_args = [tool_file_fullpath]
            # base
            if base_is_excluded:
                tool_args += [base_file_fullpath]
            else:
                tool_args += [base_source_dir_fullpath]
            if bname is not None:
                tool_args += ['--left_display_name:{}'.format(bname)]
            # mine
            if mine_is_excluded:
                tool_args += [mine_file_fullpath]
            else:
                tool_args += [mine_source_dir_fullpath]
            if yname is not None:
                tool_args += ['--right_display_name:{}'.format(yname)]
        if tool_args is None:
            raise Exception('Diff files \'{0}\' and \'{1}\' failed'.format(base_file_fullpath, mine_file_fullpath))
        exit_code = subprocess.check_call(tool_args)
        if not exit_code == 0:
            raise Exception('Diff files \'{0}\' and \'{1}\' failed'.format(base_file_fullpath, mine_file_fullpath))


def run(args) -> None:
    try:
        processor = Processor()

        # Args
        base_file_fullpath = Path(args.base)
        mine_file_fullpath = Path(args.mine)
        bname = args.bname
        yname = args.yname
        name_format = args.name_format
        tool = args.tool

        processor.run(base_file_fullpath, mine_file_fullpath, bname, yname, name_format, tool)
    except Exception as e:
        logger.exception(e)
