# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

# noinspection PyUnresolvedReferences
from diff_1c.__about__ import __version__
# noinspection PyUnresolvedReferences
from diff_1c.main import Processor

# noinspection PyUnresolvedReferences
logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
