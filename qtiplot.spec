Summary:	Data analysis and scientific plotting
Name:		qtiplot
Version:	0.9.1
Release:	%mkrel 1
License:	GPLv2+
Group:		Sciences/Other
Url:		http://soft.proindependent.com/qtiplot.html
Source0:	http://soft.proindependent.com/src/%{name}-%{version}.tar.bz2
Patch0:		qtiplot-0.9.1-compile-options.patch
# Automatically added by buildreq on Fri Dec 03 2004
BuildRequires:	qt4-devel libqwt-devel libqwtplot3d-devel gsl-devel icoutils
BuildRequires:	python-qt4 muparser-devel
BuildRequires:	ImageMagick
%py_requires -d
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Data analysis and scientific plotting.
Free clone of Origin.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
%{qt4dir}/bin/qmake %{name}.pro \
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

%clean
rm -rf %{buildroot}

%post
%update_menus
%update_icon_cache hicolor

%postun
%clean_menus
%clean_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc README.html gpl_licence.txt
%attr(755,root,root) %{_bindir}/qtiplot
%{_libdir}/qtiplot/plugins
%{_datadir}/applications/*.desktop
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/*/apps/*.png
