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

import unittest

from src.utils.repocheck import RepoCheck


class TestRepoCheck(unittest.TestCase):

    def setUp(self):
        self.repo_check = RepoCheck()

    def tearDown(self):
        pass


    def test_check_exist(self):
        """Test class method check_exist()
        """
        result = self.repo_check.check_exist()
        self.assertIn(result, [True, False], "check_exist test failed!")

    def test__load_data(self):
        """Test class method _load_data()
        """
        result = self.repo_check._load_data()
        self.assertIsInstance(result, list, "_load_data test failed!")


if __name__ == "__main__":
    unittest.main(verbosity=2)
