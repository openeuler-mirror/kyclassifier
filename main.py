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
import argparse

class kyClassifier:
    @staticmethod
    def process_iso(iso_path):
        pass


if __name__ == '__main__':
    options = ['-h\n',
               '                   -iso ISO_FILE_PATH\n']

    str_usage = 'kyclassifier ' + ' '.join(options)
    parser = argparse.ArgumentParser(usage=str_usage)
    parser.add_argument('-iso', type=str, help='Input ISO file path')
    args = parser.parse_args()
    if args.iso:
        kyClassifier.process_iso(args.iso)


