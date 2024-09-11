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
import copy

class AlgLayer(object):
    """
        分层算法模块
    """
    def __init__(self,dep_obj,init_f=''):
        self.init_id2pkgs_dict = self._load_init_data(init_f)
        self.dep_obj = dep_obj
        self.all_pkgs_set = dep_obj.all_pkgs
        
    def _load_init_data(self,init_f):
        """
            加载初始分层数据json文件
        Args:
            init_f (str): 初始化数据文件路径

        Returns:
            res (dict): 初始化分分层字典
        """
        res = {}
        with open(init_f,'r',encoding='utf-8') as f:
            tmp = json.load(f)
        for k,v in tmp.items():
            res[int(k)] = copy.deepcopy(v)
        return res
    
    @classmethod
    def run(cls):
        pass

    @classmethod
    def filter_init_dict(cls,id2pkgs_dict,all_pkgs_set):
        """
            排除不在集合中的软件包，生成新的分层字典
        Args:
            id2pkgs_dict (dict): 初始化分层字典
            all_pkgs_set (set): 软件包名集合

        Returns:
            res_dict: 输出分层字典
        """
        res_dict = {k:[] for k in range(1,5)}
        for k,v in id2pkgs_dict.items():
            res_dict[k] = list(set(v) & set(all_pkgs_set))
        return res_dict