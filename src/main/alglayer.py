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
    def run(cls,dep_obj,init_f):
        """
            分层算法模块入口函数
        Args:
            dep_obj : DepParse类对象
            init_f (str): 初始化数据文件路径

        Returns:
            pkg2id_dict: 输出分层字典
        """
        obj = cls(dep_obj,init_f)
        id2pkgs_dict = obj.filter_init_dict(obj.init_id2pkgs_dict,obj.all_pkgs_set)
        id2pkgs_dict = cls.augment_layered_set(id2pkgs_dict,obj.dep_obj,add_no_depby_pkgs=True)
        id2pkgs_dict = cls.filter_duplicates(id2pkgs_dict)
        unfilter_pkg_list = cls.get_unlayered_pkgs(id2pkgs_dict,obj.all_pkgs_set)
        final_id2pkgs_dict = cls.get_layer_by_reqlayer(id2pkgs_dict,unfilter_pkg_list,obj.dep_obj)
        pkg2id_dict = cls.get_pkg2id_dict(final_id2pkgs_dict)
        return pkg2id_dict

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

    @classmethod
    def augment_layered_set(cls,id2pkgs_dict,dep_obj,add_no_depby_pkgs=True):
        """
            补充分层集合,把无被依赖软件包加入第4层;把每层的依赖包加入各层级；
        Args:
            id2pkgs_dict (dict): 输入分层字典
            dep_obj : DepParse类对象
            add_no_depby_pkgs (bool, optional): 控制是否将无被依赖软件包加入第4层,默认为True . Defaults to True.

        Returns:
            id2pkgs_dict: 输出分层字典
        """
        dep_by_dict = dep_obj.dep_by_dict
        if add_no_depby_pkgs:
            for k,v in dep_by_dict.items():
                if not v:
                    id2pkgs_dict[4].append(k)
        else:
            for id,p_list in copy.deepcopy(id2pkgs_dict).items():
                for p in p_list:
                    p_deps = dep_obj.get_pkg_all_deps(p)
                    id2pkgs_dict[id] += p_deps
                id2pkgs_dict[id] = list(set(id2pkgs_dict[id]))
        return id2pkgs_dict

    @classmethod
    def filter_duplicates(cls,id2pkgs_dict):
        """
            处理有多个层级的软件包，只保留最低层级
        Args:
            id2pkgs_dict (dict): 输入分层字典

        Returns:
            res_dict: 输出分层字典
        """
        visited_pkglist =[]
        res_dict = {k:[] for k in range(1,5)}
        for k,v in id2pkgs_dict.items():
            if k==1:
                res_dict[k] = list(set(v))
            else:
                res_dict[k] = list(set(v) - set(visited_pkglist))
            visited_pkglist += res_dict[k]
            visited_pkglist = list(set(visited_pkglist))
            res_dict[k] = list(set(res_dict[k]))
        return res_dict

    @classmethod
    def get_unlayered_pkgs(cls,id2pkgs_dict,all_pkgs_set):
        """
            获取还未分层软件包列表
        Args:
            id2pkgs_dict (dict): 输入分层字典
            all_pkgs_set (set): 所有软件集合

        Returns:
            res: 未分层软件包列表
        """
        layered_pkgs = []
        res = []
        for k,v in id2pkgs_dict.items():
            layered_pkgs += v
        res = list(set(all_pkgs_set) - set(layered_pkgs))
        return res

    @classmethod
    def get_layer_by_reqlayer(cls,id2pkgs_dict,unfilter_pkg_list,dep_obj):
        """
            通过依赖关系获取输入未分层软件包的层级
        Args:
            id2pkgs_dict (dict): 输入分层字典
            unfilter_pkg_list (list): 未分层软件包列表
            dep_obj : DepParse类对象

        Returns:
            res: 输出分层字典
        """
        tmp_dict = {k:[] for k in range(1,5)}
        turn = 0
        while True:
            turn += 1
            in_num = len(unfilter_pkg_list)
            for p in copy.copy(unfilter_pkg_list):
                p_deps_set = dep_obj.get_pkg_all_deps(p)
                for id in range(4,0,-1):
                    if p_deps_set & set(copy.copy(id2pkgs_dict[id])):
                        tmp_dict[id] += list(p_deps_set)
                        tmp_dict[id].append(p)
                        unfilter_pkg_list = list(set(unfilter_pkg_list) - p_deps_set -set(p)) 
                        break
            out_num = len(unfilter_pkg_list)
            condition = bool(in_num - out_num)
            if condition:
                continue
            else:
                tmp_dict[4] += unfilter_pkg_list
                break
        for i in range(1,5):
            id2pkgs_dict[i] += tmp_dict[i]
        id2pkgs_dict = cls.filter_duplicates(id2pkgs_dict)
        return id2pkgs_dict

    @classmethod
    def get_pkg2id_dict(cls,id2pkgs_dict):
        """
            获取pkgname为key,layer_id为value的分层字典
        Args:
            id2pkgs_dict (dict): id2pkg_dict

        Returns:
            res: pkg2id_dict
        """
        return {pkg: _id for _id, pkgs in id2pkgs_dict.items() for pkg in pkgs}
