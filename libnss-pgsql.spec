%define name libnss-pgsql
%define version 1.4.0
%define release %mkrel 8

Summary: NSS library for postgresql
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://ovh.dl.sourceforge.net/sourceforge/sysauth-pgsql/%{name}-%{version}.tar.bz2
Patch0: libnss-pgsql.includedir.patch
Patch1: libnss-pgsql.readconfigsilentfailed.patch
License: GPL
Group: System/Libraries
Url: http://sourceforge.net/projects/sysauth-pgsql
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: libpq-devel
BuildRequires: postgresql-devel
BuildRequires: xmlto
BuildRequires: automake1.4

%description
This library provide the capability to have all classical 
users definitions in a PostgreSQL server instead than in the
old plain text files in /etc passwd,group,shadow.

All is done without any trick or something like, simply 
connecting to the nss (name servica switch) facility 
offered by the libc (2.x) as nis and nisplus already did.

All without recompiling or touching any application 
configurations. Just compile and install nss_postgresql 
library and set up a PostgreSQL server.

%if %_lib != lib
%package -n %{_lib}nss-pgsql
Summary: NSS library for postgresql
Group: System/Libraries

%description -n %{_lib}nss-pgsql
This library provide the capability to have all classical 
users definitions in a PostgreSQL server instead than in the
old plain text files in /etc passwd,group,shadow.

All is done without any trick or something like, simply 
connecting to the nss (name servica switch) facility 
offered by the libc (2.x) as nis and nisplus already did.

All without recompiling or touching any application 
configurations. Just compile and install nss_postgresql 
library and set up a PostgreSQL server.
%endif

%prep
%setup -q
%patch0 -p0 -b .pgsqlinclude
%patch1 -p0 -b .readconfigsilentfailed

%build
%configure --libdir=/%_lib
%make CFLAGS="%optflags -fPIC"

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %buildroot/{%_lib,%_sysconfdir}
%makeinstall_std
install -m644 conf/nss-pgsql.conf %buildroot/%_sysconfdir/nss-pgsql.conf
install -m600 conf/nss-pgsql-root.conf %buildroot/%_sysconfdir/nss-pgsql-root.conf

rm -fr %buildroot/%_prefix/doc

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %_lib != lib
%files -n %{_lib}nss-pgsql
%else
%files
%endif
%defattr(-,root,root)
%doc conf/dbschema.sql README* TODO AUTHORS 
%doc doc/caution.png doc/nss-pgsql.html
/%_lib/libnss_pgsql.*
%config(noreplace) %_sysconfdir/*.conf
