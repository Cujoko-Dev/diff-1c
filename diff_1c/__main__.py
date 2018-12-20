# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import sys

from diff_1c.core import run
import logging

logger = logging.getLogger(__name__)


sys.path.insert(0, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir)))

if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        logger.info("sldjfsdlfj")
