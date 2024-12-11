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
import copy

from src.main.algclassify import AlgClassify
from src.utils.dataparse import DataParse
from src.utils.config import BaseConfig

class TestAlgClassify(unittest.TestCase):
    """
        AlgClassify模块单元测试
    """

    def setUp(self):
        data_obj = DataParse()
        data_obj.pkgs_name = {'aaa', 'aaa-devel'}
        main_rpminfo = {
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
            'rpm_sourcerpm' : 'aaa.rpm_sourcerpm',
            'rpm_files' : [
                '/usr/share/doc/aaa.txt',
                '/usr/lib/systemd/system/aaa.service',
                '/etc/aaa.conf'
            ]}
        devel_rpminfo = copy.deepcopy(main_rpminfo)
        devel_rpminfo.update({
            'name' : 'aaa-devel',
            'rpm_files' : []
        })
        pkgs_info = [main_rpminfo, devel_rpminfo]
        data_obj.pkgs_info = pkgs_info
        data_obj.pkgname_pkginfo_dict = {'aaa' : [main_rpminfo], 'aaa-devel' : [devel_rpminfo]}
        data_obj.srcrpm_pkginfo_dict = {'aaa.rpm_sourcerpm' : [main_rpminfo, devel_rpminfo]}
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
        result = AlgClassify._load_data(self.data_f)
        self.assertIsInstance(result,dict,"_load_data test failed!")

    def test_get_pkgs(self):
        """
            Test class AlgClassify method _get_pkgs()
        Returns:
            set
        """
        result = AlgClassify._get_pkgs(self.data_obj)
        self.assertIsInstance(result,set,"_get_pkgs test failed!")

    def test_get_pkg2category_by_rpmgroup(self):
        """
            Test class AlgClassify method _get_pkg2category_by_rpmgroup()
        Returns:
            dict
        """
        result = AlgClassify._get_pkg2category_by_rpmgroup(self.data_obj)
        self.assertIsInstance(result,dict,"_get_pkg2category_by_rpmgroup test failed!")

    def test_get_pkg2category_by_rpmfiles(self):
        """
            Test class AlgClassify method _get_pkg2category_by_rpmfiles()
        Returns:
            dict
        """
        result = AlgClassify._get_pkg2category_by_rpmfiles(self.data_obj)
        self.assertIsInstance(result,dict,"_get_pkg2category_by_rpmfiles test failed!")
        self.assertIn('帮助与文档',result.get('aaa', []),"The category of package aaa test failed!")
        self.assertIn('服务',result.get('aaa', []),"The category of package aaa test failed!")

    def test_get_pkg2category_by_srcrpm(self):
        """
            Test class AlgClassify method _get_pkg2category_by_srcrpm()
        Returns:
            dict
        """
        main_rpm_dict = {
            'aaa' : ['category1']
        }
        devel_rpm_dict = {
            'aaa-devel' : []
        }
        result = AlgClassify._get_pkg2category_by_srcrpm(self.data_obj,main_rpm_dict,devel_rpm_dict)
        self.assertIsInstance(result,dict,"_get_pkg2category_by_srcrpm test failed!")
        self.assertIn('category1',result.get('aaa-devel', []),"The category of package aaa-devel test failed!")

    def test_get_pkg2category_by_rpmvendor(self):
        """
            Test class AlgClassify method _get_pkg2category_by_rpmvendor()
        Returns:
            dict
        """
        result = AlgClassify._get_pkg2category_by_rpmvendor(self.data_obj)
        self.assertIsInstance(result,dict,"_get_pkg2category_by_rpmvendor test failed!")

    def test_get_pkg2category_by_jsonf(self):
        """
            Test class AlgClassify method _get_pkg2category_by_jsonf()
        Returns:
            dict
        """
        if not os.path.exists(self.data_f):
            self.skipTest("Test File not exists, test skiped!")
        result = AlgClassify._get_pkg2category_by_jsonf(self.data_f)
        self.assertIsInstance(result,dict,"_get_pkg2category_by_jsonf test failed!")

    def test_merge_pkg2category_dict(self):
        """
            Test class AlgClassify method _merge_pkg2category_dict()
        Returns:
            dict
        """
        main_rpm_dict = {
            'aaa' : ['category1']
        }
        devel_rpm_dict = {
            'aaa' : ['category2']
        }
        result = AlgClassify._merge_pkg2category_dict(self.data_obj, main_rpm_dict, devel_rpm_dict)
        self.assertIsInstance(result,dict,"_merge_pkg2category_dict test failed!")
        self.assertEqual(result['aaa'], ['category1', 'category2'], "_merge_pkg2category_dict test failed!")
        self.assertEqual(result['aaa-devel'], ['其它'], "_merge_pkg2category_dict test failed!")

    def test_run(self):
        """
            Test class AlgClassify method run()
        Returns:
            dict
        """
        if not os.path.exists(self.data_f):
            self.skipTest("Test File not exists, test skiped!")
        result = AlgClassify.run(self.data_obj,self.data_f)
        self.assertIsInstance(result,dict,"run test failed!")

if __name__ == "__main__":
    unittest.main(verbosity=2)
