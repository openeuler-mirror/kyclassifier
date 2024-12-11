# -*- coding: utf-8 -*-

"""
# **********************************************************************************
# Copyright (c) KylinSoft Co., Ltd. 2024.All rights reserved.
# [kyclassifier] licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
# PURPOSE.
# See the Mulan PSL v2 for more details.
# **********************************************************************************
"""
import os
import sys
current_path = os.path.dirname(__file__)
parent_path = os.path.dirname(current_path)
sys.path.append(parent_path)

import unittest

from test_algclassify import TestAlgClassify
from test_alglayer import TestAlglayer
from test_dataparse import TestDataParse
from test_depparse import TestDepParse
from test_isocheck import TestIsoCheck
from test_localcheck import TestLocalCheck
from test_repocheck import TestRepoCheck
from test_util import TestUtil
from test_querylayerinlocal import TestQueryLayerInLocal


if __name__ == "__main__":
    unittest.main(verbosity=2)
