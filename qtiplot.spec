Summary:	Data analysis and scientific plotting
Name:		qtiplot
Version:	0.9.8.9
Release:	3
License:	GPLv2+
Group:		Sciences/Other
Url:		http://soft.proindependent.com/qtiplot.html
Source0:	http://download.berlios.de/qtiplot/%{name}-%{version}.tar.bz2
Source1:	http://www.stat.tamu.edu/~aredd/tamuanova/tamu_anova-0.2.tar.gz
Source2:	build.conf
Patch0:		qtiplot-0.9.8.9-rosa-pro.patch
Patch1:		qtiplot-0.9.7.11-fix-str-fmt.patch
Patch2:		qtiplot-0.9.8.9-debian-fix_paths.patch
Patch3:		qtiplot-0.9.8.9-debian-crasher_without_internet.patch
Patch4:		qtiplot-0.9.8.9-debian-glu_include.patch
Patch5:		qtiplot-0.9.8.9-rosa-gl2ps_zlib_png.patch
Patch6:		qtiplot-0.9.8.9-linkage.patch
Patch7:		qtiplot-0.9.8.9-sip-4.15.patch
Patch8:		qtiplot-0.9.8.9-sip-4.15-2.patch
BuildRequires:	docbook-dtd44-xml
BuildRequires:	docbook-utils
BuildRequires:	icoutils
BuildRequires:	imagemagick
BuildRequires:	python2-qt4
BuildRequires:	python2-sip
BuildRequires:	qt4-devel
BuildRequires:	qtexengine-devel
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gsl)
BuildRequires:	pkgconfig(muparser)
BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(QtAssistantClient)
Requires:	qt-assistant-adp
Requires:	python2-qt4

%description
Data analysis and scientific plotting. Free clone of Origin.

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

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1 -b .compile
%patch1 -p0 -b .str
%patch2 -p1 -b .path
%patch3 -p1 -b .inet
%patch4 -p1 -b .glu
%patch5 -p1 -b .zlib_png
%patch6 -p1 -b .linkage
%patch7 -p1 -b .sip415
%patch8 -p1 -b .sip415-2
pushd 3rdparty
tar xf %{SOURCE1}
mv tamu_anova-0.2 tamu_anova
popd

cp %{SOURCE2} .
sed -i 's|@LIBDIR@|%{_libdir}|g;s|@INCLUDEDIR@|%{_includedir}|g' build.conf

# use py2
sed -i -e "s,/usr/bin/python,%{__python2},g" qtiplot/*.py

%build
pushd 3rdparty/tamu_anova
export PYTHON=%{__python2}
%configure --disable-shared --enable-static
%make
popd
%qmake_qt4 -d \
	%if "%{_lib}" != "lib"
		libsuff=64 \
	%endif
	-o Makefile
%make

%install
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

rm -fr %{buildroot}/usr/local

# Nuke the junk
find %{buildroot} -name libqwtplot3d.a -delete
