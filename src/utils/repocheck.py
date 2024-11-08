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
import shutil
import subprocess

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

    @staticmethod
    def _create_repofile(repos_l):
        """
            创建.repo文件
        Args:
            repos_l (list): 仓库数据
        Returns:
            bool
        """
        if not repos_l:
            return False
        try:
            with open('/etc/yum.repos.d/check_tmp.repo','w') as f:
                repo_str = ''
                for r in repos_l:
                    tmp = '[{}]\nname = kyclassifier-{}\nbaseurl = {}\ngpgcheck = 0\nsslverify = 0\nenabled = 1\n'.format(r['repo_id'],r['repo_id'],r['baseurl'])
                    repo_str += tmp
                f.write(repo_str)
            return True
        except:
            return False

    @staticmethod
    def move_repofiles(src,dst):
        """
            移动src目录中的.repo 文件到dst目录
        Args:
            src (str)
            dst (str)
        """
        repo_files = [f for f in os.listdir(src) if f.endswith('.repo')]
        for repo_file in repo_files:
            src_path = os.path.join(src, repo_file)
            dst_path = os.path.join(dst, repo_file)
            try:
                shutil.move(src_path, dst_path)
            except IOError as e:
                print("Error moving '{}': {}".format(repo_file, e))

    @staticmethod
    def remove_repofiles(src):
        """
            删除src目录中的repo文件
        Args:
            src (str)
        """
        repo_files = [f for f in os.listdir(src) if f.endswith('.repo')]
        for repo_file in repo_files:
            file_path = os.path.join(src, repo_file)
            try:
                os.remove(file_path)
            except OSError as e:
                print("Error removing '{}': {}".format(file_path, e))

    @classmethod
    def check_repo_useful(cls):
        """
            检查配置的仓库是否可用
        Returns:
            res (bool)
        """
        repo_dir = '/etc/yum.repos.d'
        backup_dir = '/etc/yum.repos.d/check_bak'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        cls.move_repofiles(repo_dir,backup_dir)
        repos_l = cls._load_data()
        if not cls._create_repofile(repos_l):
            return False
        try:
            cmd = 'dnf clean all $1>/dev/null 2>&1 && dnf makecache  --setopt=retries=1 $1>/dev/null 2>&1'
            res = subprocess.call(cmd, shell=True)
        except:
            return False
        finally:
            cls.remove_repofiles(repo_dir)
            cls.move_repofiles(backup_dir,repo_dir)
            shutil.rmtree(backup_dir)
        if res == 0:
            return True
        else:
            return False

    @classmethod
    def check(cls):
        """
            仓库检查入口函数
        """
        if not cls.check_exist():
            print(cls.ERROR_INFO.get(1001,''))
            return False
        elif not cls.check_repo_useful():
            print(cls.ERROR_INFO.get(1002,''))
            return False
        else:
            return True

