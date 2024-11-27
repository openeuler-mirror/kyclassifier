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

from src.utils.dataparse import ISODataParse


class TestDataParse(unittest.TestCase):
    """
        DataParse模块单元测试
    """

    def setUp(self):
        self.files_path = ['/opt/kyclassifier/iso_parse/repodata/test_primary.xml',
                           '/opt/kyclassifier/iso_parse/repodata/test_filelists.xml',
                           '/opt/kyclassifier/iso_parse/repodata/repomd.xml']
        self.iso_dataparse = ISODataParse(self.files_path)
        
    def tearDown(self):
        pass

    def test_get_pkgname_set(self):
        """
            Test class method get_pkgname_set()
        Returns:
            set()
        """
        result = self.iso_dataparse.get_pkgname_set(self.files_path)
        self.assertIsInstance(result, set, "get_pkgname_set test failed!")


if __name__ == "__main__":
    unittest.main(verbosity=2)