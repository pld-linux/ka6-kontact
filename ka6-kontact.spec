#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.12.0
%define		kframever	6.14.0
%define		qtver		6.8.0
%define		kaname		kontact
Summary:	kontact
Name:		ka6-%{kaname}
Version:	25.12.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	95da72f781cd322721a87a838c7b8a15
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6WebEngine-devel
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-tools
BuildRequires:	ka6-grantleetheme-devel >= %{kdeappsver}
BuildRequires:	ka6-kontactinterface-devel >= %{kdeappsver}
BuildRequires:	ka6-libkdepim-devel >= %{kdeappsver}
BuildRequires:	ka6-pimcommon-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcmutils-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-kguiaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
ExclusiveArch:	%{x8664} aarch64
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kontact is the integrated solution to your personal information
management (PIM) needs. It combines well-known KDE applications like
KMail, KOrganizer and KAddressBook into a single interface to provide
easy access to mail, scheduling, address book and other PIM
functionality.

%description -l pl.UTF-8
Kontact jest zintegrowanym rozwiązaniem do zarządzania informacją
osobistą (PIM). W jego skład wchodzą dobrze znane aplikacje KDE, takie
jak KMail, KOrganizer i KAddressBook. Mają ujednolicony interfejs i
dają łatwy dostęp do poczty, listy zadań, książki adresowej i innych
funkcjonalności PIM.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kontact
%ghost %{_libdir}/libkontactprivate.so.6
%{_libdir}/libkontactprivate.so.*.*
%{_desktopdir}/org.kde.kontact.desktop
%{_datadir}/config.kcfg/kontact.kcfg
%{_iconsdir}/hicolor/*x*/apps/kontact.png
%{_iconsdir}/hicolor/scalable/apps/kontact.svg
%{_datadir}/messageviewer/about/default/introduction_kontact.html
%{_datadir}/messageviewer/about/default/loading_kontact.html
%{_datadir}/metainfo/org.kde.kontact.appdata.xml
%{_datadir}/dbus-1/services/org.kde.kontact.service
%{_datadir}/qlogging-categories6/kontact.categories
%{_datadir}/qlogging-categories6/kontact.renamecategories
%dir %{_libdir}/qt6/plugins/pim6/kcms/kontact
%{_libdir}/qt6/plugins/pim6/kcms/kontact/kcm_kontact.so
