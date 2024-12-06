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
import sys
current_path = os.path.dirname(__file__)
parent_path = os.path.dirname(current_path)
sys.path.append(parent_path)

from rpmquery import RpmQuery
from utils.util import ISOUtils
from utils.depparse import ISODepParse
from utils.config import BaseConfig
from main.alglayer import AlgLayer


class QueryLayerInIso(RpmQuery):

    def __init__(self,rpm,iso):
        self._rpm = rpm
        self._iso = iso
        self._get_isofiles()

    def get_rpm_layer(self):
        """查询rpm层级
        """
        pass

    def _get_rpmdeps(self):
        """获取rpm包在iso中的南向依赖包
        """
        pass

    def _get_isopkgs_layer(self):
        """
            获取isopkgs的分层结果
        Returns:
            res (dict)  
        """
        isodepobj = ISODepParse(self._isofiles)
        res = AlgLayer.run(isodepobj, BaseConfig.LAYERDATA)
        return res

    def _get_isofiles(self):
        """获取iso元数据
        """
        self._isofiles = ISOUtils.parse_iso_repofile(self.iso)

    def _check(self):
        """检查输入rpm、iso文件
        """
        pass

    @property
    def rpm(self):
        return self._rpm

    @property
    def iso(self):
        return self._iso

