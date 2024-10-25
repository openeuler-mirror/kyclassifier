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
import copy
import json
from collections import defaultdict
import hawkey
import dnf

class DepParse(object):
    """
        依赖解析模块
    """
    def __init__(self):
        self.dep_dict = defaultdict(list)
        self.dep_by_dict = defaultdict(list)
        self.all_pkgs = set()

    def get_pkg_all_deps(self,pkg_name):
        """
            解析输入软件包的所有南向依赖软件包
        Args:
            pkg_name (string): 软件包名

        Returns:
            set: 南向依赖软件包集合
        """
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
    """
        ISO软件包依赖解析模块
    """
    def __init__(self,files_path):
        super(ISODepParse,self).__init__()
        self._files_path = files_path
        self.dep_dict = self._get_repo_pkg_deps()
        self.dep_by_dict = self._get_repo_pkg_deps_by()
        self.all_pkgs = self._get_all_pkgs()

    def _get_all_pkgs(self):
        """
            解析iso中所有软件包名集合
        Returns:
            set: iso中所有软件包名集合
        """
        if isinstance(self.dep_dict,dict):
            res_set = set(self.dep_dict.keys())
        else:
            res_set = set()
        return res_set

    def _get_repo_pkg_deps(self):
        """
            解析软件包南向依赖关系
        Returns:
            dict: 软件包南向依赖关系字典
        """
        package_dep_d = defaultdict(list)
        sack = hawkey.Sack()
        repo = hawkey.Repo("repo_parse")
        repo.repomd_fn,repo.primary_fn,repo.filelists_fn = self._files_path
        sack.load_repo(repo,load_filelists=True)
        q = hawkey.Query(sack)
        for p in q:
            p_name = p.name
            req_l = []
            req_objs = q.filter(provides=p.requires)
            for req_obj in req_objs:
                req_pkgname = req_obj.name
                req_l.append(req_pkgname)
            package_dep_d[p_name] = req_l
        return package_dep_d

    def _get_repo_pkg_deps_by(self):
        """
            解析软件包北向依赖关系
        Returns:
            dict: 软件包北向依赖关系字典
        """
        deps_by_dict = defaultdict(list)
        dep_pkgs_dict = copy.deepcopy(self.dep_dict)
        for p in dep_pkgs_dict.keys():
            deps_by_dict[p]
        for k,v in dep_pkgs_dict.items():
            if not v:
                continue
            else:
                for dep_pkg in v:
                    tmp_k = dep_pkg
                    if tmp_k not in deps_by_dict.keys():
                        deps_by_dict[tmp_k] = [k]
                    else:
                        tmp_v = deps_by_dict.get(tmp_k)
                        tmp_v.append(k)
                        tmp_v = list(set(tmp_v))
                        deps_by_dict[tmp_k] = tmp_v
        return deps_by_dict
    

class RepoDepParse(DepParse):
    """
        仓库软件包依赖解析模块 
    """
    def __init__(self):
        self.dep_dict = self._get_repo_pkg_deps()
        self.dep_by_dict = self._get_repo_pkg_deps_by()
        self.all_pkgs = self._get_all_pkgs()

    def _load_data(self):
        """
            加载仓库配置数据
        Returns:
            res (list): 仓库配置数据
        """
        with open('/opt/kyclassifier/src/data/repos_data.json','r') as f:
            res = json.load(f)
        return res

    def _get_all_pkgs(self):
        """
            解析仓库中所有软件包名集合
        Returns:
            res_set (set): 仓库中所有软件包名集合
        """
        if isinstance(self.dep_dict,dict):
            res_set = set(self.dep_dict.keys())
        else:
            res_set = set()
        return res_set

    def _get_repo_pkg_deps(self):
        """
            获取repo仓库中所有软件包南向依赖
        Returns:
            package_dep_d: 软件包南向依赖字典
        """
        repos = self._load_data()
        package_dep_d = defaultdict(list)
        with dnf.Base() as base:
            conf = base.conf
            for r in repos:
                base.repos.add_new_repo(
                    r.get('repo_id'),
                    conf,
                    baseurl = [r.get('baseurl')],
                    sslverify=0,
                )
            base.fill_sack(load_system_repo=False)
            print("Enabled repositories:")
            for repo in base.repos.iter_enabled():
                print("id: {}".format(repo.id))
                print("baseurl: {}".format(repo.baseurl))
            q = base.sack.query()
        for p in q.available():
            package_dep_d[p.name] = list(set(map(lambda x : '{}'.format(x.name),q.filter(provides=p.requires))))
        return package_dep_d

    def _get_repo_pkg_deps_by(self):
        """
            获取repo仓库中所有软件包北向依赖
        Returns:
            dict: 软件包北向依赖字典
        """
        deps_by_dict = defaultdict(list)
        dep_pkgs_dict = copy.deepcopy(self.dep_dict)
        for p in dep_pkgs_dict.keys():
            deps_by_dict[p]
        for k,v in dep_pkgs_dict.items():
            if not v:
                continue
            else:
                for dep_pkg in v:
                    tmp_k = dep_pkg
                    if tmp_k not in list(deps_by_dict.keys()):
                        deps_by_dict[tmp_k] = [k]
                    else:
                        tmp_v = deps_by_dict.get(tmp_k)
                        tmp_v.append(k)
                        tmp_v = list(set(tmp_v))
                        deps_by_dict[tmp_k] = tmp_v
        return deps_by_dict 