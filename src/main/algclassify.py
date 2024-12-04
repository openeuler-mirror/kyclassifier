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
import json
import os
import copy 
from itertools import chain
import re

class AlgClassify(object): 
    """
        分类算法模块
    """

    @classmethod
    def run(cls,data_obj,json_f):
        """
            分类算法入口函数
        Args:
            data_obj : DataParse类对象
            json_f (str): 分类数据json文件

        Returns:
            res: 分类字典
        """
        category_d1 = cls._get_pkg2category_by_jsonf(json_f)
        category_d2 = cls._get_pkg2category_by_rpmgroup(data_obj)
        category_d3 = cls._get_pkg2category_by_srcrpm(data_obj,category_d1,category_d2)
        category_d4 = cls._get_pkg2category_by_rpmfiles(data_obj)
        category_d5 = cls._get_pkg2category_by_rpmvendor(data_obj)
        res = cls._merge_pkg2category_dict(data_obj,category_d1,category_d2,category_d3,category_d4,category_d5)
        return res

    @staticmethod
    def _load_data(data_f):
        """
            加载分类数据json文件
        Args:
            data_f (str): 分类数据文件路径

        Returns:
            res (dict): 初始化分类字典
        """
        with open(data_f,'r',encoding='utf-8') as f:
            res = json.load(f)
        return res

    @staticmethod
    def _get_pkgs(data_obj):
        """
            获取所有软件包名集合
        Args:
            data_obj: DataParse类对象

        Returns:
            软件包名集合
        """
        return data_obj.pkgs_name
    
    @staticmethod
    def _get_pkg2category_by_rpmgroup(data_obj):
        """
            通过rpmgroup获取软件包类别
        Args:
            data_obj: DataParse类对象

        Returns:
            res: 分类字典
        """
        res = {}
        invalid_labels = ['Unspecified','']
        pkgsinfo = data_obj.pkgs_info
        for p in pkgsinfo:
            name = p.get('name')
            rpm_group = p.get('rpm_group')
            if rpm_group not in invalid_labels:
                res.update({name:[rpm_group]})
            else:
                continue
        return res
    
    @staticmethod
    def _get_pkg2category_by_rpmfiles(data_obj):
        """
            通过软件包文件列表添加软件包类别信息
        Args:
            data_obj: DataParse类对象

        Returns:
            res: 分类字典
        """

        pattern_dict = {
            '^/usr/share/man/' : '帮助与文档',
            '^/usr/share/doc/' : '帮助与文档',
            '^/usr/lib/systemd/system/.*\.service$' : '服务'
        }
        res = {}
        pkgsinfo = data_obj.pkgs_info
        for p in pkgsinfo:
            name = p.get('name')
            rpm_files = p.get('rpm_files')
            classlist = []
            for pattern,classinfo in pattern_dict.items():
                for file in rpm_files:
                    if re.match(pattern, file):
                        classlist.append(classinfo)
                        break
            res[name] = list(set(classlist))
        return res
    
    @staticmethod
    def _get_pkg2category_by_rpmvendor(data_obj):
        """
            通过软件包vendor信息对第三方软件包分类
        Args:
            data_obj: DataParse类对象

        Returns:
            res: 分类字典
        """
        res = {}
        if not hasattr(data_obj,'os_vendor') or not data_obj.os_vendor:
            return res
        pkgsinfo = pkgsinfo = data_obj.pkgs_info
        for p in pkgsinfo:
            rpm_vendor = p.get('rpm_vendor', '')
            if rpm_vendor != data_obj.os_vendor:
                res[p['name']] = ['第三方软件包']
        return res

    @staticmethod
    def _get_pkg2category_by_srcrpm(data_obj,*args):
        """
            通过所属源码包信息补充软件包类别
        Args:
            data_obj: DataParse类对象

        Returns:
            no_classinfo_dict: 分类字典
        """
        pkgnames = data_obj.pkgs_name
        res = { p:[] for p in pkgnames}
        dict_l = [d for d in args] if args else []
        for p in pkgnames:
            category_l = [d.get(p,[]) for d in dict_l]
            category = list(chain.from_iterable(category_l))
            res[p] = copy.deepcopy(category)

        # 对无分类信息的软件包，通过所属源码包信息获取软件包类别
        no_classinfo_dict = { p:v for p,v in res.items() if not v}
        for p,v in no_classinfo_dict.items():
            # 获取无分类信息的二进制包所属的源码包
            # 将该源码包下其它二进制包的分类信息，同步到该二进制包
            srcrpm_list = [d.get('rpm_sourcerpm', '') for d in data_obj.pkgname_pkginfo_dict.get(p, [])]
            rpmname_list = []
            for srcrpm in srcrpm_list:
                rpmname_list.extend([d.get('name', '') for d in data_obj.srcrpm_pkginfo_dict.get(srcrpm, []) if d.get('name', '') != p])
            lists = [res.get(rpmname, []) for rpmname in rpmname_list]
            no_classinfo_dict[p] = list(set(list(chain(*lists))))

        return no_classinfo_dict

    @classmethod
    def _get_pkg2category_by_jsonf(cls,jsonf):
        """
            通过json文件获取软件包类别
        Args:
            jsonf (str): 分类数据json文件

        Returns:
            res: 分类字典
        """
        res = {}
        if os.path.exists(jsonf):
            try:
                res = cls._load_data(jsonf)
            except (IOError, json.JSONDecodeError) as e:
                print('Failed to load classify data file: {} ,skip load classify data.\nERROR: {}'.format(jsonf,e))
            return res
        else:
            print('File {} not exists,skip load classify data.'.format(jsonf))
            return res

    @classmethod
    def _merge_pkg2category_dict(cls,data_obj,*args):
        """
            合并分类数据
        Args:
            data_obj: DataParse类对象

        Returns:
            res: 分类字典
        """
        pkgnames = list(cls._get_pkgs(data_obj))
        res = { p:[] for p in pkgnames}
        dict_l = [d for d in args] if args else []
        for p in pkgnames:
            category_l = [d.get(p,[]) for d in dict_l]
            category = list(chain.from_iterable(category_l))
            res[p] = copy.deepcopy(category)
        for p,v in res.items():
            if not v :
                res[p] = ['其它']
        return res