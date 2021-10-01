%global commit0 e341b4957c304823faca063448792358ce62b077
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

%define _legacy_common_support 1


Summary: Object oriented programming environment for real-time audio and video processing
Name: supercollider
Version: 3.12.1
Release: 1%{?dist}
License: GPLv3
Group: Applications/Multimedia
URL: https://supercollider.github.io
Source0: https://github.com/supercollider/supercollider/releases/download/Version-%{version}/SuperCollider-%{version}-Source.tar.bz2
Source1: supercollider-snapshot
#Patch: supercollider-3.11.0-use_system_link.patch

BuildRequires: cmake 
BuildRequires: gcc-c++ 
BuildRequires: autoconf 
BuildRequires: automake 
BuildRequires: libtool 
BuildRequires: pkgconfig
BuildRequires: jack-audio-connection-kit-devel 
BuildRequires: libsndfile-devel alsa-lib-devel
Buildrequires: fftw3-devel 
BuildRequires: libcurl-devel 
BuildRequires: emacs 
BuildRequires: w3m 
BuildRequires: ruby
BuildRequires: avahi-devel 
BuildRequires: libX11-devel 
BuildRequires: libXt-devel
BuildRequires: libicu-devel 
BuildRequires: readline-devel
BuildRequires: qt5-qtbase-devel 
BuildRequires: qt5-qtsensors-devel 
BuildRequires: qt5-qttools-devel
BuildRequires: qt5-qtlocation-devel 
BuildRequires: qt5-qtwebkit-devel
BuildRequires: qt5-qtwebengine-devel
BuildRequires: pkgconfig(Qt5Svg)
BuildRequires: pkgconfig(Qt5WebSockets)
BuildRequires: yaml-cpp-devel   
BuildRequires: cwiid-devel
BuildRequires: chkconfig
BuildRequires: systemd-devel
BuildRequires: libatomic
BuildRequires: boost-devel 
BuildRequires: yaml-cpp-devel 
BuildRequires: git
BuildRequires: chrpath

Requires: emacs 
Requires: w3m-el

%description
SuperCollider is an object oriented programming environment for
real-time audio and video processing. It is one of the finest and most
versatile environments for signal processing and especially for
creating music applications of all kinds, such as complete
compositions, interactive performances, installations etc.

%package devel
Summary: Development files for SuperCollider
Group: Development/Libraries
Requires: supercollider = %{version}-%{release} pkgconfig 
Requires: jack-audio-connection-kit-devel alsa-lib-devel
Requires: libsndfile-devel
Requires: avahi-devel

%description devel
This package includes include files and libraries neede to develop
SuperCollider applications

%package emacs
Summary: SuperCollider support for Emacs
Group: Applications/Multimedia
Requires: supercollider = %{version}-%{release}

%description emacs
SuperCollider support for the Emacs text editor.

%package gedit
Summary: SuperCollider support for GEdit
Group: Applications/Multimedia
Requires: supercollider = %{version}-%{release}

%description gedit
SuperCollider support for the GEdit text editor.

%package vim
Summary: SuperCollider support for Vim
Group: Applications/Multimedia
Requires: supercollider = %{version}-%{release}
Recommends: scvim

%description vim
SuperCollider support for the Vim text editor.

%prep 
%autosetup -n SuperCollider-%{version}-Source -p1

  # removing macOS hidden files (due to release tarball issues):
  # https://github.com/supercollider/supercollider/issues/4545
  find . -type f -iname "*\._*" -delete

%build
mkdir -p build
%cmake -B build -DCMAKE_BUILD_TYPE=Release  

#        -DSC_VIM=OFF

%make_build -C build V=0

%install
%make_install -C build V=0

# Remove rpath.
chrpath --delete $RPM_BUILD_ROOT/%{_bindir}/scide
chrpath --delete $RPM_BUILD_ROOT/%{_bindir}/sclang

# Remove Zero length files
find %{buildroot} -size 0 -delete

find . -name '*.py' -exec sed -i -r 's|/usr/bin/python$|&2|g' {} +

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README*
%{_bindir}/sclang
# in doc
%exclude %{_datadir}/SuperCollider/AUTHORS
%exclude %{_datadir}/SuperCollider/COPYING
%exclude %{_datadir}/SuperCollider/README.md
%exclude %{_datadir}/SuperCollider/README_LINUX.md
%exclude %{_datadir}/SuperCollider/CHANGELOG.md
%{_datadir}/SuperCollider/HelpSource
%{_datadir}/SuperCollider/SCClassLibrary
%{_datadir}/SuperCollider/sounds
%{_datadir}/SuperCollider/translations
# scsynth
%{_bindir}/scsynth
%{_libdir}/SuperCollider/plugins
%ifnarch %{arm}
# supernova
%{_bindir}/supernova
%endif
# examples
%{_datadir}/SuperCollider/examples
%exclude %{_datadir}/doc/SuperCollider/
%{_datadir}/SuperCollider/HID_Support
# ide
%{_bindir}/scide
%{_datadir}/applications/SuperColliderIDE.desktop
%{_datadir}/icons/hicolor/*/apps/supercollider.xpm
 %{_datadir}/icons/hicolor/*/apps/supercollider.png
%{_datadir}/icons/hicolor/scalable/apps/sc_ide.svg

%files devel
%defattr(-,root,root,-)
%{_includedir}/SuperCollider

%files emacs
%defattr(-,root,root,-)
%{_datadir}/emacs/site-lisp/SuperCollider
%{_datadir}/SuperCollider/Extensions/scide_scel

%files vim
%defattr(-,root,root,-)
/usr/share/SuperCollider/Extensions/scide_scvim/SCVim.sc

%files gedit
%defattr(-,root,root,-)
%{_libdir}/gedit*/plugins/*
%{_datadir}/gtksourceview*/language-specs/supercollider.lang
%{_datadir}/mime/packages/supercollider.xml

%changelog

* Thu Sep 16 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.12.1-1
- Updated to 3.12.1

* Thu Jun 03 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.11.2-1
- Updated to 3.11.2

* Thu Sep 24 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.11.1-1
- Updated to 3.11.1

* Sun Mar 15 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.11.0-1
- Updated to 3.11.0

* Sun Jan 19 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.10.4-1
- Updated to 3.10.4-1

* Tue Sep 03 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.10.3-1
- Updated to 3.10.3-1

* Sun Feb 17 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.10.2-1.git834c036
- Updated to 3.10.2-1.git834c036

* Thu Jan 24 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.10.1-1.git8597bef
- Updated to 3.10.1-1.git8597bef  

* Sat Dec 01 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.10.0-1.gita3b8ac7  
- Updated to 3.10.0-1.gita3b8ac7 

* Thu May 17 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.9.3-1.gitabe2491  
- Upstream 
- Cleaned and Updated to 3.9.3

* Wed Oct 25 2017 Yann Collette <ycollette.nospam@free.fr> 3.8.0-1
- update to 3.8.0
