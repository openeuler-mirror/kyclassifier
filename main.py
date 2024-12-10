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
from src.utils.localcheck import LocalCheck
from src.utils import dataparse
from src.utils import depparse
from src.utils import util
from src.utils.util import ISOUtils
from src.utils.config import BaseConfig
from src.utils.programcheck import find_processes_with_cmdline_keyword
from src.main.alglayer import AlgLayer
from src.main.algclassify import AlgClassify
from src.log.logger import logger, LOGGER
from src.report.report_generator import ReportGenerator
from src.rpmquery.querylayeriniso import QueryLayerInIso
from src.rpmquery.querylayerinlocal import QueryLayerInLocal

class kyClassifier(object):

    @classmethod
    def process_iso(cls,iso_path,tmpdir='/opt/kyclassifier/iso_parse/repodata'):
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        files_path = ISOUtils.parse_iso_repofile(iso_path)
        depobj = depparse.ISODepParse(files_path)
        dataobj = dataparse.ISODataParse(files_path)
        layer_res = AlgLayer.run(depobj, BaseConfig.LAYERDATA)
        classify_res =AlgClassify.run(dataobj, BaseConfig.CLASSIFYDATA)
        cls.save_output(layer_res,classify_res)

    @classmethod
    def process_repo(cls):
        depobj = depparse.RepoDepParse()
        dataobj = dataparse.RepoDataParse()
        layer_res = AlgLayer.run(depobj, BaseConfig.LAYERDATA)
        classify_res =AlgClassify.run(dataobj, BaseConfig.CLASSIFYDATA)
        cls.save_output(layer_res,classify_res)
    
    @classmethod
    def process_local(cls):
        depobj = depparse.LocalInstalledDepParse()
        dataobj = dataparse.LocalInstalledDataParse()
        layer_res = AlgLayer.run(depobj, BaseConfig.LAYERDATA)
        classify_res =AlgClassify.run(dataobj, BaseConfig.CLASSIFYDATA)
        cls.save_output(layer_res,classify_res)

    @staticmethod
    def save_output(pkg2layer,pkg2category):
        os_data = util.get_localos_data()
        JSON_OUTPATH = (
            (pkg2layer,'pkg2layer.json'),
            (pkg2category,'pkg2category.json'),
            (os_data,'osinfo.json')
        )
        formatted_time = util.get_formatted_time()
        dir_path = '/opt/kyclassifier/output/{}/'.format(formatted_time)
        logfile_path = '/opt/kyclassifier/output/kyclassifier.log'
        json_path = '{}json/'.format(dir_path)
        html_path = '{}html/'.format(dir_path)
        os.makedirs(dir_path)
        os.makedirs(json_path)
        os.makedirs(html_path)
        for tup in JSON_OUTPATH:
            with open(json_path + tup[1],'w') as f:
                json.dump(tup[0],f)
        
        report_generator = ReportGenerator(
            os.path.join(json_path,'pkg2category.json'),
            os.path.join(json_path,'pkg2layer.json'),
            os.path.join(json_path,'osinfo.json'),
            html_path,
            'Report.html')
        report_generator.generate_result_file()
        logger.info(("Output json file saved at {}").format(json_path))
        logger.info(("Output html file saved at {}").format(html_path))
        logger.info(("Output log file saved at {}").format(logfile_path))
         


if __name__ == '__main__':
    options = ['-h\n',
               '                   -iso  ISO_FILE_PATH\n',
               '                   -repo\n',
               '                   -local\n',
               '                   -console_log\n',
               '                   -q_rpminiso  RPM_FILE_PATH ISO_FILE_PATH\n',
               '                   -q_rpminlocal  RPM_FILE_PATH']

    str_usage = 'kyclassifier ' + ' '.join(options)
    parser = argparse.ArgumentParser(usage=str_usage)
    parser.add_argument('-iso', type=str, help='Input ISO file path')
    parser.add_argument('-repo', action = 'store_true', help='Whether to analyze repo packages.')
    parser.add_argument('-local', action = 'store_true', help='Whether to analyze local installed packages.')
    parser.add_argument('-console_log', action = 'store_true', default = True, help='Output log to console.')
    parser.add_argument('-q_rpminiso', type=str, nargs=2, help='Query input rpm layer in iso.')
    parser.add_argument('-q_rpminlocal', type=str, nargs=1, help='Query input rpm layer in local.')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    if args.console_log:
        LOGGER.update_console_log(logger)
    
    #进程检查函数
    find_processes_with_cmdline_keyword('kyclassifier')

    logger.info("Start run kyclassifier...")
    if args.iso:
        if not IsoCheck.check(args.iso):
            sys.exit(1)
        kyClassifier.process_iso(args.iso)
    if args.repo:
        if not RepoCheck.check():
            sys.exit(1)
        kyClassifier.process_repo()   
    if args.local:
        if not LocalCheck.check():
            sys.exit(1)
        kyClassifier.process_local()
    if args.q_rpminiso:
        layer = QueryLayerInIso.run(args.q_rpminiso)
        if layer < 0:
            logger.error("Check error,skipped query rpm layer in iso.")
        else:
            logger.info("Rpm layer in iso is {}".format(layer))
    if args.q_rpminlocal:
        layer = QueryLayerInLocal.run(args.q_rpminlocal)
        if layer < 0:
            logger.info("Check error,skipped query rpm layer in local.")
        else:
            logger.info("Rpm layer in local is {}".format(layer))

    logger.info("Kyclassifier end!")
