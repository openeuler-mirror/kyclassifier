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
    """RpmHdrInfo 数据类
    """
    def __init__(self, rpmhdr):
        self.rpmhdr = rpmhdr

        self.name = rpmhdr['name']
        self.version = rpmhdr['version']
        self.release = rpmhdr['release']
        self.arch = rpmhdr['arch']
        self.summary = rpmhdr['summary']
        self.description = rpmhdr['description']
        self.license = rpmhdr['license']
        self.url = rpmhdr['url']

    def __repr__(self):
        return f"<RpmHdrInfo({self.name}-{self.version}-{self.release}.{self.arch})>"

    def as_dict(self):
        """类属性字段转换为字典

        Returns:
            dict: 类属性字段转换的字典数据
        """
        return {
            'name' : self.name,
            'arch' : self.arch,
            'version' : self.version,
            'epoch' : self.epoch,
            'release' : self.release,
            'summary' : self.summary,
            'description' : self.description,
            'url' : self.url,
            'license': self.license,
            'vendor' : self.vendor,
            'group' : self.group,
            'sourcerpm' : self.rpm_sourcerpm,
            'requires' : self.requires
        }

    @property
    def epoch(self):
        """获取epoch对象的值

        Returns:
            str: epoch对应的值或空值
        """
        if hasattr(self.rpmhdr, "epoch"):
            return self.rpmhdr["epoch"]
        return None

    @property
    def vendor(self):
        """获取vendor对象的值

        Returns:
            str: vendor对应的值或空值
        """
        if hasattr(self.rpmhdr, "vendor"):
            return self.rpmhdr["vendor"]
        return None

    @property
    def group(self):
        """获取group对象的值

        Returns:
            str: group对应的值或空值
        """
        if hasattr(self.rpmhdr, "group"):
            return self.rpmhdr["group"]
        return ""
    
    @property
    def rpm_sourcerpm(self):
        """获取sourcerpm对象的值

        Returns:
            str: sourcerpm对应的值或空值
        """
        if hasattr(self.rpmhdr, "sourcerpm"):
            return self.rpmhdr["sourcerpm"]
        return ""

    @property
    def requires(self):
        """获取requires对象的值

        Returns:
            str: requires对应的值或空值
        """
        if hasattr(self.rpmhdr, "requires"):
            return self.rpmhdr["requires"]
        return []
