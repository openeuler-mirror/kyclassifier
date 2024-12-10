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
import os
import struct

import pycdlib

from .exceptions import ISOCheckError
from .config import BaseConfig


class IsoCheck(object):
    """
        输入ISO检查模块,检查失败打印错误信息
    """
    def __init__(self,path):
        self.path=path
        
    def check_exist(self):
        """
            检查文件存在性
        """
        return os.path.exists(self.path)
        
    def check_format(self):
        """
            检查iso格式是否正确

        ISO文件必须包含repodata目录
        """
        if not os.path.isfile(self.path):
            return False
        iso = pycdlib.PyCdlib()
        try:
            check_result = False
            iso.open(self.path)
            entry = iso.get_entry(iso_path='/repodata')
            if entry.is_dir():
                check_result = True
            iso.close()
            return check_result
        except (ISOCheckError, pycdlib.pycdlibexception.PyCdlibException, struct.error) as e:
            print("Error checking ISO: {}".format(str(e)))
            return False
        
    @classmethod
    def check(cls,iso_path):
        """
            入口函数
        Args:
            iso_path (string): iso文件路径

        Returns:
            bool: True/False
        """
        obj = cls(iso_path)
        if not obj.check_exist():
            print(BaseConfig.ISO_CHECK_ERROR_INFO.get(1001,''))
            return False
        if not obj.check_format():
            print(BaseConfig.ISO_CHECK_ERROR_INFO.get(1002,''))
            return False
        return True
