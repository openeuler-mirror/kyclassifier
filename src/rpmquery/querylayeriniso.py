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

from rpmquery import RpmQuery


class QueryLayerInIso(RpmQuery):

    def __init__(self,rpm,iso):
        pass

    @classmethod
    def run(cls):
        # return rpm layer in iso 
        return ''

    def get_rpm_layer(self):
        """查询rpm层级
        """
        pass

    def _get_rpmdeps(self):
        """获取rpm包在iso中的南向依赖包
        """
        pass

    def _get_isopkgs_layer(self):
        """获取isopkgs的分层结果
        """
        pass

    def _get_isofiles(self):
        """获取iso元数据
        """
        pass

    def _check(self):
        """检查输入rpm、iso文件
        """
        pass

    @property
    def rpm(self):
        pass

    @property
    def iso(self):
        pass

