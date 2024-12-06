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
from src.utils.depparse import LocalInstalledDepParse
from src.utils.config import BaseConfig
from src.main.alglayer import AlgLayer


class QueryLayerInLocal(RpmQuery):

    def __init__(self,rpm):
        self._rpm = rpm

    def get_rpm_layer(self):
        """查询rpm层级
        """
        pass

    def _get_rpmdeps(self):
        """获取rpm包在local环境中的南向依赖包
        """
        pass

    def _get_localpkgs_layer(self):
        """
            获取localpkgs的分层结果
        Returns:
            res (dict)  
        """
        localdepobj = LocalInstalledDepParse()
        res = AlgLayer.run(localdepobj, BaseConfig.LAYERDATA)
        return res

    def _check(self):
        """检查输入rpm文件
        """
        pass

    @property
    def rpm(self):
        return self._rpm
