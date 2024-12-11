# kyclassifier

#### 介绍
用于分析openEuler中包的图层和类别信息。

#### 软件架构
支持x86_64和aarch64架构系统


#### 安装教程

工具安装：<br>
git clone https://gitee.com/openeuler/kyclassifier<br>
mv kyclassifier kyclassifier-1.1<br>
tar -czvf kyclassifier-1.1.tar.gz kyclassifier-1.1<br>
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}<br>
mv kyclassifier-1.1.tar.gz ~/rpmbuild/SOURCES<br>
cp kyclassifier-1.1/kyclassifier.spec ~/rpmbuild/SPECS<br>
rpmbuild -ba ~/rpmbuild/SPECS/kyclassifier.spec<br>
rpm -ivh ~/rpmbuild/RPMS/xxxx/kyclassifier-1.1-0.xxxx.rpm<br>

依赖安装：<br>
yum install python3-hawkey<br>
pip3 install pycdlib Jinja2 MarkupSafe psutil<br>


#### 使用说明

kyclassifier -h<br> 
usage: kyclassifier -h<br>
                    -iso  ISO_FILE_PATH<br>
                    -repo<br>
                    -local<br>
                    -console_log<br>
                    -q_rpminiso<br>

optional arguments:<br>
  -h, --help  show this help message and exit<br>
  -iso ISO    Input ISO file path<br>
  -repo       Whether to analyze repo packages.<br>
  -local      Whether to analyze local installed packages.<br>
  -console_log  Output log to console.<br>
  -q_rpminiso   Query input rpm layer in iso<br>
  

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
