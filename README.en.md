# kyclassifier

#### Description
Use for analyzes layers and categories information of packages in openEuler.

#### Software Architecture
Supports x86_64 and aarch64 architecture systems

#### Installation

Tool Installation:<br>
git clone https://gitee.com/openeuler/kyclassifier<br>
mv kyclassifier kyclassifier-1.1<br>
tar -czvf kyclassifier-1.1.tar.gz kyclassifier-1.1<br>
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}<br>
mv kyclassifier-1.1.tar.gz ~/rpmbuild/SOURCES<br>
cp kyclassifier-1.1/kyclassifier.spec ~/rpmbuild/SPECS<br>
rpmbuild -ba ~/rpmbuild/SPECS/kyclassifier.spec<br>
rpm -ivh ~/rpmbuild/RPMS/xxxx/kyclassifier-1.1-0.xxxx.rpm<br>

Install dependent packages:<br>
pip3 install pycdlib isoparser<br>
yum install python3-hawkey<br>

#### Instructions

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
