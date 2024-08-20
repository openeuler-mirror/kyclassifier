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


class ISODepParse(DepParse):
    def __init__(self,iso_path):
        super(ISODepParse,self).__init__()
        self._iso_path = iso_path
        # deps_dict   {pkg1:[pkg2,pkg3,...,pkgi]}
        self.dep_dict = self._get_repo_pkg_deps()
        self.dep_by_dict = self._get_repo_pkg_deps_by()
        self.all_pkgs = self._get_all_pkgs()

    def _get_all_pkgs(self):
        if isinstance(self.dep_dict,dict):
            res_set = set(self.dep_dict.keys())
        else:
            res_set = set()
        return res_set

    def _get_repo_pkg_deps(self):
        pass

    def _get_repo_pkg_deps_by(self):
        pass
