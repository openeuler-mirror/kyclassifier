# kyclassifier

#### Description
Use for analyzes layers and categories information of packages in openEuler.

#### Software Architecture
Supports x86_64 and aarch64 architecture systems

#### Installation

Tool Installation:
git clone https://gitee.com/openeuler/kyclassifier
mv kyclassifier kyclassifier-1.1
tar -czvf kyclassifier-1.1.tar.gz kyclassifier-1.1
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
mv kyclassifier-1.1.tar.gz ~/rpmbuild/SOURCES
cp kyclassifier-1.1/kyclassifier.spec ~/rpmbuild/SPECS
rpmbuild -ba ~/rpmbuild/SPECS/kyclassifier.spec
rpm -ivh ~/rpmbuild/RPMS/xxxx/kyclassifier-1.1-0.xxxx.rpm

Install dependent packages:
pip3 install pycdlib isoparser
yum install python3-hawkey

#### Instructions

kyclassifier -h 
usage: kyclassifier -h
                    -iso  ISO_FILE_PATH
                    -repo
                    -local
                    -console_log
                    -q_rpminiso

optional arguments:
  -h, --help  show this help message and exit
  -iso ISO    Input ISO file path
  -repo       Whether to analyze repo packages.
  -local      Whether to analyze local installed packages.
  -console_log  Output log to console.
  -q_rpminiso   Query input rpm layer in iso


#### Contribution

1.  Fork the repository
2.  Create Feat_xxx branch
3.  Commit your code
4.  Create Pull Request


#### Gitee Feature

1.  You can use Readme\_XXX.md to support different languages, such as Readme\_en.md, Readme\_zh.md
2.  Gitee blog [blog.gitee.com](https://blog.gitee.com)
3.  Explore open source project [https://gitee.com/explore](https://gitee.com/explore)
4.  The most valuable open source project [GVP](https://gitee.com/gvp)
5.  The manual of Gitee [https://gitee.com/help](https://gitee.com/help)
6.  The most popular members  [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
