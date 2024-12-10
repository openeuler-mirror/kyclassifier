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

from .rpmquery import RpmQuery


class QueryLayerInRepo(RpmQuery):
    
    def __init__(self,rpm):
        pass

    def run(self):
        """入口函数
        """
        pass

    def get_rpm_layer(self):
        """查询rpm层级
        """
        pass

    def _get_rpmdeps(self):
        """获取rpm包在repo中的南向依赖包
        """
        pass

    def _get_repopkgs_layer(self):
        """获取repopkgs的分层结果
        """
        pass

    def check(self):
        """检查输入rpm以及配置的repo
        """
        pass

    @property
    def rpm(self):
        pass