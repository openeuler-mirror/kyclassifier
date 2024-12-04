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


class RpmHdrInfo():
    """
        RpmHdrInfo 数据类
    """
    def __init__(self, rpmhdr):
        self.name = rpmhdr['name']
        self.version = rpmhdr['version']
        self.release = rpmhdr['release']
        self.arch = rpmhdr['arch']
        self.summary = rpmhdr['summary']
        self.description = rpmhdr['description']
        self.license = rpmhdr['license']
        self.url = rpmhdr['url']

    def as_dict(self):
        """
            类属性字段转换为字典
        Returns:
            dict: 类属性字段转换的字典数据
        """
        pass

    @property
    def epoch(self):
        pass

    @property
    def vendor(self):
        pass

    @property
    def group(self):
        pass
    
    @property
    def rpm_sourcerpm(self):
        pass

    @property
    def requires(self):
        pass

