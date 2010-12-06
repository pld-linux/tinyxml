%define		file_version	%(echo %{version} | tr . _)
Summary:	A simple, small, C++ XML parser
Summary(pl.UTF-8):	Prosty, mały, napisany w C++ parser XML
Name:		tinyxml
Version:	2.6.1
Release:	1
License:	zlib
Group:		Libraries
Source0:	http://downloads.sourceforge.net/tinyxml/%{name}_%{file_version}.zip
# Source0-md5:	60f92af4f43364ab0c6d5b655e804bd3
Patch0:		%{name}-flags.patch
URL:		http://www.grinninglizard.com/tinyxml/
BuildRequires:	unzip
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
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for tinyxml library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki tinyxml.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%{__make} \
	CXX="%{__cxx}" \
	LD="%{__cxx}" \
	OPTFLAGS="%{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags}"


# Not really designed to be build as lib
for i in tinyxml.cpp tinystr.cpp tinyxmlerror.cpp tinyxmlparser.cpp; do
	%{__cxx} %{rpmcxxflags} -fPIC -o $i.o -c $i
done
%{__cxx} %{rpmcxxflags} %{rpmldflags} -shared -o lib%{name}.so.0.%{version} *.cpp.o

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

cp -a xmltest $RPM_BUILD_ROOT%{_bindir}
cp -a libtinyxml.so.0.%{version} $RPM_BUILD_ROOT%{_libdir}
cp -a tiny*.h $RPM_BUILD_ROOT%{_includedir}
ln -s libtinyxml.so.0.%{version} $RPM_BUILD_ROOT%{_libdir}/libtinyxml.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc changes.txt readme.txt
%attr(755,root,root) %{_bindir}/xmltest
%attr(755,root,root) %{_libdir}/libtinyxml.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtinyxml.so
%{_includedir}/*
