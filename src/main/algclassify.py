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


class AlgClassify(object): 
    """
        分类算法模块
    """

    @classmethod
    def run(cls):
        """
            分类算法入口函数
        """
        pass

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
                res.update({name:rpm_group})
            else:
                continue
        return res