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

from src.utils.util import get_formatted_time, trans_set2list, get_localos_data


class TestUtil(unittest.TestCase):

    def setUp(self):
        """
        """
        pass

    def tearDown(self):
        """
        """
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
