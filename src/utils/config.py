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

class BaseConfig():
    """全局配置对象
    """
    # main
    LAYERDATA = '/opt/kyclassifier/src/data/layer_data.json'
    CLASSIFYDATA = '/opt/kyclassifier/src/data/classify_data.json'

    # dataparse, depparse, repocheck
    REPODATA = '/opt/kyclassifier/src/data/repos_data.json'

    # isocheck
    ISO_CHECK_ERROR_INFO={
        1001:"The ISO path does not exist. Please check if the entered ISO path is correct.",
        1002:"The ISO file format is not correct. Please check if the input file is a server operating system ISO image file.",
    }

    # repocheck
    REPO_CHECK_ERROR_INFO = {
        1001:'The repository configuration file does not exist. Please check if the file /opt/kyclassifier/src/data/repos_data.json exists',
        1002:'The currently configured repository is not available. Please check that the repository configuration in the file /opt/kyclassifier/src/data/repos_data.json is correct.',
    }

    RPM_CHECK_ERROR_INFO={
        1001:"The RPM path does not exist. Please check if the entered RPM path is correct.",
    }

    # util
    ISO_REPODATA_DIR = '/opt/kyclassifier/iso_parse/repodata'

    # logger
    LOGNAME='kyclassifier'
    LOG_PATH = '/opt/kyclassifier/output'
    LOG_FILE_NAME = "kyclassifier.log"
