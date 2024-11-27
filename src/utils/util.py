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
import time
import platform
from fnmatch import fnmatch
import isoparser


def get_formatted_time(fmt="%Y-%m-%d-%H-%M-%S"):
    """
        获取当前时间格式化输出
    Returns:
        formatted_time (str) : 格式化输出当前时间
    """
    formatted_time = time.strftime(fmt)
    return formatted_time

def trans_set2list(key2set_dict):
    """
        数据类型转换, set2list
    Args:
        key2set_dict (dict): 输入字典

    Returns:
        res: 输出转换类型后字典
    """
    return { k:list(v) for k,v in key2set_dict.items()}

def get_localos_data():
    """
        获取部署系统信息数据
    Returns:
        os_data (dict): 部署系统信息数据
    """
    with open('/etc/system-release','r') as f:
        os_info = f.read().strip()
    kernel_info = platform.release()
    if not isinstance(os_info,str):
        os_info = 'linux'
    if not isinstance(kernel_info,str):
        kernel_info = 'unknown'
    os_data = {
    "os_info": os_info,
    "kernel_info":kernel_info
    }
    return os_data

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

        for root, _, files in os.walk(path):
            for f in files:
                if fnmatch(f,'repomd.xml'):
                    repomd_path = os.path.join(root, f)
                    repomd_fn.append(repomd_path)
                elif fnmatch(f,'*primary.xml.*'):
                    primary_path = os.path.join(root, f)
                    primary_fn.append(primary_path)
                elif fnmatch(f,'*filelists.xml.*'):
                    filelists_path = os.path.join(root, f)
                    filelists_fn.append(filelists_path)
                else:
                    continue

        if any(len(x)!=1 for x in [repomd_fn,primary_fn,filelists_fn]):
            raise FileExistsError
        else:
            return repomd_fn[0], primary_fn[0], filelists_fn[0]

    @classmethod
    def parse_iso_repofile(cls,iso_path,target_dir='/opt/kyclassifier/iso_parse/repodata'):
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