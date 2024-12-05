# -*- coding: utf-8 -*-
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
import unittest

from src.main.alglayer import AlgLayer
from src.utils.repocheck import RepoCheck


class DepObj(object):
    def __init__(self):
        self.dep_dict = {'kexec-tools':['bash', 'bzip2', 'coreutils', 'dracut', 'dracut-network', 'dracut-squash', 'elfutils-libelf', 'elfutils-libs', 'ethtool', 'glibc', 'lzo', 'ncurses-libs', 'sed', 'snappy', 'systemd', 'systemd-udev', 'xz-libs', 'zlib'],
                         'dbus-x11':['dbus-daemon', 'dbus-libs', 'glibc', 'libX11'],
                         'libevdev-help':[]}
        self.dep_by_dict = {'kexec-tools': ['anaconda'],'dbus-x11':['lightdm', 'tigervnc-server-minimal', 'ukui-power-manager', 'firewalld'],'libevdev-help':[]}
        self.all_pkgs = {'kexec-tools', 'dbus-x11', 'libevdev-help'}

    def get_pkg_all_deps(self,pkg_name):
        """
            解析输入软件包的所有南向依赖软件包
        Args:
            pkg_name (string): 软件包名

        Returns:
            set: 南向依赖软件包集合
        """
        dep_set = set()
        dep_pkgs_dict = self.dep_dict
        to_process = {pkg_name}
        while to_process:
            package = to_process.pop()
            dep_set.add(package)
            for dep in dep_pkgs_dict.get(package,set()):
                if dep not in dep_set:
                    to_process.add(dep)
                    dep_set.add(dep)
        dep_set.remove(pkg_name)
        return dep_set

class TestAlglayer(unittest.TestCase):
    """
        alglayer模块单元测试
    """

    def setUp(self):
        self.files_path = '/opt/kyclassifier/src/data/layer_data.json'
        self.depobj = DepObj()
    

    def _init_alglayer(self):
        """
            Try to init alglayer
        Returns:
            bool
        """
        try:
            self.alglayer = AlgLayer(self.depobj,self.files_path)
            return True
        except:
            return False

    def test_load_init_data(self):
        """
            Test class AlgLayer method _load_init_data()
        Returns:
            dict()
        """
        if not self._init_alglayer():
            self.skipTest("Init AlgLayer failed, test skiped!")
        else:
            result = self.alglayer._load_init_data(self.files_path)
            self.assertIsInstance(result, dict, "_load_init_data test failed!")
    
    def test_filter_init_dict(self):
        """
            Test class AlgLayer method filter_init_dict(()
        Returns:
            dict()
        """
        if not self._init_alglayer():
            self.skipTest("Init AlgLayer failed, test skiped!")
        else:
            result = self.alglayer.filter_init_dict(self.alglayer.init_id2pkgs_dict,self.depobj.all_pkgs)
            self.assertIsInstance(result, dict, "filter_init_dict( test failed!")
    
    def test_augment_layered_set(self):
        """
            Test class AlgLayer method augment_layered_seta()
        Returns:
            dict()
        """
        if not self._init_alglayer():
            self.skipTest("Init AlgLayer failed, test skiped!")
        else:
            result = self.alglayer.augment_layered_set(self.alglayer.init_id2pkgs_dict,self.depobj)
            self.assertIsInstance(result, dict, "augment_layered_set test failed!")
    
    def test_filter_duplicates(self):
        """
            Test class AlgLayer method filter_duplicates
        Returns:
            dict()
        """
        if not self._init_alglayer():
            self.skipTest("Init AlgLayer failed, test skiped!")
        else:
            result = self.alglayer.filter_duplicates(self.alglayer.init_id2pkgs_dict)
            self.assertIsInstance(result, dict, "filter_duplicates test failed!")
    
    def test_get_unlayered_pkgs(self):
        """
            Test class AlgLayer method get_unlayered_pkgs
        Returns:
            list
        """
        if not self._init_alglayer():
            self.skipTest("Init AlgLayer failed, test skiped!")
        else:
            result = self.alglayer.get_unlayered_pkgs(self.alglayer.init_id2pkgs_dict,self.depobj.all_pkgs)
            self.assertIsInstance(result, list, "get_unlayered_pkgs test failed!")
    
    def test_get_layer_by_reqlayer(self):
        """
            Test class AlgLayer method get_layer_by_reqlayer
        Returns:
            dict()
        """
        if not self._init_alglayer():
            self.skipTest("Init AlgLayer failed, test skiped!")
        else:
            result = self.alglayer.get_layer_by_reqlayer(self.alglayer.init_id2pkgs_dict,[],self.depobj)
            self.assertIsInstance(result, dict, "get_layer_by_reqlayer test failed!")
    def test_get_pkg2id_dict(self):
        """
            Test class AlgLayer method get_pkg2id_dict
        Returns:
            dict()
        """
        if not self._init_alglayer():
            self.skipTest("Init AlgLayer failed, test skiped!")
        else:
            result = self.alglayer.get_pkg2id_dict(self.alglayer.init_id2pkgs_dict)
            self.assertIsInstance(result, dict, "get_pkg2id_dict test failed!")
    
    def test_run(self):
        """
            Test class AlgLayer method run
        Returns:
            dict()
        """
        if not self._init_alglayer():
            self.skipTest("Init AlgLayer failed, test skiped!")
        else:
            result = self.alglayer.run(self.depobj,self.files_path)
            self.assertIsInstance(result, dict, "run test failed!")

if __name__ == "__main__":
    unittest.main(verbosity=2)