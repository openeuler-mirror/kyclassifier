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

from src.rpmquery.querylayeriniso import QueryLayerInIso

class TestQueryLayerInIso(unittest.TestCase):

    def setUp(self):
        self._rpm = '/opt/kyclassifier/test.rpm'
        self._iso = '/opt/kyclassifier/test.iso'
        self.isinit = True if self._init_querylayeriniso() else False
        
    def _init_querylayeriniso(self):
        """
            Try to init querylayeriniso object
        Returns:
            bool
        """
        try:
            self.obj = QueryLayerInIso(self._rpm,self._iso)
            return True
        except:
            return False

    def test_get_rpm_layer(self):
        pass

    def test_get_rpmdeps(self):
        pass

    def test_get_isopkgs_layer(self):
        """
            Test class QueryLayerInIso method _get_isopkgs_layer()
        Returns:
            dict
        """
        if not self.isinit:
            self.skipTest("QueryLayerInIso obj init failed,get_isopkgs_layer test skiped!")
        result = self.obj._get_isopkgs_layer()
        self.assertIsInstance(result,dict,"_get_isopkgs_layer test failed!")
    
    def test_get_isofiles(self):
        pass

    def test_check(self):
        pass

    def test_rpm(self):
        pass

    def test_iso(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)