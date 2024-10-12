Name:           kyclassifier
Version:        1.0
Release:        0
Summary:        Use for analyzes layers and categories information of packages in openEuler.
License:        Mulan PSL v2
Source0:        kyclassifier-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3

Requires: python3

%description
Use for analyzes layers and categories information of packages in openEuler.

%prep
%setup -q

%install
# kyclassifier install
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/opt/kyclassifier
mv main.py %{buildroot}/opt/kyclassifier

%files
%doc NOTICE LICENSES 
/opt/kyclassifier/main.py
%exclude /opt/kyclassifier/__pycache__

%clean
rm -rf %{buildroot}  
rm -rf 	%{_builddir}/*


%changelog
* Fri Aug 09 2024 Sheng Ding <dingsheng@kylinos.cn> -1.0-0
- Initial spec.