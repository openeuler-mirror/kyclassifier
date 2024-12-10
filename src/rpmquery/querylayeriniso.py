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
from src.utils.util import ISOUtils
from src.utils.depparse import ISODepParse
from src.utils.config import BaseConfig
from src.main.alglayer import AlgLayer
from src.rpmquery.rpmcheck import RpmCheck
from src.utils.isocheck import IsoCheck
from src.log.logger import logger


class QueryLayerInIso(RpmQuery):

    def __init__(self,rpm,iso):
        self._rpm = rpm
        self._iso = iso
        self._isofiles = ISOUtils.parse_iso_repofile(self.iso)

    @classmethod
    def run(cls,args):
        if not cls.check(args):
            return -1
        rpm = args[0]
        iso = args[1]
        obj = cls(rpm,iso)
        layer = obj.get_rpm_layer()
        logger.info("RPM file: {}\nISO file: {}\nRPM layer in ISO: {}".format(rpm,iso,layer))
        return layer

    def get_rpm_layer(self):
        """
            查询rpm层级
        Returns:
            int
        """
        layers = []
        rpmdeps = self._get_rpmdeps()
        isopkgs_layer = self._get_isopkgs_layer()
        for p in rpmdeps:
            l = isopkgs_layer.get(p,0)
            layers.append(l)
        return max(layers)

    def _get_rpmdeps(self):
        """
            获取rpm包在iso中的南向依赖包
        Returns:
            list
        """
        rpminfo = RpmQuery.get_rpminfo(self.rpm)
        sack = hawkey.Sack()
        repo = hawkey.Repo("repo_parse")
        repo.repomd_fn, repo.primary_fn,repo.filelists_fn = self._isofiles
        sack.load_repo(repo,load_filelists=True)
        q = hawkey.Query(sack)
        req_objs = q.filter(provides=rpminfo.requires)
        req_l = {req_obj.name for req_obj in req_objs}
        return list(req_l)

    def _get_isopkgs_layer(self):
        """
            获取isopkgs的分层结果
        Returns:
            res (dict)  
        """
        isodepobj = ISODepParse(self._isofiles)
        return AlgLayer.run(isodepobj, BaseConfig.LAYERDATA)

    @classmethod
    def check(cls,args):
        """
            检查输入rpm、iso文件
        Returns:
            bool
        """
        rpm = args[0]
        iso = args[1]
        if RpmCheck.check(rpm) and IsoCheck.check(iso):
            return True
        return False

    @property
    def rpm(self):
        return self._rpm

    @property
    def iso(self):
        return self._iso

