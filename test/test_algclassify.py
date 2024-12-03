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
import unittest

from src.main.algclassify import AlgClassify
from src.utils.dataparse import DataParse
from src.utils.config import BaseConfig

class TestAlgClassify(unittest.TestCase):
    """
        AlgClassify模块单元测试
    """

    def setUp(self):
        data_obj = DataParse()
        data_obj.pkgs_name = {'aaa'}
        pkgs_info = [{
            'name' : 'aaa',
            'arch' : 'x86_64',
            'version' : '1.0',
            'epoch' : '0',
            'release' : '1',
            'summary' : 'aaa.summary',
            'description' : 'aaa.description',
            'url' : 'aaa.url',
            'rpm_license': 'aaa.rpm_license',
            'rpm_vendor' : 'aaa.rpm_vendor',
            'rpm_group' : 'aaa.rpm_group',
            'rpm_sourcerpm' : 'aaa.rpm_sourcerpm'},]
        data_obj.pkgs_info = pkgs_info
        data_obj.pkgname_pkginfo_dict = {'aaa' : pkgs_info}
        self.data_obj = data_obj
        self.data_f = BaseConfig.CLASSIFYDATA
        
    def tearDown(self):
        pass

    def test_load_data(self):
        """
            Test class AlgClassify method _load_data()
        Returns:
            list
        """
        if not os.path.exists(self.data_f):
            self.skipTest("Test File not exists, test skiped!")
        else:
            result = AlgClassify._load_data(self.data_f)
            self.assertIsInstance(result,dict,"_load_data test failed!")

    def test_get_pkgs(self):
        pass

    def test_get_pkg2category_by_rpmgroup(self):
        pass

    def test_get_pkg2category_by_jsonf(self):
        pass

    def test_merge_pkg2category_dict(self):
        pass

    def test_run(self):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)