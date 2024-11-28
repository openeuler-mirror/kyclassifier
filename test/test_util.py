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
import os
import time

from src.utils.util import get_formatted_time, trans_set2list, get_localos_data, ISOUtils


class TestUtil(unittest.TestCase):

    def setUp(self):
        self.iso_utils = ISOUtils()
        self.iso_path = "/tmp/test.iso"

    def tearDown(self):
        pass

    def test_get_formatted_time(self):
        """Test method get_formatted_time()
        """
        result = get_formatted_time()
        standard_time = time.strftime("%Y-%m-%d-%H-%M")
        self.assertIn(standard_time, result, "get_formatted_time test failed!")

    def test_trans_set2list(self):
        """Test method trans_set2list(key2set_dict)
        """
        key2set_dict = {
            "key1": set(["value1","value2","value3"]),
            "key2": set([1,2,3]),

        }
        result_dict = trans_set2list(key2set_dict)
        result = []
        for _,value in result_dict.items():
            if isinstance(value, list):
                result.append(True)
        self.assertTrue(all(result),"trans_set2list test falied!")


    def test_parse_iso_repodata(self):
        """Test static method parse_iso_repodata(iso_path,repodata_dir='/opt/kyclassifier/iso_parse/repodata')
        """
        repodata_dir='/opt/kyclassifier/iso_parse/repodata'
        if os.path.exists(self.iso_path):
            self.iso_utils.parse_iso_repodata(self.iso_path)
            self.assertTrue(os.path.exists(repodata_dir), "parse_iso_repodata test failed!")
        else:
            self.skipTest("trans_set2list test skiped!")

    def test_get_repo_from_dir(self):
        """Test static method get_repo_from_dir(repodata_dir='/opt/kyclassifier/iso_parse/repodata')
        """
        repodata_dir='/opt/kyclassifier/iso_parse/repodata'
        if os.path.exists(repodata_dir):
            repomd_fn, primary_fn, filelists_fn = self.iso_utils.get_repo_from_dir(repodata_dir)
            result = all(['repomd.xml' in repomd_fn, 'primary.xml' in primary_fn, 'filelists.xml' in filelists_fn])
            self.assertTrue(result, "get_repo_from_dir test failed!")
        else:
            self.skipTest("get_repo_from_dir test skiped!")

    def test_parase_iso_repofile(self):
        """Test class method parase_iso_repofile(iso_path,target_dir='/opt/kyclassifier/iso_parse/repodata')
        """
        target_dir='/opt/kyclassifier/iso_parse/repodata'
        if os.path.exists(target_dir) and os.path.exists(self.iso_path):
            repomd_fn, primary_fn, filelists_fn = self.iso_utils.parase_iso_repofile(self.iso_path)
            result = all(['repomd.xml' in repomd_fn, 'primary.xml' in primary_fn, 'filelists.xml' in filelists_fn])
            self.assertTrue(result, "parase_iso_repofile test failed!")
        else:
            self.skipTest("parase_iso_repofile test skiped!")
