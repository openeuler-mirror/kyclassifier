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


class ISOCheckError(Exception):
    """ISO check exception
    """
    def __init__(self, message):
        self.message = message
 
    def __str__(self):
        return f"ISOCheckError: {self.message}"

class ReportGenerateError(Exception):
    """app report generate error
    """
    def __init__(self, message):
        self.message = message
 
    def __str__(self):
        return f"ReportGenerateError: {self.message}"
