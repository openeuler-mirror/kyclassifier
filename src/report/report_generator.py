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
import io
import os
import json
import time
import sys
from jinja2 import Environment, FileSystemLoader, select_autoescape

class ReportGenerator(object):
    """
    A generator to convert raw data to json file and html file
    """
    def __init__(self, category_path, id_path, result_path, file_name):
        self.category_path = category_path
        self.id_path = id_path
        self.result_path = result_path
        self.file_name = file_name
        self.flag = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        self.mod = 0o640
        self.work_dir = os.path.dirname(__file__)

    def _check_param_valid(self):
        for path in [self.category_path, self.id_path, self.base_path]:
            if not os.path.exists(path):
                raise Exception("The input data path not exist")

        if not os.path.exists(self.result_path):
            try:
                os.makedirs(self.result_path)
            except Exception as err:
                print("The input path not exist, generate report failed!")

    def _format_report_data(self):
        with open(self.category_path, 'r') as f:
            category_data = json.load(f)

        with open(self.id_path, 'r') as f:
            id_data = json.load(f)

        with open(self.base_path, 'r') as f:
            base_data = json.load(f)

        out_pie_data = {1:0, 2:0, 3:0, 4:0}
        out_category_data = {}
        out_id_data = []
        for name, id in id_data.items():
            out_pie_data[id] += 1
            category_list = category_data.get(name,[])

            for category_item in category_list:
                if out_category_data.get(category_item):
                    out_category_data[category_item]["count"] += 1
                    out_category_data[category_item]["pkgs"].append(name)
                else:
                    out_category_data[category_item] = { "count": 1, "pkgs": [name] }

            out_id_data.append({
                "name": name,
                "id": id,
                "category": category_list
            })

        return out_pie_data, out_category_data, out_id_data, base_data
    
    def _format_chart_data(self, pie_data,category_data):
        format_pie_data = []
        format_category_data = []
        format_sum_data = 0
        for name, value in pie_data.items():
            format_sum_data = format_sum_data + value
            format_pie_data.append({
                "name":name,
                "value":value
            })
        for name,value in category_data.items():
            boxID = str.replace(str(name), '/', '-')
            boxID = str.replace(boxID, ' ', '-')
            format_category_data.append({
                "desc":name+" 分类软件包数量: "+str(value["count"]),
                "boxID":boxID,
                "pkgs":value["pkgs"]
            })
        return format_pie_data,format_category_data, format_sum_data
    
    def _generate_html_file(self):
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        pie_data, category_data, id_data, base_data = self._format_report_data()
        pie_data, category_data,sum_data = self._format_chart_data(pie_data,category_data)
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'template')),autoescape=select_autoescape(["html", "xml"]),enable_async=False)
        template = env.get_template("category_and_id_report.html")
        report_template = template.render(
            start_time=start_time,
            base_data = base_data,
            list_data=id_data, 
            category_data=category_data,
            pie_data=pie_data, 
            sum_data=sum_data 
        )
        try:
            html_path = os.path.join(self.result_path, self.file_name)
            with io.open(html_path,'w',encoding='utf-8') as hf:
                hf.write(report_template) 
        except (SyntaxError, OSError) as err:
            raise Exception(err)

    def generate_result_file(self):
        self._check_param_valid()
        self._generate_html_file()

if __name__ == "__main__":
    # category_path: 分类json文件路径
    # id_path：分层josn文件路径
    # result_path：输出文件路径
    # base_path: 部署环境基础信息
    # file_name：输出文件名
    fenlei_json_file = sys.argv[1]
    fenceng_json_file = sys.argv[2]
    osinfo_json_file = sys.argv[3]
    result_path = sys.argv[4]
    result_file_name = sys.argv[5]
    report_generator = ReportGenerator(fenlei_json_file, fenceng_json_file, osinfo_json_file, result_path, result_file_name)
    report_generator.generate_result_file()