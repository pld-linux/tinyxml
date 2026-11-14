%define		file_version	%(echo %{version} | tr . _)
Summary:	A simple, small, C++ XML parser
Summary(pl.UTF-8):	Prosty, mały, napisany w C++ parser XML
Name:		tinyxml
Version:	2.6.2
Release:	10
License:	Zlib
Group:		Libraries
Source0:	https://downloads.sourceforge.net/tinyxml/%{name}_%{file_version}.tar.gz
# Source0-md5:	c1b864c96804a10526540c664ade67f0
Source1:	%{name}.pc.in
Patch0:		%{name}-flags.patch
Patch1:		enforce-use-stl.patch
# dead
#URL:		http://www.grinninglizard.com/tinyxml/
URL:		https://sourceforge.net/projects/tinyxml/
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TinyXML is a simple, small, C++ XML parser that can be easily
integrating into other programs.

%description -l pl.UTF-8
TinyXML to prosty, mały, napisany w C++ parser XML, który może być w
łatwy sposób integrowany z innymi programami.

%package devel
Summary:	Header files for tinyxml library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki tinyxml
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libstdc++-devel%{?_isa}

%description devel
Header files for tinyxml library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki tinyxml.

%package static
Summary:	Static tinyxml library
Summary(pl.UTF-8):	Statyczna biblioteka tinyxml
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static tinyxml library.

%description static -l pl.UTF-8
Statyczna biblioteka tinyxml.

%prep
%setup -q -n %{name}
%patch -P0 -p1
%patch -P1 -p1

%build
%{__make} \
	CXX="%{__cxx}" \
	LD="%{__cxx}" \
	OPTFLAGS="%{rpmcppflags} %{rpmcxxflags} -DTIXML_USE_STL" \
	LDFLAGS="%{rpmldflags}"

# Not really designed to be built as lib
for i in tinyxml.cpp tinystr.cpp tinyxmlerror.cpp tinyxmlparser.cpp; do
	libtool --tag=CXX --mode=compile \
		%{__cxx} %{rpmcppflags} %{rpmcxxflags} -DTIXML_USE_STL -o $i.lo -c $i
done
libtool --tag=CXX --mode=link \
	%{__cxx} %{rpmcxxflags} %{rpmldflags} \
	-rpath %{_libdir} -version-info 0:0:0 \
	-o libtinyxml.la *.cpp.lo

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

cp -a xmltest $RPM_BUILD_ROOT%{_bindir}
cp -a tiny*.h $RPM_BUILD_ROOT%{_includedir}
libtool --mode=install %{__install} libtinyxml.la $RPM_BUILD_ROOT%{_libdir}

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
sed -e 's![@]prefix[@]!%{_prefix}!g' \
	-e 's![@]exec_prefix[@]!%{_exec_prefix}!g' \
	-e 's![@]libdir[@]!%{_libdir}!g' \
	-e 's![@]includedir[@]!%{_includedir}!g' \
	-e 's![@]version[@]!%{version}!g' \
	%{SOURCE1} > $RPM_BUILD_ROOT%{_pkgconfigdir}/%{name}.pc

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtinyxml.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc changes.txt readme.txt
%attr(755,root,root) %{_bindir}/xmltest
%{_libdir}/libtinyxml.so.*.*.*
%ghost %{_libdir}/libtinyxml.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtinyxml.so
%{_includedir}/tinystr.h
%{_includedir}/tinyxml.h
%{_pkgconfigdir}/tinyxml.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtinyxml.a
