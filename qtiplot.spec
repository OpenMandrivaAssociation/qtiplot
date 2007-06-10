%define prel rc2
%define	qtdir	%{_libdir}/qt3

Summary:	Data analysis and scientific plotting
Name:		qtiplot
Version:	0.9
Release:	%mkrel 0.%{prel}.1
License:	GPL
Group:		Sciences/Other
Url:		http://soft.proindependent.com/qtiplot.html
Source0:	http://soft.proindependent.com/src/%{name}-%{version}%{prel}.tar.bz2
# Automatically added by buildreq on Fri Dec 03 2004
BuildRequires:	qt3-devel libqwt-devel libqwtplot3d-devel gsl-devel icoutils
BuildRequires:	ImageMagick
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Data analysis and scientific plotting.
Free clone of Origin.

%prep
%setup -q -n %{name}-%{version}%{prel}
#sed -i -e 's|INCLUDEPATH.*qwt/include|INCLUDEPATH += %{qtdir}/include/qwt|g' %{name}/%{name}.pro
sed -i -e 's|INCLUDEPATH.*/include/qwtplot3d|INCLUDEPATH += %{qtdir}/include/qwtplot3d|g' %{name}/%{name}.pro
sed -i -e 's|INCLUDEPATH.*D:.*|INCLUDEPATH += %{_includedir}|g' %{name}/%{name}.pro
sed -i -e 's|helpFilePath=.*$|helpFilePath="%{_datadir}/doc/%{name}-%{version}/help.html";|g' %{name}/src/ApplicationWindow.cpp
sed -i -e 's|sub-3rdparty-qwt ||g' %{name}/%{name}.pro

%build
#cd %{name}
export QTDIR=%{qtdir}
export PATH=$QTDIR/bin:$PATH
qmake %{name}.pro -o Makefile
%make

%install
rm -rf %{buildroot}
install -m755 qtiplot/qtiplot -D %{buildroot}%{_bindir}/qtiplot

#desktop-file-install --vendor="" \
#  --remove-category="Application" \
#  --add-category="Qt" \
#  --add-category="More Applications/Sciences/Data Visualization" \
#  --add-category="X-MandrivaLinux-MoreApplications-Sciences-DataVisualization" \
#  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/qtiplot.desktop


mkdir -p %{buildroot}{%{_liconsdir},%{_iconsdir},%{_miconsdir}}
icotool -x -i1 %{name}/src/qtiplot.ico -o qtiplot32.png
convert -scale 48 qtiplot32.png %{buildroot}%{_liconsdir}/%{name}.png
install -m 644 qtiplot32.png %{buildroot}%{_iconsdir}/%{name}.png
convert -scale 16 qtiplot32.png %{buildroot}%{_miconsdir}/%{name}.png

%clean
rm -rf %{buildroot}

%post
%update_menus

%postun
%clean_menus

%files
%defattr(644,root,root,755)
%doc README.html gpl_licence.txt
%attr(755,root,root) %{_bindir}/qtiplot
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
