%global debug_package %{nil}
%global dkms_name vendor-reset

Name:       %{dkms_name}-dkms
Version:    {{{ git_dir_version }}}
Release:    1%{?dist}
Summary:    Linux kernel vendor specific hardware reset module
License:    GPLv2
URL:        https://github.com/KyleGospo/vendor-reset
BuildArch:  noarch

Source:     {{{ git_dir_pack }}}

Provides:   %{dkms_name}-dkms = %{version}
Requires:   dkms

%description
A kernel module that is capable of resetting hardware devices into a state where they can be re-initialized or passed through into a virtual machine (VFIO).

%prep
{{{ git_dir_setup_macro }}}

%build

%install
# Create empty tree
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr * %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

install -d %{buildroot}%{_sysconfdir}/modules-load.d
cat > %{buildroot}%{_sysconfdir}/modules-load.d/vendor-reset.conf << EOF
vendor-reset
EOF

%post -n %{name}
dkms add -m %{dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry
dkms remove -m %{dkms_name} -v %{version} -q --all || :

%files
%license LICENSE
%doc README.md
%{_usrsrc}/%{dkms_name}-%{version}
%{_sysconfdir}/modules-load.d/vendor-reset.conf

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
{{{ git_dir_changelog }}}