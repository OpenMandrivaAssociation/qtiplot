Summary:	Data analysis and scientific plotting
Name:		qtiplot
Version:	0.9.7.5
Release:	%mkrel 1
License:	GPLv2+
Group:		Sciences/Other
Url:		http://soft.proindependent.com/qtiplot.html
Source0:	http://soft.proindependent.com/src/%{name}-%{version}.tar.bz2
Patch0:		qtiplot-0.9.7.5-compile-options.patch
Patch2:		qtiplot-0.9.7.4-fix-str-fmt.patch
# Automatically added by buildreq on Fri Dec 03 2004
BuildRequires:	qt4-devel libqwtplot3d-devel gsl-devel icoutils
BuildRequires:	python-qt4 muparser-devel
BuildRequires:	boost-devel
BuildRequires:	libqwt-devel >= 5.1.0
BuildRequires:	imagemagick docbook-utils docbook-dtd44-xml
%py_requires -d
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Data analysis and scientific plotting.
Free clone of Origin.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .compile
%patch2 -p0 -b .str

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

install -D -m755 qtiplot/qtiplot %buildroot%_bindir/qtiplot
install -D -m644 qtiplot.1 %buildroot%{_mandir}/man1/qtiplot.1

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
%{_datadir}/applications/*.desktop
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/*/apps/*.png
