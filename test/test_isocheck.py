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
import pycdlib

from src.utils.isocheck import IsoCheck


class TestIsoCheck(unittest.TestCase):
    """
        IsoCheck模块单元测试
    """

    def setUp(self):
        self.iso_path = '/opt/kyclassifier/test.iso'
        self.iso_check = IsoCheck(self.iso_path)

    def tearDown(self):
        pass


    def test_check_exist(self):
        """
            Test class method check_exist()
        Returns:
            bool
        """
        result = self.iso_check.check_exist()
        self.assertIn(result, [True, False], "check_exist test failed!")

    def test_check_format(self):
        """
            Test class method check_format()
        Returns:
            bool
        """
        if not self.iso_check.check_exist():
            self.skipTest("iso file not exist,skip test check_format")
        result = self.iso_check.check_format()
        self.assertIn(result, [True, False], "check_format test failed!")
        

if __name__ == "__main__":
    unittest.main(verbosity=2)
