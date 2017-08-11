%global release_name Penguin
%global dist_version 26

Summary:        Dapper Linux release files
Name:           dapper-release
Version:        26
Release:        1
License:        MIT
Group:	        System Environment/Base
Source0:        %{name}-%{version}.tar.xz
Obsoletes:      redhat-release
Provides:       redhat-release
Provides:       system-release
Provides:       system-release(%{version})
# Comment this next Requires out if we're building for a non-rawhide target
# Requires:       fedora-repos-rawhide
Requires:       dapper-repos(%{version})
Obsoletes:      generic-release-rawhide
Obsoletes:      generic-release-cloud
Obsoletes:      generic-release-server
Obsoletes:      generic-release-workstation
BuildArch:      noarch
Obsoletes:      fedora-release
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release(%{version})

%description
Dapper Linux release files such as dnf configs and various /etc/ files that
define the release. 

%package notes
Summary:	Release Notes
License:	Open Publication
Group:		System Environment/Base
Provides:	system-release-notes = %{version}-%{release}
Conflicts:	fedora-release-notes

%description notes
Dapper Linux release notes package.


%package workstation
Summary:        Base package for Dapper Linux Workstation-specific default configurations
Provides:       system-release-workstation
Provides:       system-release-workstation(%{version})
Provides:       system-release-product
Requires:       dapper-release
# needed for captive portal support
Requires:       NetworkManager-config-connectivity-fedora
# Replace fedora's packages
Provides:       fedora-release-workstation
Obsoletes:      fedora-release-workstation


%description workstation
Provides a base package for Dapper Linux Workstation-specific configuration files to
depend on.

%package server
Summary:        Base package for Dapper Linux Server-specific default configurations
Provides:       system-release-server
Provides:       system-release-server(%{version})
Provides:       system-release-product
Requires:       dapper-release
Requires:       systemd
Requires:       cockpit-bridge
Requires:       cockpit-networkmanager
Requires:       cockpit-shell
Requires:       cockpit-storaged
Requires:       cockpit-ws
Requires:       openssh-server
Requires:       rolekit
Requires(post):	systemd

%description server
Provides a base package for Dapper Linux Server-specific configuration files to
depend on.

%prep
%setup -q

%build

%install
install -d %{buildroot}/etc
echo "Dapper Linux release %{version} (%{release_name})" > %{buildroot}/etc/fedora-release
echo "cpe:/o:dapperlinux:dapperlinux:%{version}" > %{buildroot}/etc/system-release-cpe
ln -s fedora-release %{buildroot}/etc/redhat-release
ln -s fedora-release %{buildroot}/etc/system-release

mkdir -p %{buildroot}/usr/lib/systemd/system-preset/

cat << EOF >>%{buildroot}/usr/lib/os-release
NAME="Dapper Linux"
VERSION="%{version} (%{release_name})"
ID=dapper
ID_LIKE=fedora
VERSION_ID=%{version}
PRETTY_NAME="Dapper Linux %{version} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:dapperlinux:dapperlinux:%{version}"
HOME_URL="https://dapperlinux.com"
EOF
# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}/etc/os-release

install -d $RPM_BUILD_ROOT/usr/lib/os.release.d/
cat << EOF >>$RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-fedora
NAME="Dapper Linux"
VERSION="%{version} (%{release_name})"
ID=dapper
ID_LIKE=fedora
VERSION_ID=%{version}
PRETTY_NAME="Dapper Linux %{version} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:dapperlinux:dapperlinux:%{version}"
HOME_URL="https://dapperlinux.com"
EOF

# Create the common /etc/issue
echo "\S" > $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-fedora
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-fedora
echo >> $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-fedora

# Create /etc/issue.net
echo "\S" > $RPM_BUILD_ROOT/usr/lib/issue.net
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/usr/lib/issue.net
ln -s ../usr/lib/issue.net $RPM_BUILD_ROOT/etc/issue.net

# Workstation
cp -p $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-fedora \
      $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-workstation
echo "VARIANT=\"Workstation Edition\"" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-workstation
echo "VARIANT_ID=workstation" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-workstation
sed -i -e "s|(%{release_name})|(Workstation Edition)|g" $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-workstation

# Server
cp -p $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-fedora \
      $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-server
echo "VARIANT=\"Server Edition\"" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-server
echo "VARIANT_ID=server" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-server
sed -i -e "s|(%{release_name})|(Server Edition)|g" $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-server

cp -p $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-fedora \
      $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-server
echo "Admin Console: https://\4:9090/ or https://[\6]:9090/" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-server
echo >> $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-server

# Create the symlink for /etc/issue
# We don't create the /usr/lib/os-release symlink until %%post
# so that we can ensure that the right one is referenced.
ln -s ../usr/lib/issue $RPM_BUILD_ROOT/etc/issue

# Set up the dist tag macros
install -d -m 755 %{buildroot}%{_rpmconfigdir}/macros.d
cat >> %{buildroot}%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%fedora		%{dist_version}
%%dist		.fc%{dist_version}
%%fc%{dist_version}		1
EOF

# Add presets
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/user-preset/
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
mkdir -p $RPM_BUILD_ROOT/usr/lib/os.release.d/presets


# Default system wide
install -m 0644 85-display-manager.preset $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -m 0644 90-default.preset $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -m 0644 99-default-disable.preset $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
# Fedora Server
install -m 0644 80-server.preset $RPM_BUILD_ROOT%{_prefix}/lib/os.release.d/presets/
install -m 0644 80-server.preset $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
# Fedora Workstation
install -m 0644 80-workstation.preset $RPM_BUILD_ROOT%{_prefix}/lib/os.release.d/presets/
install -m 0644 80-workstation.preset $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%license LICENSE README.license
%dir /usr/lib/os.release.d
%dir /usr/lib/os.release.d/presets
%config %attr(0644,root,root) /usr/lib/os.release.d/os-release-fedora
%config %attr(0644,root,root) /usr/lib/os-release
/etc/os-release
%config %attr(0644,root,root) /etc/fedora-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%config %attr(0644,root,root) /usr/lib/os.release.d/issue-fedora
%config(noreplace) /etc/issue
%config %attr(0644,root,root) /usr/lib/issue.net
%config(noreplace) /etc/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir /usr/lib/systemd/user-preset/
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset

%files workstation
%config %attr(0644,root,root) /usr/lib/os.release.d/os-release-workstation
%{_prefix}/lib/systemd/system-preset/80-workstation.preset
%config %attr(0644,root,root) /usr/lib/os.release.d/presets/80-workstation.preset

%files server
%config %attr(0644,root,root) /usr/lib/os.release.d/os-release-server
%config %attr(0644,root,root) /usr/lib/os.release.d/issue-server
%{_prefix}/lib/systemd/system-preset/80-server.preset
%config %attr(0644,root,root) /usr/lib/os.release.d/presets/80-server.preset

%files notes
%defattr(-,root,root,-)
%doc README.Dapper-Release-Notes

%changelog
* Fri Aug 11 2017 Matthew Ruffell <msr50@uclive.ac.nz> - 26-1
- Dapper Linux 26

* Sat Nov 26 2016 Matthew Ruffell <msr50@uclive.ac.nz> - 25-3
- Fixing small version problems

* Sat Nov 26 2016 Matthew Ruffell <msr50@uclive.ac.nz> - 25-2
- Adding new workstation package

* Fri Nov  4 2016 Matthew Ruffell <msr50@uclive.ac.nz> - 25-1
- Dapper Linux Release 25

* Fri Oct  7 2016 Matthew Ruffell <msr50@uclive.ac.nz> - 24-2
- Dapper Linux Release 24

* Wed Jun 22 2016 Bruno Wolff III <bruno@wolff.to> - 24-1
- Change to a release version to avoid pre-release builds - bug 1282159

* Sat Mar 05 2016 Bruno Wolff III <bruno@wolff.to> - 24-0.5
- f24 isn't rawhide any more

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 24-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Tom Callaway <spot@fedoraproject.org> - 24-0.3
- spec file cleanups

* Sat Aug 22 2015 Bruno Wolff III <bruno@wolff.to> - 24-0.2
- Fix typo in obsoletes

* Wed Jul 15 2015 Bruno Wolff III <bruno@wolff.to> - 24-0.1
- Rawhide is now f24

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 23-0.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Dennis Gilmore <dennis@ausil.us> - 23-0.5
- add system preset files
- drop product sub-packages

* Sat Feb 14 2015 Bruno Wolff III <bruno@wolff.to> - 23-0.4
- Fix up change log

* Sat Feb 14 2015 Bruno Wolff III <bruno@wolff.to> - 23-0.3
- Rawhide is now 23

* Tue Oct 21 2014 Tom Callaway <spot@fedoraproject.org> - 22-0.3
- add versioned provide for system-release(VERSION)

* Tue Oct 21 2014 Tom Callaway <spot@fedoraproject.org> - 22-0.2
- add productization (it is the foooooture)

* Thu Aug 07 2014 Dennis Gilmore <dennis@ausil.us> - 22-0.1
- Require fedora-repos and no longer ship repo files

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Tom Callaway <spot@fedoraproject.org> - 21-4
- license changes and clarification doc

* Sun Mar 09 2014 Bruno Wolff III <bruno@wolff.to> - 21-3
- Install dist macro into the correct directory

* Sun Jan 05 2014 Bruno Wolff III <bruno@wolff.to> - 21-2
- Work around incorrect prefix in the upstream tarball

* Sun Jan 05 2014 Bruno Wolff III <bruno@wolff.to> - 21-1
- Bump version to match current rawhide

* Sat Dec 21 2013 Bruno Wolff III <bruno@wolff.to> - 21-0.3
- Update version to 21 (which should have happened when f20 was branched)
- Changed to work with recent yum change (bug 1040607)

* Mon Dec  9 2013 Tom Callaway <spot@fedoraproject.org> - 20-1
- final release (disable rawhide dep)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 26 2013 Tom Callaway <spot@fedoraproject.org> - 20-0.1
- sync

* Wed Jun 26 2013 Tom Callaway <spot@fedoraproject.org> - 19-2
- sync to release

* Mon Mar 11 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 19-0.3
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 19-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012 Tom Callaway <spot@fedoraproject.org> - 19-0.1
- sync to 19-0.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 18-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2012 Tom Callaway <spot@fedoraproject.org> - 18-0.2
- sync with fedora-release model

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 28 2011 Tom Callaway <spot@fedoraproject.org> - 17-0.2
- initial 17

* Fri Jul 22 2011 Tom Callaway <spot@fedoraproject.org> - 16-0.2
- require -rawhide subpackage if we're built for rawhide

* Fri May 13 2011 Tom Callaway <spot@fedoraproject.org> - 16-0.1
- initial 16

* Fri May 13 2011 Tom Callaway <spot@fedoraproject.org> - 15-1
- sync to f15 final

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 15-0.3
- sync to rawhide

* Wed Feb 24 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 14-0.2
- fix broken requires

* Wed Feb 17 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 14-0.1
- update to sync with fedora-release

* Mon Nov 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 12-1
- Update for F12 final

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 11.90-1
- Build for F12 collection

* Wed May 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 11-1
- resync with fedora-release package

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> 10.90-2
- drop Requires: system-release-notes

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 10.90-1
- 10.90

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 10-1
- Bump to 10, update repos

* Mon Sep 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 9.91-2
- add Conflicts
- further sanitize descriptions

* Mon Sep 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 9.91-1
- initial package for generic-release and generic-release-notes
