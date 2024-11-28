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
import hawkey
import dnf

from .config import BaseConfig


class RpmInfo():
    """数据类
    """
    def __init__(self, obj):
        self.name = obj.name
        self.arch = obj.arch
        self.version = obj.version
        self.epoch = obj.epoch
        self.release = obj.release
        self.summary = obj.summary
        self.description = obj.description
        self.url = obj.url
        self.rpm_license = obj.license
        self.rpm_vendor = obj.vendor if hasattr(obj,'vendor') else ""
        self.rpm_group = obj.group
        self.rpm_sourcerpm = obj.sourcerpm

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
            'rpm_license': self.rpm_license,
            'rpm_vendor' : self.rpm_vendor,
            'rpm_group' : self.rpm_group,
            'rpm_sourcerpm' : self.rpm_sourcerpm
        }


class DataParse(object):
    """
        软件包数据解析模块
    """
    def __init__(self):
        self.pkgs_name = set()
        self.pkgs_info = []
        self.pkgname_pkginfo_dict = {}
        
    def get_pkginfo_byname(self, pkgname):
        """
            通过pkgname获取pkginfos
        Args:
            pkgname (str)
        Returns:
            pkginfos (list) [info1,info2]
        """
        return self.pkgname_pkginfo_dict.get(pkgname,[])

class ISODataParse(DataParse):
    """
        ISO数据解析模块
    """
    def __init__(self,files_path):
        """
        Args:
            files_path (tuple): ISO数据文件路径
        """
        super(ISODataParse,self).__init__()
        self.pkgs_name = self.get_pkgname_set(files_path)
        self.pkgs_info = self.get_pkgsinfo_list(files_path)
        self.pkgname_pkginfo_dict = self._list2dict(self.pkgs_info,"name")

    @classmethod
    def get_pkgname_set(cls,files_path):
        """
            获取pkgname集合
        Args:
            files_path (tuple): ISO数据文件路径

        Returns:
            pkgname_set (set): iso中pkgname集合
        """
        if not isinstance(files_path,tuple) or len(files_path) != 3:
            return set()
        pkgname_set = set()
        sack = hawkey.Sack()
        repo = hawkey.Repo("repo_parse")
        repo.repomd_fn,repo.primary_fn,repo.filelists_fn = files_path
        sack.load_repo(repo,load_filelists=True)
        q = hawkey.Query(sack)
        for p in q:
            if p.name:
                pkgname_set.add(p.name)
            else:
                continue
        return pkgname_set
    
    @classmethod
    def get_pkgsinfo_list(cls,files_path):
        """
            获取软件包信息列表
        Args:
            files_path (tuple): ISO数据文件路径
        Returns:
            res : iso中pkginfo列表
        """
        if not isinstance(files_path,tuple) or len(files_path) != 3:
            return []
        res = []
        sack = hawkey.Sack()
        repo = hawkey.Repo("repo_parse")
        repo.repomd_fn,repo.primary_fn,repo.filelists_fn = files_path
        sack.load_repo(repo,load_filelists=True)
        q = hawkey.Query(sack)
        for p in q:
            pkginfo = RpmInfo(p)
            res.append(pkginfo.as_dict())
        return res

    @classmethod
    def _list2dict(cls, dict_list, key):
        """
            数据格式转换list2dict
        Args:
            dict_list (list): [d1,d2,...]
            key (str): dict 中作为索引的key
        Returns:
            res (dict): {d[key]:[d1,d2,...], ...}
        """
        res = {}
        for d in dict_list:
            v = d.get(key)
            if v not in res.keys():
                res[v] = [d]
            else:
                res[v].append(d)
        return res

class RepoDataParse(DataParse):
    """
        仓库数据解析模块
    """
    def __init__(self):
        super(RepoDataParse,self).__init__()
        self.pkgs_name = self.get_pkgname_set()
        self.pkgs_info = self.get_pkgsinfo_list()
        self.pkgname_pkginfo_dict = self._list2dict(self.pkgs_info,"name")
    
    @classmethod
    def _load_data(cls):
        """
            加载仓库配置数据

            default path '/opt/kyclassifier/src/data/repos_data.json'
        Returns:
            res: 仓库配置数据
        """


        with open(BaseConfig.REPODATA, 'r') as f:
            res = json.load(f)
        return res

    @classmethod
    def get_pkgname_set(cls):
        """
            获取pkgname集合
        Returns:
            pkgname_set (set): repo中pkgname集合
        """
        res = set()
        repos = cls._load_data()
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
            pkg_a = base.sack.query().available()
            for p in pkg_a:
                if p.name:
                    res.add(p.name)
                else:
                    continue
        return res

    @classmethod
    def get_pkgsinfo_list(cls):
        """
            获取pkginfo列表
        Returns:
            res : repo中pkginfo列表
        """
        res = []
        repos = cls._load_data()
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
            pkg_a = base.sack.query().available()
            for p in pkg_a:
                pkginfo = RpmInfo(p)
                res.append(pkginfo.as_dict())
        return res

    @classmethod
    def _list2dict(cls, dict_list, key):
        """
            数据格式转换list2dict
        Args:
            dict_list (list): [d1,d2,...]
            key (str): dict 中作为索引的key
        Returns:
            res (dict): {d[key]:[d1,d2,...], ...}
        """
        res = {}
        for d in dict_list:
            v = d.get(key)
            if v not in res.keys():
                res[v] = [d]
            else:
                res[v].append(d)
        return res
    

class LocalInstalledDataParse(DataParse):
    """
        已安装软件包数据解析模块
    """

    def __init__(self):
        super(LocalInstalledDataParse,self).__init__()
        self.pkgs_name = self.get_pkgname_set()
        self.pkgs_info = self.get_pkgsinfo_list()
        self.pkgname_pkginfo_dict = self._list2dict(self.pkgs_info,"name")

    @classmethod
    def get_pkgname_set(cls):
        """
            获取pkgname集合
        Returns:
            pkgname_set (set): 本地已安装pkgname集合
        """
        res = set()
        sack = hawkey.Sack()
        sack.load_system_repo(build_cache=False)
        q = hawkey.Query(sack)
        for p in q:
            if p.name:
                res.add(p.name)
            else:
                continue
        return res

    @classmethod
    def get_pkgsinfo_list(cls):
        """
            获取本地已安装软件包的基本信息
        Returns:
            res (list): 软件包信息列表
        """
        res = []
        sack = hawkey.Sack()
        sack.load_system_repo(build_cache=False)
        q = hawkey.Query(sack)
        for p in q:
            pkginfo = RpmInfo(p)
            res.append(pkginfo.as_dict())
        return res


    @classmethod
    def _list2dict(cls, dict_list, key):
        """
            数据格式转换list2dict
        Args:
            dict_list (list): [d1,d2,...]
            key (str): dict 中作为索引的key
        Returns:
            res (dict): {d[key]:[d1,d2,...], ...}
        """
        res = {}
        for d in dict_list:
            v = d.get(key)
            if v not in res.keys():
                res[v] = [d]
            else:
                res[v].append(d)
        return res
