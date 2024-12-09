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

from src.rpmquery.rpmhdrinfo import RpmHdrInfo

rpmhdr = rpmhdr{
     'name':'test',
     'version':'1.0',
     'release':'1',
     'arch':'x86',
     'summary':'none',
     'description':'none',
     'license':'none',
     'url':'none'
}
      

class TestRpmHdrInfo(unittest.TestCase):
    '''
        RpmHdrInfo模块单元测试
    '''

    def setUp(self):
        self.rpmhdr = rpmhdr

    def _init_rpmhdrinfo(self):
        """
            Try to init rpmhdrinfo
        Returns:
            bool
        """
        try:
            self.rpmhdrinfo = RpmHdrInfo(self.rpmhdr)
            return True
        except:
            return False
    
    def test_as_dict(self):
        """
            Test class RpmHdrInfo method as_dict
        Returns:
            dict()
        """
        if not self._init_alglayer():
            self.skipTest("Init RpmHdrInfo failed, test skiped!")
        else:
            result = self.rpmhdrinfo.as_dict()
            self.assertIsInstance(result, dict, "as_dict test failed!")
    


if __name__ == "__main__":
    unittest.main(verbosity=2)