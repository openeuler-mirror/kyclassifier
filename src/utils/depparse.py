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
import copy
from collections import defaultdict
from fnmatch import fnmatch
import isoparser

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
    def __init__(self,iso_path):
        super(ISODepParse,self).__init__()
        self._iso_path = iso_path
        # deps_dict   {pkg1:[pkg2,pkg3,...,pkgi]}
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
        pass

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
    

class ISOUtils(object):
    """
        ISO处理工具类
    """
    
    @staticmethod
    def parse_iso_repodata(iso_path,repodata_dir='/opt/kyclassifier/iso_parse/repodata'):
        """
            解析ISO中repodata目录
        Args:
            iso_path (string): iso文件
            repodata_dir (string, optional): repodata目录. Defaults to '/opt/kyclassifier/iso_parse/repodata'.
        """
        os.makedirs(repodata_dir,exist_ok=True)
        iso = isoparser.parse(iso_path)
        for repo in iso.record(b'repodata').children:
            file_name = repo.name.decode('utf-8')
            content = repo.get_stream().read()
            with open(os.path.join(repodata_dir,file_name),'wb') as f:
                f.write(content)

    @staticmethod
    def get_repo_from_dir(repodata_dir='/opt/kyclassifier/iso_parse/repodata'):
        """
            解析repodata目录中数据文件
        Args:
            repodata_dir (str, optional): repodata目录. Defaults to '/opt/kyclassifier/iso_parse/repodata'.
        Returns:
            tuple: ISO数据文件路径
        """
        repomd_fn = []
        primary_fn = []
        filelists_fn = []
        path = repodata_dir
        for res in os.walk(path):
            files = res[-1]
            for f in files:
                if fnmatch(f,'repomd.xml'):
                    repomd_fn.append(f)
                elif fnmatch(f,'*primary.xml.*'):
                    primary_fn.append(f)
                elif fnmatch(f,'*filelists.xml.*'):
                    filelists_fn.append(f)
                else:
                    continue
        if any(len(x)!=1 for x in [repomd_fn,primary_fn,filelists_fn]):
            raise FileExistsError
        else:
            return os.path.join(path,repomd_fn[0]),os.path.join(path,primary_fn[0]),os.path.join(path,filelists_fn[0])

    @classmethod
    def parase_iso_repofile(cls,iso_path,target_dir='/opt/kyclassifier/iso_parse/repodata'):
        """
            解析ISO数据文件
        Args:
            iso_path (str): ISO文件
            target_dir (string, optional): 数据文件保存目录. Defaults to '/opt/kyclassifier/iso_parse/repodata'.
        Returns:
            tuple: ISO数据文件路径
        """
        cls.parse_iso_repodata(iso_path,target_dir)
        return cls.get_repo_from_dir()