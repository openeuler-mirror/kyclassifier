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
import hawkey

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

class ISODataParse(object):
    """
        ISO数据解析模块
    """
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