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

from src.utils.dataparse import ISODataParse, RepoDataParse, LocalInstalledDataParse
from src.utils.repocheck import RepoCheck


class TestDataParse(unittest.TestCase):
    """
        DataParse模块单元测试
    """

    def setUp(self):
        self.files_path = ['/opt/kyclassifier/iso_parse/repodata/repomd.xml',
                           '/opt/kyclassifier/iso_parse/repodata/test_primary.xml.gz',
                           '/opt/kyclassifier/iso_parse/repodata/test_filelists.xml.gz',
                           ]
        
    def tearDown(self):
        pass

    def _init_iso_dataparse(self):
        """
            Try to init iso_depparse object
        Returns:
            bool
        """
        try:
            self.iso_dataparse = ISODataParse(self.files_path)
            return True
        except:
            return False

    def test_iso_get_pkgname_set(self):
        """
            Test class ISODataParse method get_pkgname_set()
        Returns:
            set()
        """
        if not self._init_iso_dataparse():
            self.skipTest("Init iso_dataparse failed, test skiped!")
        else:
            result = self.iso_dataparse.get_pkgname_set(self.files_path)
            self.assertIsInstance(result, set, "get_pkgname_set test failed!")

    def test_iso_get_pkgsinfo_list(self):
        """
            Test class ISODataParse method get_pkgname_set()
        Returns:
            list
        """
        if not self._init_iso_dataparse():
            self.skipTest("Init iso_dataparse failed, test skiped!")
        else:
            result = self.iso_dataparse.get_pkgsinfo_list(self.files_path)
            self.assertIsInstance(result, list, "get_pkgsinfo_list test failed!")

    def test_iso_get_pkginfo_byname(self):
        """
            Test class ISODataParse method get_pkginfo_byname()
        Args:
            pkgname (str)
        Returns:
            result (list) [info1,info2]
        """
        if not self._init_iso_dataparse():
            self.skipTest("Init iso_dataparse failed, test skiped!")
        else:
            pkgname = 'kernel'
            result = self.iso_dataparse.get_pkginfo_byname(pkgname)
            self.assertIsInstance(result, list, "get_pkginfo_byname test failed!")
    
    def test__list2dict(self):
        """
            Test class ISODataParse method _list2dict()
        Args:
            dict_list (list): [d1,d2,...]
            key (str)
        Returns:
            res (dict): {d[key]:[d1,d2,...], ...}
        """
        dict_list = [{'pkgname':'aaa'},
                     {'pkgname':'bbb'}]
        key = 'pkgname'
        result = ISODataParse._list2dict(dict_list,key)
        self.assertIsInstance(result,dict,"_list2dict test failed!")
    
    def test_repo__load_data(self):
        """
            Test class RepoDataParse method _load_data()
        Returns:
            list
        """
        if not RepoCheck.check():
            self.skipTest("Repo check failed, test skiped!")
        else:
            result = RepoDataParse._load_data()
            self.assertIsInstance(result,list,"_load_data test failed!")
            
    def test_repo_get_pkgname_set(self):
        """
            Test class RepoDataParse method get_pkgname_set()
        Returns:
            set
        """
        if not RepoCheck.check():
            self.skipTest("Repo check failed, test skiped!")
        else:
            result = RepoDataParse.get_pkgname_set()
            self.assertIsInstance(result,set,"get_pkgname_set test failed!")

    def test_repo_get_pkgsinfo_list(self):
        """
            Test class RepoDataParse method get_pkgsinfo_list()
        Returns:
            list
        """
        if not RepoCheck.check():
            self.skipTest("Repo check failed, test skiped!")
        else:
            result = RepoDataParse.get_pkgsinfo_list()
            self.assertIsInstance(result,list,"get_pkgsinfo_list test failed!")

    def test_repo_list2dict(self):
        """
            Test class RepoDataParse method _list2dict()
        Returns:
            list
        """
        if not RepoCheck.check():
            self.skipTest("Repo check failed, test skiped!")
        else:
            dict_list = [{'pkgname':'aaa'},
                         {'pkgname':'bbb'}]
            key = 'pkgname'
            result = RepoDataParse._list2dict(dict_list,key)
            self.assertIsInstance(result,dict,"_list2dict test failed!")

    def test_local_get_pkgname_set(self):
        """
            Test class LocalInstalledDataParse method get_pkgname_set()
        Returns:
            set
        """
        result = LocalInstalledDataParse.get_pkgname_set()
        self.assertIsInstance(result,set,"get_pkgname_set test failed!")


if __name__ == "__main__":
    unittest.main(verbosity=2)