%global commit0 abe24916e35e83b1d9d1cda39bf068a534434da9
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Summary: Object oriented programming environment for real-time audio and video processing
Name: supercollider
Version: 3.9.3
Release: 1%{?gver}%{?dist}
License: GPLv3
Group: Applications/Multimedia
URL: https://supercollider.github.io
Source0: https://github.com/supercollider/supercollider/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1: supercollider-snapshot

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
BuildRequires: yaml-cpp03-devel 
BuildRequires: cwiid-devel
BuildRequires: chkconfig
BuildRequires: systemd-devel
BuildRequires: libatomic
BuildRequires: boost-devel 
BuildRequires: yaml-cpp-devel 
BuildRequires: git
BuildRequires:  chrpath

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
%{S:1} -c %{commit0}
%setup -T -D -n %{name}-%{shortcommit0} 

%build

find . -name '*.py' -exec sed -i -r 's|/usr/bin/python$|&2|g' {} +

# https://fedoraproject.org/wiki/Changes/Avoid_usr_bin_python_in_RPM_Build#Quick_Opt-Out
export PYTHON_DISALLOW_AMBIGUOUS_VERSION=0

%cmake  -DSSE=ON \
	-DSSE2=ON \
        -DSUPERNOVA=ON \
        -DSYSTEM_BOOST=ON .

%make_build V=0

%install
%make_install V=0

# Remove rpath.
chrpath --delete $RPM_BUILD_ROOT/%{_bindir}/scide
chrpath --delete $RPM_BUILD_ROOT/%{_bindir}/sclang

# Remove Zero length files
find %{buildroot} -size 0 -delete

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
%{_datadir}/pixmaps/supercollider*
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
%{_datadir}/pixmaps/sc_ide.svg

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

* Thu May 17 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 3.9.3.gitabe2491-1  
- Upstream 
- Cleaned and Updated to 3.9.3

* Wed Oct 25 2017 Yann Collette <ycollette.nospam@free.fr> 3.8.0-1
- update to 3.8.0
