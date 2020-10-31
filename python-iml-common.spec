%global srcname iml-common

%{?dist_version: %global source https://github.com/whamcloud/%{srcname}/archive/%{dist_version}.tar.gz}
%{?dist_version: %global archive_version %{dist_version}}
%{?!dist_version: %global source https://files.pythonhosted.org/packages/source/i/%{srcname}/%{srcname}-%{version}.tar.gz}
%{?!dist_version: %global archive_version %{version}}

Name:           python-%{srcname}
Version:        1.5.0
# Release Start
Release:    1%{?dist}
# Release End
Summary:        Common library used by multiple IML components
License:        MIT
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %{source}
BuildArch:      noarch
Group: Development/Libraries
Obsoletes:      python-iml-common1.4

%global _description %{expand:
A Python package that contains common components for the IML project Different
areas of the IML project utilise common code that is shared distributed through
this package.This packaging intends to improve code reuse and componentization
within the IML project.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python36-distro
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-iml-common
%defattr(-,root,root,-)
%license license.txt
%doc README.md README.rst
%{python3_sitelib}/iml_common-*.egg-info/
%{python3_sitelib}/iml_common/

%changelog
* Mon Nov 2 2020 Joe Grund <jgrund@whamcloud.com> 1.5.0-1
- Update to Python 3

* Tue Apr 30 2019 Joe Grund <jgrund@whamcloud.com> 1.4.5-1
- Update to imlteam/copr build system

* Tue May 29 2018 Brian J. Murrell <brian.murrell@intel.com> 1.4.4-2
- Add Obsoletes: python2-iml-common1.x

* Fri May 18 2018 Tom Nabarro <tom.nabarro@intel.com> 1.4.4-1
- Fix bug where module is checked for before loading

* Thu May 17 2018 Tom Nabarro <tom.nabarro@intel.com> 1.4.3-1
- Remove use of modprobe to test presence of kernel modules.
- Remove unused FirewallControl classes and relevant tests.

* Tue May 8 2018 Joe Grund <joe.grund@intel.com> 1.4.2-1
- Add back missing commit.

* Tue Mar 13 2018 Joe Grund <joe.grund@intel.com> 1.4.1-1
- include missing files.

* Tue Mar 13 2018 Brian J. Murrell <brian.murrell@intel.com> 1.4.0-1
- Package in stand-alone module

* Tue Feb 13 2018 Tom Nabarro <tom.nabarro@intel.com> 1.3.3-2
- Add explicit dependency on python-lockfile

* Tue Oct 17 2017 Tom Nabarro <tom.nabarro@intel.com> 1.3.3-1
- Update to upstream 1.3.3

* Wed Oct 11 2017 Tom Nabarro <tom.nabarro@intel.com> 1.3.2-1
- Update to upstream 1.3.2

* Tue Oct 10 2017 Joe Grund <joe.grund@intel.com> 1.3.1-1
- Update to upstream 1.3.1

* Wed Oct 04 2017 Joe Grund <joe.grund@intel.com> 1.3.0-1
- Update to upstream 1.3.0

* Tue Oct 03 2017 Brian J. Murrell <brian.murrell@intel.com> 1.2.0-1
- Update to upstream 1.2.0

* Thu Sep 28 2017  - 1.1.1-1
- Remove zfs object store on agent initialisation and termination.

* Fri Sep 15 2017  - 1.1.0-1
- Updates to remove force zpool imports.

* Fri Sep 15 2017  - 1.0.7-1

* Thu Aug 10 2017  - 1.0.6-1
- Initial package.
