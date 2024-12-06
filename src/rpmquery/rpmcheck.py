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
from src.utils.config import BaseConfig
import subprocess


class RpmCheck(object):
    """
        rpm检查模块
    """

    def __init__(self,path):
        self.path=path
        
    def check_exist(self):
        """
            检查软件包存在性
        """
        return os.path.exists(self.path)
    
    def check_formate(self):
        try:
            # 使用rpm命令查询RPM文件信息
            result = subprocess.run(['rpm', '-qip', self.path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # 检查命令是否成功执行
            if result.returncode != 0:
                print(f"Error querying RPM file {self.path}: {result.stderr}")
                return False
            return True
        except Exception as e:
            print(f"Error querying RPM file {self.path}: {e}")
            return False
        
    @classmethod
    def check(cls,rpm_path):
        """
            入口函数
        Args:
            rpm_path (string): rpm文件路径

        Returns:
            bool: True/False
        """
        obj = cls(rpm_path)
        if not obj.check_exist():
            print(BaseConfig.RPM_CHECK_ERROR_INFO.get(1001,''))
            return False
        if not obj.check_formate():
            print(BaseConfig.RPM_CHECK_ERROR_INFO.get(1002,''))
            return False
        return True

