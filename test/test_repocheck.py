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

from src.utils.repocheck import RepoCheck


class TestRepoCheck(unittest.TestCase):

    def setUp(self):
        self.repo_check = RepoCheck()
        self.repo_path = "/etc/yum.repos.d"
        self.repofile = os.path.join(self.repo_path, "check_tmp.repo")
        self.tmp_path = "/tmp"
        self.dst_repofile = os.path.join(self.repo_path, "check_tmp.repo")

    def tearDown(self):
        """Clear test data
        """
        if os.path.exists(self.repofile):
            os.remove(self.repofile)

        if os.path.exists(self.dst_repofile):
            os.remove(self.dst_repofile)

    def test_check_exist(self):
        """Test class method check_exist()

        Returns:
            bool
        """
        result = self.repo_check.check_exist()
        self.assertIn(result, [True, False], "check_exist test failed!")

    def test__load_data(self):
        """Test class method _load_data()

        Returns:
            datatype
        """
        result = self.repo_check._load_data()
        self.assertIsInstance(result, list, "_load_data test failed!")

    def test__create_repofile(self):
        """Test static method _create_repofile(arepos_l)

        Args:
            repos_l (list): repodata list
        Returns:
            bool
        """
        repos_l = [{
            "repo_id": "test_base_repo",
            "baseurl": "http://url/path/base/arch"
            }, {
            "repo_id": "test_updates_repo",
            "baseurl": "http://url/path/updates/arch"
            }
        ]
        if os.path.exists(self.repo_path):
            result = self.repo_check._create_repofile(repos_l)
            self.assertIn(result, [True, False], "_create_repofile test failed!")
        else:
            self.skipTest("_create_repofile test skiped!")


    def test_move_repofiles(self):
        """Test static method move_repofiles(src,dst)

        Args:
            src (str)
            dst (str)
        Returns:
            None
        """
        try:
            if os.path.exists(self.repo_path) and os.path.exists(self.tmp_path):
                self.repo_check.move_repofiles(self.repofile, self.dst_repofile)
            else:
                raise IOError("move file dose not exists")
        except IOError:
            self.skipTest("move_repofiles test skiped!")

    def test_check_repo_useful(self):
        """Test class method check_repo_useful()

        Returns:
            None
        """
        try:
            result = self.repo_check.check_repo_useful()
            self.assertIn(result, [True, False], "check_repo_useful test failed!")
        except IOError:
            self.skipTest("check_repo_useful test skiped!")

    def test_check(self):
        """Test class method check()

        Returns:
            bool
        """
        result = self.repo_check.check()
        self.assertIn(result, [True, False], "check test failed!")


if __name__ == "__main__":
    unittest.main(verbosity=2)
