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

import hawkey

from .rpmquery import RpmQuery
from src.utils.depparse import LocalInstalledDepParse
from src.utils.config import BaseConfig
from src.main.alglayer import AlgLayer
from src.rpmquery.rpmcheck import RpmCheck
from src.log.logger import logger


class QueryLayerInLocal(RpmQuery):

    def __init__(self,rpm):
        self._rpm = rpm

    @classmethod
    def run(cls,args):
        """
            入口函数
        Returns:
            layer (int)
        """
        rpm = args[0]
        if not cls.check(rpm):
            return -1
        obj = cls(rpm)
        layer = obj.get_rpm_layer()
        logger.info("RPM file: {}\nRPM layer in Local: {}".format(rpm,layer))
        return layer

    def get_rpm_layer(self):
        """
            查询rpm层级
        Returns:
            layer (int)
        """
        layers = []
        rpmdeps = self._get_rpmdeps()
        localpkgs_layer = self._get_localpkgs_layer()
        for p in rpmdeps:
            l = localpkgs_layer.get(p,0)
            layers.append(l)
        return max(layers)

    def _get_rpmdeps(self):
        """
            获取rpm包在local环境中的南向依赖包
        Returns:
            req_l (list)
        """
        rpminfo = RpmQuery.get_rpminfo(self.rpm)
        sack = hawkey.Sack()
        sack.load_system_repo(build_cache=False)
        q = hawkey.Query(sack)
        req_objs = q.filter(provides=rpminfo.requires)
        req_l = {req_obj.name for req_obj in req_objs}
        return list(req_l)

    def _get_localpkgs_layer(self):
        """
            获取localpkgs的分层结果
        Returns:
            res (dict)  
        """
        localdepobj = LocalInstalledDepParse()
        return AlgLayer.run(localdepobj, BaseConfig.LAYERDATA)

    @classmethod
    def check(cls,rpm):
        """
            检查输入rpm文件
        Returns:
            bool
        """
        return RpmCheck.check(rpm)

    @property
    def rpm(self):
        return self._rpm
