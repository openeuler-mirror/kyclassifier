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
import sys
import os
import shutil
import json
import argparse

from src.utils.isocheck import IsoCheck
from src.utils.repocheck import RepoCheck
from src.utils import dataparse
from src.utils import depparse
from src.utils import util
from src.utils.util import ISOUtils
from src.main.alglayer import AlgLayer
from src.main.algclassify import AlgClassify

LAYERDATA = '/opt/kyclassifier/src/data/layer_data.json'
CLASSIFYDATA = '/opt/kyclassifier/src/data/classify_data.json'

class kyClassifier(object):

    @classmethod
    def process_iso(cls,iso_path,tmpdir='/opt/kyclassifier/iso_parse/repodata'):
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        files_path = ISOUtils.parse_iso_repofile(iso_path)
        depobj = depparse.ISODepParse(files_path)
        dataobj = dataparse.ISODataParse(files_path)
        layer_res = AlgLayer.run(depobj,LAYERDATA)
        classify_res =AlgClassify.run(dataobj,CLASSIFYDATA)
        cls.save_output(layer_res,classify_res)

    @classmethod
    def process_repo(cls):
        depobj = depparse.RepoDepParse()
        dataobj = dataparse.RepoDataParse()
        layer_res = AlgLayer.run(depobj,LAYERDATA)
        classify_res =AlgClassify.run(dataobj,CLASSIFYDATA)
        cls.save_output(layer_res,classify_res)
    
    @classmethod
    def process_local(cls):
        depobj = depparse.LocalInstalledDepParse()
        dataobj = dataparse.LocalInstalledDataParse()
        layer_res = AlgLayer.run(depobj,LAYERDATA)
        classify_res =AlgClassify.run(dataobj,CLASSIFYDATA)
        cls.save_output(layer_res,classify_res)

    @staticmethod
    def save_output(pkg2layer,pkg2category):
        JSON_OUTPATH = (
            (pkg2layer,'pkg2layer.json'),
            (pkg2category,'pkg2category.json'),
        )
        formatted_time = util.get_formatted_time()
        dir_path = '/opt/kyclassifier/output/{}/'.format(formatted_time)
        json_path = '{}json/'.format(dir_path)
        os.makedirs(dir_path)
        os.makedirs(json_path)
        for tup in JSON_OUTPATH:
            with open(json_path + tup[1],'w') as f:
                json.dump(tup[0],f)
        print(("Output json file saved at {}").format(json_path))    


if __name__ == '__main__':
    options = ['-h\n',
               '                   -iso  ISO_FILE_PATH\n',
               '                   -repo\n',
               '                   -local']

    str_usage = 'kyclassifier ' + ' '.join(options)
    parser = argparse.ArgumentParser(usage=str_usage)
    parser.add_argument('-iso', type=str, help='Input ISO file path')
    parser.add_argument('-repo', action = 'store_true', help='Whether to analyze repo packages.')
    parser.add_argument('-local', action = 'store_true', help='Whether to analyze local installed packages.')
    args = parser.parse_args()
    if args.iso:
        if not IsoCheck.check(args.iso):
            sys.exit(1)
        kyClassifier.process_iso(args.iso)
    if args.repo:
        if not RepoCheck.check():
            sys.exit(1)
        kyClassifier.process_repo()   
    if args.local:
        kyClassifier.process_local()  

