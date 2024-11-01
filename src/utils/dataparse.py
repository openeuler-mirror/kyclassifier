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

RPMINFO = {
    'name' : '',
    'arch' : '',
    'version' : '',
    'epoch' : '',
    'release' : '',
    'summary' : '',
    'description' : '',
    'url' : '',
    'rpm_license': '',
    'rpm_vendor' : '',
    'rpm_group' : '',
    'rpm_sourcerpm' : '',
}

class DataParse(object):
    """
        软件包数据解析模块
    """
    def __init__(self):
        self.pkgs_name = set()
        self.pkgs_info = []
        
    def get_pkginfo_byname(self):
        pass

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
            pkginfo = copy.copy(RPMINFO)
            pkginfo['name'] = p.name
            pkginfo['arch'] = p.arch
            pkginfo['version'] = p.version
            pkginfo['epoch'] = str(p.epoch)
            pkginfo['release'] = p.release
            pkginfo['summary'] = p.summary
            pkginfo['description'] = p.description
            pkginfo['url'] = p.url
            pkginfo['rpm_license'] = p.license
            pkginfo['rpm_vendor'] = p.vendor
            pkginfo['rpm_group'] = p.group
            pkginfo['rpm_sourcerpm'] = p.sourcerpm
            res.append(pkginfo)
        return res

    def get_pkginfo_byname(self,pkgname):
        """
            通过pkgname获取pkginfos
        Args:
            pkgname (str)
        Returns:
            pkginfos (list) [info1,info2]
        """
        return self.pkgname_pkginfo_dict.get(pkgname)

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
        Returns:
            res: 仓库配置数据
        """
        repodata = '/opt/kyclassifier/src/data/repos_data.json'
        with open(repodata,'r') as f:
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
                pkginfo = copy.copy(RPMINFO)
                pkginfo['name'] = p.name
                pkginfo['arch'] = p.arch
                pkginfo['version'] = p.version
                pkginfo['epoch'] = str(p.epoch)
                pkginfo['release'] = p.release
                pkginfo['summary'] = p.summary
                pkginfo['description'] = p.description
                pkginfo['url'] = p.url
                pkginfo['rpm_license'] = p.license
                pkginfo['rpm_vendor'] = p.vendor
                pkginfo['rpm_group'] = p.group
                pkginfo['rpm_sourcerpm'] = p.sourcerpm
                res.append(pkginfo)
        return res

    def get_pkginfo_byname(self,pkgname):
        """
            通过pkgname获取pkginfos
        Args:
            pkgname (str)
        Returns:
            pkginfos (list) [info1,info2]
        """
        return self.pkgname_pkginfo_dict.get(pkgname)

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