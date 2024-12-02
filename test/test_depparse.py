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

from src.utils.depparse import ISODepParse,RepoDepParse
from src.utils.repocheck import RepoCheck


class TestDepParse(unittest.TestCase):
    """
        DepParse模块单元测试
    """

    def setUp(self):
        self.files_path = ['/opt/kyclassifier/iso_parse/repodata/test_primary.xml',
                           '/opt/kyclassifier/iso_parse/repodata/test_filelists.xml',
                           '/opt/kyclassifier/iso_parse/repodata/repomd.xml']

    def tearDown(self):
        pass

    def _init_iso_depparse(self):
        """
            Try to init iso_depparse object
        Returns:
            bool
        """
        try:
            self.iso_depparse = ISODepParse(self.files_path)
            return True
        except:
            return False

    def test_iso_get_repo_pkg_deps(self):
        """
            Test class ISODepParse method _get_repo_pkg_deps()
        Returns:
            dict
        """
        if not self._init_iso_depparse():
            self.skipTest("Init iso_depparse failed, test skiped!")
        else:
            result = self.iso_depparse._get_repo_pkg_deps()
            self.assertIsInstance(result,dict,"iso_depparse._get_repo_pkg_deps test failed!")
    
    def test_iso_get_repo_pkg_deps_by(self):
        """
            Test class ISODepParse method _get_repo_pkg_deps_by()
        Returns:
            dict
        """
        if not self._init_iso_depparse():
            self.skipTest("Init iso_depparse failed, test skiped!")
        else:
            result = self.iso_depparse._get_repo_pkg_deps_by()
            self.assertIsInstance(result,dict,"iso_depparse._get_repo_pkg_deps_by test failed!")
    
    def test_iso_get_all_pkgs(self):
        """
            Test class ISODepParse method _get_all_pkgs()
        Returns:
            set
        """
        if not self._init_iso_depparse():
            self.skipTest("Init iso_depparse failed, test skiped!")
        else:
            result = self.iso_depparse._get_all_pkgs()
            self.assertIsInstance(result,set,"iso_depparse._get_all_pkgs test failed!")
    
    def _init_repo_depparse(self):
        """
            Try to init RepoDepParse object
        Returns:
            bool
        """
        try:
            self.repo_depparse = RepoDepParse()
            return True
        except:
            return False
    
    def test_repo_load_data(self):
        """
            Test class RepoDepParse method _load_data()
        Returns:
            list
        """
        if not RepoCheck:
            self.skipTest("Repo check failed, test skiped!")
        if not self._init_repo_depparse():
            self.skipTest("RepoDepParse obj init failed, test skiped!")
        result = self.repo_depparse._load_data()
        self.assertIsInstance(result,list,"repo_depparse._load_data test failed!")

    def test_repo_get_all_pkgs(self):
        """
            Test class RepoDepParse method _get_all_pkgs()
        Returns:
            set
        """
        if not RepoCheck:
            self.skipTest("Repo check failed, test skiped!")
        if not self._init_repo_depparse():
            self.skipTest("RepoDepParse obj init failed, test skiped!")
        result = self.repo_depparse._get_all_pkgs()
        self.assertIsInstance(result,set,"repo_depparse._get_all_pkgs test failed!")

    def test_repo_get_repo_pkg_deps(self):
        """
            Test class RepoDepParse method _get_repo_pkg_deps()
        Returns:
            dict
        """
        if not RepoCheck:
            self.skipTest("Repo check failed, test skiped!")
        if not self._init_repo_depparse():
            self.skipTest("RepoDepParse obj init failed, test skiped!")
        result = self.repo_depparse._get_repo_pkg_deps()
        self.assertIsInstance(result,dict,"repo_depparse._get_repo_pkg_deps test failed!")


if __name__ == "__main__":
    unittest.main(verbosity=2)