Summary:	Data analysis and scientific plotting
Name:		qtiplot
Version:	0.9.8.1
Release:	%mkrel 1
License:	GPLv2+
Group:		Sciences/Other
Url:		http://soft.proindependent.com/qtiplot.html
Source0:	http://download.berlios.de/qtiplot/%{name}-%{version}.tar.bz2
Patch0:		qtiplot-0.9.7.12-build.conf.patch
Patch1:		qtiplot-0.9.7.11-fix-str-fmt.patch
Patch2:		qtiplot-0.9.8.1-gcc45.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%py_requires -d
BuildRequires:	qt4-devel >= 4.4.0
BuildRequires:	qt-assistant-adp-devel
#BuildRequires:	libqwtplot3d-devel
BuildRequires:	gsl-devel
BuildRequires:	icoutils
BuildRequires:	muparser-devel >= 1.32
BuildRequires:	boost-devel >= 1.36.0
#BuildRequires:	libqwt-devel >= 5.2.0
BuildRequires:	python-qt4 >= 4.4.4
BuildRequires:	imagemagick
BuildRequires:	docbook-utils
BuildRequires:	docbook-dtd44-xml
Requires:	qt-assistant-adp
Requires:	python-qt4 >= 4.4.4

%description
Data analysis and scientific plotting.
Free clone of Origin.

%prep
%setup -q
%patch0 -p1 -b .compile
%patch1 -p0 -b .str
%patch2 -p0 -b .gcc

%build
%qmake_qt4 \
	%if "%{_lib}" != "lib"
		libsuff=64 \
	%endif
	-o Makefile
%make

%install
rm -rf %{buildroot}
make install INSTALL_ROOT=%{buildroot}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=qtiplot
Comment=Data analysis and scientific plotting
Exec=qtiplot
Icon=qtiplot
Terminal=false
Type=Application
Categories=Qt;Science;DataVisualization;
StartupNotify=true
EOF

mkdir -p %{buildroot}{%{_liconsdir},%{_iconsdir},%{_miconsdir}}
convert -scale 48 qtiplot_logo.png %{buildroot}%{_liconsdir}/%{name}.png
convert -scale 32 qtiplot_logo.png %{buildroot}%{_iconsdir}/%{name}.png
convert -scale 16 qtiplot_logo.png %{buildroot}%{_miconsdir}/%{name}.png

mkdir -p %{buildroot}%{_iconsdir}/hicolor/16x16/apps/
convert -geometry 16x16 qtiplot_logo.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
mkdir -p %{buildroot}%{_iconsdir}/hicolor/32x32/apps/
convert -geometry 32x32 qtiplot_logo.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
mkdir -p %{buildroot}%{_iconsdir}/hicolor/48x48/apps/
convert -geometry 48x48 qtiplot_logo.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

rm -fr %buildroot/usr/local

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%endif

%files
%defattr(644,root,root,755)
%doc README.html gpl_licence.txt
%attr(755,root,root) %{_bindir}/qtiplot
%{_mandir}/man1/qtiplot.1.*
%{_libdir}/qtiplot/plugins
%{_datadir}/qtiplot
%{_datadir}/applications/*.desktop
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/*/apps/*.png
