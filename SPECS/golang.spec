%global debug_package %{nil}
%global __strip /bin/true

Name: golang16
Version: 1.6.2
Release: 1%{?dist}
Summary: go 1.6.2

License: BSD
URL: http://golang.org           
Source0: https://storage.googleapis.com/golang/go%{version}.linux-amd64.tar.gz

Conflicts: golang

AutoReqProv: no

%description
golang 1.6.2


%prep
%setup -q -n go

%build
rm -f .hgignore .hgtags

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/usr/local/go

cp bin/* $RPM_BUILD_ROOT/%{_bindir}/.

cp -r . $RPM_BUILD_ROOT/usr/local/go/.

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/go
%{_bindir}/godoc
%{_bindir}/gofmt
/usr/local/go

