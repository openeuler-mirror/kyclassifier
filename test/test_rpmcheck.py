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

from src.rpmquery.rpmcheck import RpmCheck

class TestRpmCheck(unittest.TestCase):
    '''
        RpmCheck模块单元测试
    '''

    def setUp(self):
        self.rpm_path = '/opt/kyclassifier/test.rpm'
        self.rpm_check = RpmCheck(self.rpm_path)



    def test_check_exist(self):
        """
            Test class method check_exist()
        Returns:
            bool
        """
        result = self.rpm_check.check_exist()
        self.assertIn(result, [True, False], "check_exist test failed!")


if __name__ == "__main__":
    unittest.main(verbosity=2)