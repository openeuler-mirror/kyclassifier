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

from src.utils.localcheck import LocalCheck


class TestLocalCheck(unittest.TestCase):

    def setUp(self):
        self.local_check = LocalCheck()

    def tearDown(self):
        """Clear test data
        """
        pass

    def test_check_pkgsmissreq(self):
        """Test class method check_pkgsmissreq()

        Returns:
            bool
        """
        result = self.local_check.check_pkgsmissreq()
        self.assertIsInstance(result, dict, "check_pkgsmissreq test failed!")

    def test_check(self):
        """Test class method check()

        Returns:
            bool
        """
        result = self.local_check.check()
        self.assertIn(result, [True, False], "check test failed!")


if __name__ == "__main__":
    unittest.main(verbosity=2)