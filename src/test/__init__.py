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

import sys
import os

current_path = os.path.dirname(__file__)
parent_path = os.path.dirname(current_path)
pparent_path = os.path.dirname(parent_path)
sys.path.append(pparent_path)

import unittest

from test_repocheck import TestRepoCheck


if __name__ == "__main__":
    unittest.main(verbosity=2)
