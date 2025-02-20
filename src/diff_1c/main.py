# -*- coding: utf-8 -*-

"""Главная"""


import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from cjk_commons.settings import (
    SettingsError,
    get_attribute,
    get_path_attribute,
    get_settings,
)
from loguru import logger
from parse_1c_build import Parser

from diff_1c.__about__ import APP_AUTHOR, APP_NAME

logger.disable(__name__)


class Processor:
    """Процессор"""

    def __init__(self, **kwargs):
        settings_file_path = get_path_attribute(
            kwargs,
            "settings_file_path",
            default_path=Path("settings.yaml"),
            is_dir=False,
            check_if_exists=False,
        )
        self.settings = get_settings(
            settings_file_path, app_name=APP_NAME, app_author=APP_AUTHOR
        )

        self.tool = get_attribute(
            kwargs, "tool", self.settings, "default_tool", "kdiff3"
        ).lower()
        if self.tool not in self.settings["tools"]:
            raise SettingsError("Tool Incorrect")

        self.tool_path = Path(self.settings["tools"][self.tool])
        if not self.tool_path.is_file():
            raise SettingsError("Tool Not Exists")

        self.exclude_file_names = get_attribute(
            kwargs, "exclude_file_names", self.settings, "exclude_file_names", []
        )
        self.name_format = get_attribute(
            kwargs, "name_format", self.settings, "name_format", "tortoisegit"
        ).lower()

    def run(
        self,
        base_file_path: Path,
        mine_file_path: Path,
        bname: str = "",
        yname: str = "",
    ) -> None:
        """Запустить"""

        # base
        base_is_excluded = False
        if bname:
            if self.name_format == "tortoisegit":
                bname_file_path = Path(bname.split(":")[0])
            else:
                bname_file_path = Path(bname.split(":")[0])
        else:
            bname_file_path = Path.cwd()
        base_source_dir_path = None
        if bname_file_path.name not in self.exclude_file_names:
            base_file_path_suffix = base_file_path.suffix
            base_temp_file, base_temp_file_name = tempfile.mkstemp(
                base_file_path_suffix
            )
            os.close(base_temp_file)
            shutil.copyfile(str(base_file_path), base_temp_file_name)
            base_source_dir_path = Path(tempfile.mkdtemp())
            Parser().run(Path(base_temp_file_name), base_source_dir_path)
            Path(base_temp_file_name).unlink()
        else:
            base_is_excluded = True

        # mine
        mine_is_excluded = False
        if yname:
            if self.name_format == "tortoisegit":
                yname_file_path = Path(yname.split(":")[0])
            else:
                yname_file_path = Path(yname.split(":")[0])
        else:
            yname_file_path = Path.cwd()
        mine_source_dir_path = None
        if yname_file_path.name not in self.exclude_file_names:
            mine_file_path_suffix = mine_file_path.suffix
            mine_temp_file, mine_temp_file_name = tempfile.mkstemp(
                mine_file_path_suffix
            )
            os.close(mine_temp_file)
            shutil.copyfile(str(mine_file_path), mine_temp_file_name)
            mine_source_dir_path = Path(tempfile.mkdtemp())
            Parser().run(Path(mine_temp_file_name), mine_source_dir_path)
            Path(mine_temp_file_name).unlink()
        else:
            mine_is_excluded = True

        tool_args = [str(self.tool_path)]
        if self.tool == "kdiff3":
            # base
            if base_is_excluded:
                tool_args += ["--cs", "EncodingForA=UTF-8", str(base_file_path)]
            else:
                tool_args += [
                    "--cs",
                    "EncodingForA=windows-1251",
                    str(base_source_dir_path),
                ]
            if bname is not None:
                tool_args += ["--L1", bname]

            # mine
            if mine_is_excluded:
                tool_args += ["--cs", "EncodingForB=UTF-8", str(mine_file_path)]
            else:
                tool_args += [
                    "--cs",
                    "EncodingForB=windows-1251",
                    str(mine_source_dir_path),
                ]
            if yname is not None:
                tool_args += ["--L2", yname]
        exit_code = subprocess.check_call(tool_args)
        if not exit_code == 0:
            raise Exception(
                f"Diff files '{base_file_path}' and '{mine_file_path}' failed"
            )


def run(args) -> None:
    """Запустить"""

    logger.enable("cjk_commons")
    logger.enable("parse_1c_build")
    logger.enable(__name__)

    try:
        processor = Processor(name_format=args.name_format, tool=args.tool)

        base_file_path = Path(args.base)
        mine_file_path = Path(args.mine)
        bname = args.bname
        yname = args.yname

        processor.run(base_file_path, mine_file_path, bname, yname)
    except Exception as exc:
        logger.exception(exc)
        sys.exit(1)
