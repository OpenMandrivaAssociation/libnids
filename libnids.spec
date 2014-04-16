%define major 1
%define libname %mklibname nids %{major}
%define devname %mklibname nids -d

Summary:	Library that provides functions of Network Intrusion Detection System 
Name:		libnids
Version:	1.24
Release:	4
License:	GPLv2+
Group:		Networking/Other
Url:		http://libnids.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/libnids/%{name}-%{version}.tar.gz
Source1:	http://prdownloads.sourceforge.net/libnids/%{name}-%{version}.tar.gz.asc
Patch0:		libnids-1.18-libnet_config.diff
Patch1:		libnids-1.19-x86-pic.diff
BuildRequires:	libpcap-devel
BuildRequires:	libnet-devel
BuildRequires:	pkgconfig(glib-2.0)

%description
Libnids is an implementation of an E-component of Network Intrusion Detection
System. It emulates the IP stack of Linux 2.0.x. Libnids offers IP
defragmentation, TCP stream assembly and TCP port scan detection.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	A shared Library that provides functions of Network Intrusion Detection System
Group:		System/Libraries
Provides:	%{name} = %{EVRD}

%description -n %{libname}
Libnids is a library that provides a functionality of one of NIDS (Network
Intrusion Detection System) components, namely E-component. It means that
libnids code watches all local network traffic, cooks received datagrams a bit
(quite a bit ;)), and provides convenient information on them to analyzing
modules of NIDS.

%files -n %{libname}
%doc CHANGES README CREDITS MISC
%{_libdir}/libnids.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Libnids is a library that provides a functionality of one of NIDS (Network
Intrusion Detection System) components, namely E-component. It means that
libnids code watches all local network traffic, cooks received datagrams a bit
(quite a bit ;)), and provides convenient information on them to analyzing
modules of NIDS.

This package contains the static library and header files for %{name}.

%files -n %{devname}
%doc CHANGES README CREDITS MISC doc/*
%{_libdir}/libnids.a
%{_libdir}/libnids.so
%{_includedir}/nids.h
%{_mandir}/man3/*

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p0
%patch1 -p0

# fix soname
perl -pi -e "s|^LIBSHARED.*|LIBSHARED = libnids.so.%{major}|g" src/Makefile.in

find . -perm 0600 | xargs chmod 0644

%build
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal; autoconf

export CFLAGS="%{optflags} -fPIC"

%configure2_5x \
    --enable-shared \
    --enable-static

%make shared static

%install
%makeinstall

mv %{buildroot}%{_libdir}/libnids.so.%{major} \
    %{buildroot}%{_libdir}/libnids.so.%{major}.0

ln -snf libnids.so.%{major}.0 %{buildroot}%{_libdir}/libnids.so.%{major}
ln -snf libnids.so.%{major} %{buildroot}%{_libdir}/libnids.so

