Name:           perl-Consul
Version:        0.019
Release:        1%{?dist}
Summary:        Consul API
License:        Artistic 2.0
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Consul/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RO/ROBN/Consul-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
AutoReqProv:	no

%description
Consul API

%prep
%setup -q -n Consul-%{version}
%{__chmod} 644 README

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;

%{_fixperms} $RPM_BUILD_ROOT/*

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Oct 31 2016 Steve Hutchings - 1.22-1
- Initial Build

