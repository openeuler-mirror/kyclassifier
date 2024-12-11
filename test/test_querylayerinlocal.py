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

from src.rpmquery.querylayerinlocal import QueryLayerInLocal

class TestQueryLayerInLocal(unittest.TestCase):

    def setUp(self):
        self._rpm = '/opt/kyclassifier/test.rpm'
        self.isinit = True if self._init_querylayerinlocal() else False
        
    def _init_querylayerinlocal(self):
        """
            Try to init querylayerinlocal object
        Returns:
            bool
        """
        try:
            self.obj = QueryLayerInLocal(self._rpm)
            return True
        except:
            return False
    
    def test_run(self):
        if os.path.exists(self._rpm) is False:
            self.skipTest("Test File not exists, test_check skiped!")
        result = QueryLayerInLocal.run([self.obj.rpm])
        self.assertIsInstance(result, int, "Test QueryLayerInLocal.run failed!")


    def test_get_rpm_layer(self):
        if self.isinit is False:
            self.skipTest("Test initialize for QueryLayerInLocal unfinished, test_get_rpm_layer skiped!")
        layer = self.obj.get_rpm_layer()
        self.assertIsInstance(layer,int,"QueryLayerInLocal.get_rpm_layer check failed!")
        

    def test_check(self):
        if os.path.exists(self._rpm) is False:
            self.skipTest("Test File not exists, test_check skiped!")
        result = QueryLayerInLocal.check(self.obj.rpm)
        self.assertIsInstance(result,bool,"Test QueryLayerInLocal.check failed!")


    def test_rpm(self):
        pass



if __name__ == '__main__':
    unittest.main(verbosity=2)
