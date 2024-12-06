#-*- coding:utf-8 -*-
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

from .config import BaseConfig

class LocalCheck(object):
    """
        本地系统检查
    """

    @classmethod
    def check_pkgsmissreq(cls):
        """
            获取本地已安装软件包中，缺少依赖的软件包
        Returns:
            pkgs_missreq_dict: 软件包依赖缺失字典
        """
        pkgs_missreq_dict = dict()
        sack = hawkey.Sack()
        sack.load_system_repo(build_cache=False)
        q = hawkey.Query(sack)
        for p in q:
            p_name = p.name
            missreq_l = []
            for req in p.requires:
                if not str(req).startswith('rpmlib'):
                    provider_query = hawkey.Query(sack).filter(provides=str(req))
                    if not provider_query:
                        missreq_l.append(str(req))
            if missreq_l:
                pkgs_missreq_dict[p_name] = missreq_l
        
        return pkgs_missreq_dict

    @classmethod
    def check(cls):
        """
            本地检查入口函数
        """
        pkgs_missreq_dict = cls.check_pkgsmissreq()
        if pkgs_missreq_dict:
            print("{} : {}".format(BaseConfig.LOCAL_CHECK_ERROR_INFO.get(1001,''), str(pkgs_missreq_dict)))
        
        return True