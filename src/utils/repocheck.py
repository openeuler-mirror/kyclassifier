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
import json

class RepoCheck(object):
    """
        输入仓库配置检查
    """
    REPO_DATA = '/opt/kyclassifier/src/data/repos_data.json'
    ERROR_INFO = {
        1001:'The repository configuration file does not exist. Please check if the file /opt/kyclassifier/src/data/repos_data.json exists',
        1002:'The currently configured repository is not available. Please check that the repository configuration in the file /opt/kyclassifier/src/data/repos_data.json is correct.',
    }

    @classmethod
    def check_exist(cls):
        """
            检查REPO_FILE 文件是否存在
        Returns:
            bool : 返回检查结果
        """
        if not os.path.exists(cls.REPO_DATA):
            return False
        else:
            return True
        
    @classmethod
    def _load_data(cls):
        """
            加载仓库配置数据
        Returns:
            repos (list): 仓库配置数据
        """
        try:
            with open(cls.REPO_DATA,'r') as f:
                repos = json.load(f)
                return repos
        except:
            return []

    def check_repo_useful(self):
        pass

    @classmethod
    def check(cls):
        """
            仓库检查入口函数
        """
        pass

