%define major 1
%define libname %mklibname nids %{major}
%define develname %mklibname nids -d

Summary:	Library that provides function of Network Intrusion Detection System 
Name:		libnids
Version:	1.21
Release:	%mkrel 3
License:	GPL        
Group:		Networking/Other		
URL:		http://libnids.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/libnids/%{name}-%{version}.tar.bz2
Patch0:		libnids-1.18-libnet_config.diff
Patch1:		libnids-1.19-x86-pic.diff
BuildRequires:	libpcap-devel
BuildRequires:	libnet1.1.2-devel
BuildRequires:	glib2-devel >= 2.2.0
BuildRequires:  automake1.7

%description 
Libnids is an implementation of an E-component of Network
Intrusion Detection System. It emulates the IP stack of Linux
2.0.x. Libnids offers IP defragmentation, TCP stream assembly and
TCP port scan detection.

%package -n	%{libname}
Summary:	Libraries needed by %name
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
Libnids is a library that provides a functionality of one of NIDS
(Network Intrusion Detection System) components, namely
E-component. It means that libnids code watches all local network
traffic, cooks received datagrams a bit (quite a bit ;)), and
provides convenient information on them to analyzing modules of
NIDS.

%package -n	%{develname}
Summary:	Library that provides function of Network Intrusion Detection System
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname nids 1 -d}

%description -n	%{develname}
Libnids is a library that provides a functionality of one of NIDS
(Network Intrusion Detection System) components, namely
E-component. It means that libnids code watches all local network
traffic, cooks received datagrams a bit (quite a bit ;)), and
provides convenient information on them to analyzing modules of
NIDS.

%prep

%setup -q
%patch0 -p0
%patch1 -p0

# fix soname
perl -pi -e "s|^LIBSHARED.*|LIBSHARED = libnids.so.%{major}|g" src/Makefile.in

%build
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal-1.7; autoconf

export CFLAGS="%{optflags} -fPIC"

%configure2_5x \
    --enable-shared \
    --enable-static

%make shared static

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall

mv %{buildroot}%{_libdir}/libnids.so.%{major} \
    %{buildroot}%{_libdir}/libnids.so.%{major}.0

ln -snf libnids.so.%{major}.0 %{buildroot}%{_libdir}/libnids.so.%{major}
ln -snf libnids.so.%{major} %{buildroot}%{_libdir}/libnids.so

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(0644,root,root,0755)
%doc CHANGES README CREDITS MISC
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{develname}
%defattr(0644,root,root,0755)
%doc CHANGES README CREDITS MISC doc/*
%defattr(-,root,root)
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_includedir}/nids.h
%{_mandir}/man3/*
