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

from collections import defaultdict

class DepParse(object):
    def __init__(self):
        self.dep_dict = defaultdict(list)
        self.dep_by_dict = defaultdict(list)
        self.all_pkgs = set()

    def get_pkg_all_deps(self,pkg_name):
        dep_set = set()
        dep_pkgs_dict = self.dep_dict
        to_process = {pkg_name}
        while to_process:
            package = to_process.pop()
            dep_set.add(package)
            for dep in dep_pkgs_dict.get(package,set()):
                if dep not in dep_set:
                    to_process.add(dep)
                    dep_set.add(dep)
        dep_set.remove(pkg_name)
        return dep_set

