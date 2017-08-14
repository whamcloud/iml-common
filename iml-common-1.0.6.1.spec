# Created by pyp2rpm-2.0.0
%global pypi_name iml-common

Name:           python-%{pypi_name}
Version:        1.0.6.1
Release:        1%{?dist}
Summary:        TODO:

License:        MIT
URL:            TODO:
Source0:        iml-common-1.0.6.1.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python2-setuptools_scm

%description
TODO:

%package -n     python2-%{pypi_name}
Summary:        TODO:
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
TODO:


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build

%install
%py2_install


%files -n python2-%{pypi_name} 
%doc README.md README.rst license.txt
%{python2_sitelib}/iml_common
%{python2_sitelib}/iml_common-%{version}-py?.?.egg-info

%changelog
* Mon Aug 14 2017 Brian J. Murrell,,, - 1.0.6.1-1
- Initial package.
