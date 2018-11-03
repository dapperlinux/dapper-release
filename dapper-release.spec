%global release_name Pelican

Summary:        Dapper Linux release files
Name:           dapper-release
Version:        29
Release:        1
License:        MIT
URL:		https://github.com/dapperlinux/dapper-release

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
Requires(post):	systemd
# Replace Fedora's packages
Provides:		fedora-release-server
Obsoletes:		fedora-release-server

%description server
Provides a base package for Dapper Linux Server-specific configuration files to
depend on.

%package silverblue
Summary:        Base package for Dapper Linux Silverblue-specific default configurations
Provides:       system-release-silverblue
Provides:       system-release-silverblue(%{version})
Requires:       dapper-release = %{version}-%{release}
 
%description silverblue
Provides a base package for Dapper Linux Silverblue-specific configuration files to
depend on as well as Silverblue system defaults.

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
PLATFORM_ID="platform:f%{version}"
PRETTY_NAME="Dapper Linux %{version} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:dapperlinux:dapperlinux:%{version}"
HOME_URL="https://dapperlinux.com"
EOF
# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}/etc/os-release

install -d %{buildroot}/usr/lib/os.release.d/
cat << EOF >>%{buildroot}/usr/lib/os.release.d/os-release-fedora
NAME="Dapper Linux"
VERSION="%{version} (%{release_name})"
ID=dapper
ID_LIKE=fedora
VERSION_ID=%{version}
PLATFORM_ID="platform:f%{version}"
PRETTY_NAME="Dapper Linux %{version} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:dapperlinux:dapperlinux:%{version}"
HOME_URL="https://dapperlinux.com"
EOF

# Create the common /etc/issue
echo "\S" > %{buildroot}/usr/lib/issue
echo "Kernel \r on an \m (\l)" >> %{buildroot}/usr/lib/issue
echo >> %{buildroot}/usr/lib/issue
ln -s ../usr/lib/issue %{buildroot}/etc/issue

# Create /etc/issue.net
echo "\S" > %{buildroot}/usr/lib/issue.net
echo "Kernel \r on an \m (\l)" >> %{buildroot}/usr/lib/issue.net
ln -s ../usr/lib/issue.net %{buildroot}/etc/issue.net

# Workstation
cp -p %{buildroot}/usr/lib/os.release.d/os-release-fedora \
      %{buildroot}/usr/lib/os.release.d/os-release-workstation
echo "VARIANT=\"Workstation Edition\"" >> %{buildroot}/usr/lib/os.release.d/os-release-workstation
echo "VARIANT_ID=workstation" >> %{buildroot}/usr/lib/os.release.d/os-release-workstation
sed -i -e "s|(%{release_name})|(Workstation Edition)|g" %{buildroot}/usr/lib/os.release.d/os-release-workstation

# Server
cp -p %{buildroot}/usr/lib/os.release.d/os-release-fedora \
      %{buildroot}/usr/lib/os.release.d/os-release-server
echo "VARIANT=\"Server Edition\"" >> %{buildroot}/usr/lib/os.release.d/os-release-server
echo "VARIANT_ID=server" >> %{buildroot}/usr/lib/os.release.d/os-release-server
sed -i -e "s|(%{release_name})|(Server Edition)|g" %{buildroot}/usr/lib/os.release.d/os-release-server

# Silverblue
cp -p %{buildroot}/usr/lib/os.release.d/os-release-fedora \
      %{buildroot}/usr/lib/os.release.d/os-release-silverblue
echo "VARIANT=\"Silverblue\"" >> %{buildroot}/usr/lib/os.release.d/os-release-silverblue
echo "VARIANT_ID=silverblue" >> %{buildroot}/usr/lib/os.release.d/os-release-silverblue
sed -i -e "s|(%{release_name})|(Silverblue)|g" %{buildroot}/usr/lib/os.release.d/os-release-silverblue

# Set up the dist tag macros
install -d -m 755 %{buildroot}%{_rpmconfigdir}/macros.d
cat >> %{buildroot}%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%fedora		%{version}
%%dist		%%{?distprefix}.fc%{version}
%%fc%{version}		1
EOF

# Add presets
mkdir -p %{buildroot}%{_prefix}/lib/systemd/user-preset/
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset/
mkdir -p %{buildroot}%{_prefix}/lib/os.release.d/presets


# Default system wide
install -m 0644 90-default-user.preset %{buildroot}%{_prefix}/lib/systemd/user-preset/
install -m 0644 85-display-manager.preset %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 90-default.preset %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 99-default-disable.preset %{buildroot}%{_prefix}/lib/systemd/system-preset/
# Fedora Server
install -m 0644 80-server.preset %{buildroot}%{_prefix}/lib/os.release.d/presets/
install -m 0644 80-server.preset %{buildroot}%{_prefix}/lib/systemd/system-preset/
# Fedora Workstation
install -m 0644 80-workstation.preset %{buildroot}%{_prefix}/lib/os.release.d/presets/
install -m 0644 80-workstation.preset %{buildroot}%{_prefix}/lib/systemd/system-preset/

# Install Polkit Rules
mkdir -p %{buildroot}%{_datadir}/polkit-1/rules.d/
install -m 0644 org.projectatomic.rpmostree1.rules %{buildroot}%{_datadir}/polkit-1/rules.d/

%clean
rm -rf %{buildroot}

%files
%license LICENSE README.license
%dir /usr/lib/os.release.d
%dir /usr/lib/os.release.d/presets
%attr(0644,root,root) /usr/lib/os.release.d/os-release-fedora
%attr(0644,root,root) /usr/lib/os-release
/etc/os-release
%attr(0644,root,root) /etc/fedora-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%attr(0644,root,root) /usr/lib/issue
%config(noreplace) /etc/issue
%attr(0644,root,root) /usr/lib/issue.net
%config(noreplace) /etc/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir %{_prefix}/lib/systemd/user-preset/
%{_prefix}/lib/systemd/user-preset/90-default-user.preset
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset

%files workstation
%attr(0644,root,root) /usr/lib/os.release.d/os-release-workstation
%{_prefix}/lib/systemd/system-preset/80-workstation.preset
%attr(0644,root,root) /usr/lib/os.release.d/presets/80-workstation.preset
%attr(0644,root,root) /usr/share/polkit-1/rules.d/org.projectatomic.rpmostree1.rules

%files server
%attr(0644,root,root) /usr/lib/os.release.d/os-release-server
%{_prefix}/lib/systemd/system-preset/80-server.preset
%attr(0644,root,root) /usr/lib/os.release.d/presets/80-server.preset

%files silverblue
%attr(0644,root,root) /usr/lib/os.release.d/os-release-silverblue

%files notes
%defattr(-,root,root,-)
%doc README.Dapper-Release-Notes

%changelog
* Sat Nov  3 2018 Matthew Ruffell <msr50@uclive.ac.nz> - 29-1
- Dapper Linux 29
- Add selinux-autorelabel-mark.service to default presets
- Enable the pipewire service for user sessions
- fedora-* renamed to OS independent names
- Server: don't require rolekit (not installable, soon to be retired)
- Drop rolekit from Server presets too
- Drop Recommends: fedora-repos-modular from Server Edition since it has been
- Small spec file cleanups
- Escape %distprefix in the spec
- Enable dbus units explicitly
- Use %buildroot
- Drop sssd-secrets.socket from presets
- Add in silverblue
- set cpi.service as enabled in the systemd presets
- set device_cio_free service as enabled
- Enable the stratis daemon in presets
- Add ostree-finalize-staged.path preset

* Sat May  5 2018 Matthew Ruffell <msr50@uclive.ac.nz> - 28-1
- Dapper Linux 28
- Enable the virtualbox-guest-additions service (vboxservice.service)
- Add PLATFORM_ID to /etc/os-release
- Add polkit rules to let gnome-software update Atomic Workstation
- Drop %%config from files in /usr

* Fri Aug 17 2017 Matthew Ruffell <msr50@uclive.ac.nz> - 27-1
- Dapper Linux 27

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
