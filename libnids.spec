%define major 1
%define libname %mklibname nids %{major}
%define develname %mklibname nids -d

Summary:	Library that provides functions of Network Intrusion Detection System 
Name:		libnids
Version:	1.24
Release:	%mkrel 3
License:	GPL
Group:		Networking/Other
URL:		http://libnids.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/libnids/%{name}-%{version}.tar.gz
Source1:	http://prdownloads.sourceforge.net/libnids/%{name}-%{version}.tar.gz.asc
Patch0:		libnids-1.18-libnet_config.diff
Patch1:		libnids-1.19-x86-pic.diff
BuildRequires:	libpcap-devel
BuildRequires:	net-devel >= 1.1.3
BuildRequires:	glib2-devel >= 2.2.0
BuildRequires:  automake
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description 
Libnids is an implementation of an E-component of Network Intrusion Detection
System. It emulates the IP stack of Linux 2.0.x. Libnids offers IP
defragmentation, TCP stream assembly and TCP port scan detection.

%package -n	%{libname}
Summary:	A shared Library that provides functions of Network Intrusion Detection System
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
Libnids is a library that provides a functionality of one of NIDS (Network
Intrusion Detection System) components, namely E-component. It means that
libnids code watches all local network traffic, cooks received datagrams a bit
(quite a bit ;)), and provides convenient information on them to analyzing
modules of NIDS.

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname nids 1 -d}

%description -n	%{develname}
Libnids is a library that provides a functionality of one of NIDS (Network
Intrusion Detection System) components, namely E-component. It means that
libnids code watches all local network traffic, cooks received datagrams a bit
(quite a bit ;)), and provides convenient information on them to analyzing
modules of NIDS.

This package contains the static library and header files for %{name}.

%prep

%setup -q
%patch0 -p0
%patch1 -p0

# fix soname
perl -pi -e "s|^LIBSHARED.*|LIBSHARED = libnids.so.%{major}|g" src/Makefile.in

%build
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal; autoconf

export CFLAGS="%{optflags} -fPIC"

%configure2_5x \
    --enable-shared \
    --enable-static

%make shared static

%install
rm -rf %{buildroot}

%makeinstall

mv %{buildroot}%{_libdir}/libnids.so.%{major} \
    %{buildroot}%{_libdir}/libnids.so.%{major}.0

ln -snf libnids.so.%{major}.0 %{buildroot}%{_libdir}/libnids.so.%{major}
ln -snf libnids.so.%{major} %{buildroot}%{_libdir}/libnids.so

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

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


%changelog
* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.24-3mdv2011.0
+ Revision: 627789
- don't force the usage of automake1.7

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.24-2mdv2011.0
+ Revision: 609764
- rebuild

* Thu Apr 01 2010 Oden Eriksson <oeriksson@mandriva.com> 1.24-1mdv2010.1
+ Revision: 530652
- 1.24
- drop one upstream added patch

* Thu Jun 04 2009 Oden Eriksson <oeriksson@mandriva.com> 1.23-4mdv2010.0
+ Revision: 382710
- add the actual patch
- rebuilt against libnet 1.1.3

* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 1.23-3mdv2009.1
+ Revision: 298274
- rebuilt against libpcap-1.0.0

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 1.23-2mdv2009.0
+ Revision: 267924
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed May 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.23-1mdv2009.0
+ Revision: 207107
- 1.23

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Dec 14 2007 Thierry Vignaud <tv@mandriva.org> 1.21-3mdv2008.1
+ Revision: 119873
- rebuild b/c of missing subpackage on ia32

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 1.21-2mdv2008.0
+ Revision: 83685
- new devel naming


* Fri Dec 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1.21-1mdv2007.0
+ Revision: 93753
- Import libnids

* Wed May 17 2006 Emmanuel Andry <eandry@mandriva.org> 1.21-1mdk
- 1.21
- buildrequires glib2-devel

* Fri Mar 17 2006 Oden Eriksson <oeriksson@mandriva.com> 1.20-3mdk
- rebuilt against libnet1.1.2

* Thu Nov 03 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.20-2mdk
- Fix BuildRequires
- %%mkrel

* Fri Feb 11 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.20-1mdk
- 1.20

* Wed Jan 19 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.19-1mdk
- 1.19
- fix patches, drop upstream merged ones
- fix deps

* Wed Jul 28 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.18-2mdk
- corrected the funny namenaming
- fix deps
- added P0 and P1
- added P2 (Gwenole Beauchesne)
- misc spec file fixes

* Thu Apr 08 2004 Tibor Pittich <Tibor.Pittich@mandrake.org> 1.18-1mdk
- 1.18 (fixes CAN-2003-0850)
- removed Packager tag, updated URL and description

