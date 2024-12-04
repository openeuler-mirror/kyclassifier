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

import pycdlib

from .config import BaseConfig

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
    try:
        with open('/etc/system-release','r') as f:
            os_info = f.read().strip()
    except FileNotFoundError:
        release_info = {}
        try:
            with open('/etc/os-release') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        release_info[key] = value.strip('"')
        except FileNotFoundError as e:
            raise FileNotFoundError(e)
        os_info = release_info["PRETTY_NAME"]
    kernel_info = platform.uname()
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
    def parse_iso_repodata(iso_path, repodata_dir=BaseConfig.ISO_REPODATA_DIR):
        """
            解析ISO中repodata目录
        Args:
            iso_path (string): iso文件
            repodata_dir (string, optional): repodata目录. Defaults to '/opt/kyclassifier/iso_parse/repodata'.
        """
        os.makedirs(repodata_dir,exist_ok=True)

        iso = pycdlib.PyCdlib()
        try:
            iso.open(iso_path)
            iso_path_dir = '/repodata'

            for child in iso.list_children(iso_path=iso_path_dir):
                if child.is_file():
                    file = child.file_identifier().decode()
                    path = os.path.join(iso_path_dir, file)

                    save_file = child.rock_ridge.name().decode()
                    with open(os.path.join(repodata_dir, save_file), 'wb') as f:
                        iso.get_file_from_iso_fp(f, iso_path=path)

            iso.close()
        except pycdlib.pycdlibexception.PyCdlibException as e:
            pass

    @staticmethod
    def get_repo_from_dir(repodata_dir=BaseConfig.ISO_REPODATA_DIR):
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
                subpath = os.path.join(root, f)
                if fnmatch(f,'repomd.xml'):
                    repomd_fn.append(subpath)
                elif fnmatch(f,'*primary.xml.*'):
                    primary_fn.append(subpath)
                elif fnmatch(f,'*filelists.xml.*'):
                    filelists_fn.append(subpath)
                else:
                    continue

        if any(len(x)!=1 for x in [repomd_fn,primary_fn,filelists_fn]):
            raise FileExistsError
        else:
            return repomd_fn[0], primary_fn[0], filelists_fn[0]

    @classmethod
    def parse_iso_repofile(cls,iso_path,target_dir=BaseConfig.ISO_REPODATA_DIR):
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
