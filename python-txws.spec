#
# Conditional build:
# We could run the tests when building, but txWS doesn't ship the tests.py with the distribution.
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module

%define	module txws
Summary:	Twisted WebSockets wrapper
Name:		python-txws
Version:	0.9.1
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://pypi.python.org/packages/source/t/txWS/txWS-%{version}.tar.gz
# Source0-md5:	d113910af0521ea62db8a0f3d7c63abb
URL:		http://pypi.python.org/pypi/txWS
Patch0:		%{name}-drop-vcversioner.patch
BuildRequires:	rpm-pythonprov
%if %{with python3}
BuildRequires:	python-TwistedCore
BuildRequires:	python-TwistedWeb
BuildRequires:	python-setuptools
BuildRequires:	python-six
%endif
%if %{with python3}
BuildRequires:	python3-TwistedWeb
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	python3-six
BuildRequires:	python3-twisted-core
%endif
Requires:	python-TwistedCore
Requires:	python-six
Requires:	python-twisted-web
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
txWS (pronounced "Twisted WebSockets") is a small, short, simple
library for adding WebSockets server support to your favorite Twisted
applications.

%package -n python3-txws
Summary:	Twisted WebSockets wrapper
Group:		Development/Languages
Requires:	python3-six
Requires:	python3-twisted-core
Requires:	python3-twisted-web

%description -n python3-txws
txWS (pronounced "Twisted WebSockets") is a small, short, simple
library for adding WebSockets server support to your favorite Twisted
applications.

%prep
%setup -q -n txWS-%{version}
%patch0 -p1

rm -r *.egg*

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3
%endif

%if %{with tests}
PYTHONPATH=$(pwd) trial tests.py
# XXX - also, python3 tests?
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%{py_sitescriptdir}/txws.py[co]
%{py_sitescriptdir}/txWS-%{version}-*.egg-info
%endif

%if %{with python3}
%files -n python3-txws
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/txws.py*
%{py3_sitescriptdir}/txWS-%{version}-*.egg-info
%endif
