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

import rpm

from rpmhdrinfo import RpmHdrInfo

class RpmQuery(object):
    """
        rpm查询模块
    """

    def __init__(self):
        pass

    def get_rpm_layer(self):
        """
            查询rpm层级
        """
        pass
    
    def get_rpm_category(self):
        """
            查询rpm类别
        """
        pass

    @classmethod
    def get_rpminfo(cls,rpmpath):
        """
            获取rpminfo 
        """
        # Rpmcheck 
        ts = rpm.TransactionSet("/",rpm._RPMVSF_NOSIGNATURES)
        hdr = ts._f2hdr(rpmpath)
        rpminfo = RpmHdrInfo(hdr)
        return rpminfo
