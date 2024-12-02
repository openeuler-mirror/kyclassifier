Name:           kyclassifier
Version:        1.1
Release:        1
Summary:        Use for analyzes layers and categories information of packages in openEuler.
License:        Mulan PSL v2
Source0:        kyclassifier-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3

Requires: python3 python3-dnf python3-hawkey python3-six python3-pycdlib 

%description
Use for analyzes layers and categories information of packages in openEuler.

%prep
%setup -q

%install
# kyclassifier install
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/opt/kyclassifier
mv main.py %{buildroot}/opt/kyclassifier
mv src/ %{buildroot}/opt/kyclassifier
install -m 755 -D kyclassifier.sh %{buildroot}/usr/bin/kyclassifier

%files
%doc NOTICE LICENSES 
/opt/kyclassifier/
/usr/bin/kyclassifier

%clean
rm -rf %{buildroot}  
rm -rf 	%{_builddir}/*


%changelog
* Mon Dec 02 2024 ZhaoYu Jiang <jiangzhaoyu@kylinos.cn> - 1.1-1
- Enhanced Code Lint, Add Support for system-release not exist scenario, guarded RPMInfo attribute for not exist scenario.

* Tue Nov 26 2024 Sheng Ding <dingsheng@kylinos.cn> -1.1-0
- RPM packages can be analyzed in iso, repo, and local environments.

* Fri Aug 09 2024 Sheng Ding <dingsheng@kylinos.cn> -1.0-0
- Initial spec.
