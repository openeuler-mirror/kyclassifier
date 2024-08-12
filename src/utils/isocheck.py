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

ERROR_INFO={
    1001:"The ISO path does not exist. Please check if the entered ISO path is correct.",
    1002:"The ISO file format is not correct. Please check if the input file is a server operating system ISO image file.",
}

class IsoCheck(object):
    def __init__(self,path):
        self.path=path
        
    def check_exist(self):
        if not os.path.exists(self.path):
            return False
        else:
            return True
        
    def check_format(self):
        pass
    
    @classmethod
    def check(cls,iso_path):
        obj = cls(iso_path)
        if not obj.check_exist():
            print(ERROR_INFO.get(1001,''))
            return False
        elif not obj.check_format():
            print(ERROR_INFO.get(1002,''))
            return False
        else:
            return True
