%define _unpackaged_files_terminate_build 0 

Summary: High-performance HTTP accelerator
Name: varnish
Version: 5.1.2
Release: 1%{?dist}
License: BSD
Group: System Environment/Daemons
URL: http://www.varnish-cache.org/
Source0: http://repo.varnish-cache.org/source/%{name}-%{version}.tar.gz
Source1: https://github.com/varnishcache/pkg-varnish-cache/archive/varnish-config.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ncurses-devel groff pcre-devel readline-devel jemalloc-devel
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: logrotate
Requires: ncurses
Requires: pcre
Requires: jemalloc
Requires(pre): shadow-utils
Requires(post): /sbin/chkconfig, /usr/bin/uuidgen
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(preun): initscripts
Requires: gcc

%description
This is Varnish Cache, a high-performance HTTP accelerator.
Documentation wiki and additional information about Varnish is
available on the following web site: http://www.varnish-cache.org/

%package libs
Summary: Libraries for %{name}
Group: Development/Libraries
BuildRequires: ncurses-devel
%description libs
Libraries for %{name}.
Varnish Cache is a high-performance HTTP accelerator

%package libs-devel
Summary: Development files for %{name}-libs
Group: Development/Libraries
BuildRequires: ncurses-devel
Requires: varnish-libs = %{version}-%{release}

%description libs-devel
Development files for %{name}-libs
Varnish Cache is a high-performance HTTP accelerator

%prep
%setup -q -n varnish-%{version}
tar xzf %SOURCE1
ln -s pkg-varnish-cache-master/redhat redhat

%build
./autogen.sh
%configure --prefix=/usr --disable-static --localstatedir=/var/lib --with-rst2man=/bin/true
make %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p" 

mkdir -p %{buildroot}/var/lib/varnish
mkdir -p %{buildroot}/var/log/varnish
mkdir -p %{buildroot}/var/run/varnish
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
install -D -m 0644 etc/example.vcl %{buildroot}%{_sysconfdir}/varnish/default.vcl
install -D -m 0644 redhat/varnish.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/varnish
install -D -m 0644 redhat/varnish.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/varnish
install -D -m 0755 redhat/varnish.initrc %{buildroot}%{_initrddir}/varnish
install -D -m 0755 redhat/varnishncsa.initrc %{buildroot}%{_initrddir}/varnishncsa
install -D -m 0755 redhat/varnish_reload_vcl %{buildroot}%{_sbindir}/varnish_reload_vcl
echo %{_libdir}/varnish > %{buildroot}%{_sysconfdir}/ld.so.conf.d/varnish-%{_arch}.conf
rm -rf %{buildroot}/doc/sphinx/build

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sbindir}/*
%{_bindir}/*
%{_var}/lib/varnish
%attr(0700,varnish,varnish) %dir %{_var}/log/varnish
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_mandir}/man7/*.7*
#%doc LICENSE README doc/changes.rst
#%doc etc/builtin.vcl etc/example.vcl
%dir %{_sysconfdir}/varnish/
%config(noreplace) %{_sysconfdir}/varnish/default.vcl
%config(noreplace) %{_sysconfdir}/logrotate.d/varnish
%config(noreplace) %{_sysconfdir}/sysconfig/varnish
%{_initrddir}/varnish
%{_initrddir}/varnishncsa

%files libs
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_libdir}/varnish
%doc LICENSE
%config %{_sysconfdir}/ld.so.conf.d/varnish-%{_arch}.conf

%files libs-devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_includedir}/varnish
%{_libdir}/pkgconfig/varnishapi.pc
%{_datadir}/%{name}
%{_datadir}/aclocal/varnish.m4

%pre
getent group varnish >/dev/null || groupadd -r varnish
getent passwd varnish >/dev/null || \
       useradd -r -g varnish -d /var/lib/varnish -s /sbin/nologin \
               -c "Varnish Cache" varnish
exit 0

%post
/sbin/chkconfig --add varnish
/sbin/chkconfig --add varnishncsa 
chown varnish:varnish /var/log/varnish/varnishncsa.log 2>/dev/null || true
chown varnish:varnish /var/log/varnish/varnish.log 2>/dev/null || true
test -f /etc/varnish/secret || (uuidgen > /etc/varnish/secret && chmod 0600 /etc/varnish/secret)

%preun
if [ $1 -lt 1 ]; then
  # Package removal, not upgrade
  /sbin/service varnish stop > /dev/null 2>&1
  /sbin/service varnishncsa stop > /dev/null 2>%1
  /sbin/chkconfig --del varnish
  /sbin/chkconfig --del varnishncsa 
fi

%post libs -p /sbin/ldconfig

%postun libs 
/sbin/ldconfig

%changelog
* Mon Dec 05 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.4-3
- Dummy entry
