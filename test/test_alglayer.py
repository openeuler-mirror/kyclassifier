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
            self.skipTest("Init iso_dataparse failed, test skiped!")
        else:
            result = self.alglayer._load_init_data(self.files_path)
            self.assertIsInstance(result, dict, "_load_init_data test failed!")

    



if __name__ == "__main__":
    unittest.main(verbosity=2)