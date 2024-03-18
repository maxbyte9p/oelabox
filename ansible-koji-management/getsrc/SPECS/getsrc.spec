Name:           getsrc
Version:        1.0.0
Release:        1%{?dist}
Summary:        Simple lookaside grabber
BuildArch:      noarch

License:        MIT
URL:            https://github.com/rocky-linux/rocky-tools/tree/main/getsrc
Source0:        %{name}-%{version}.tar.gz

Requires:       bash
Requires:       git
Requires:       curl
Requires:       rpm-build

%description
Simple lookaside grabber from rocky-tools


%prep
%setup -q


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install -m 755 %{name}.sh $RPM_BUILD_ROOT/%{_bindir}


%files
%{_bindir}/%{name}.sh



%changelog
* Mon Feb 12 2024 maxbyte9p <maxbyte9p@gmail.com>
- 
