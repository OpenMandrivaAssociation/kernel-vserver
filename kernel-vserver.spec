# -*- Mode: rpm-spec -*-
#
# (c) Mandriva
#
# The kernel-2.6-linus package (and so this spec file) is under development,
# it does mean:
#
#    1. You can have nasty surprises when playing with the package
#    generation
#
#    2. Is easier to go and come back from Mordor than adding a new
#    architecture support
#
#    3. A known architecture with just a missing .config shouldn't be too
#    hard, but as this spec changes too fast, it's likely to be broken
# 
#
# if you try to understand kernel numbering, read docs/kernel_naming

%define kernelversion	2
%define patchlevel	6
%define sublevel	22

%define vserver_version 2.2.0.4

# kernel Makefile extraversion is substituted by 
# kpatch/kstable wich are either 0 (empty), rc (kpatch) or stable release (kstable)
%define kpatch		0
%define kstable		9

# this is the releaseversion
%define mdvrelease 	1

# This is only to make life easier for people that creates derivated kernels
# a.k.a name it kernel-tmb :)
%define kname 		kernel-vserver

%define rpmtag		%distsuffix
%if %kpatch
%define rpmrel		%mkrel 0.%{kpatch}.%{mdvrelease}
%else
%define rpmrel		%mkrel %{mdvrelease}
%endif

# theese two never change, they are used to fool rpm/urpmi/smart
%define fakever		1
%define fakerel		%mkrel 1

# When we are using a pre/rc patch, the tarball is a sublevel -1
%if %kpatch
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}
%define tar_ver	  	%{kernelversion}.%{patchlevel}.%(expr %{sublevel} - 1)
%else
%if %kstable
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}.%{kstable}
%define tar_ver   	%{kernelversion}.%{patchlevel}.%{sublevel}
%else
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}
%define tar_ver   	%{kversion}
%endif
%endif
%define kverrel   	%{kversion}-%{rpmrel}

# used for not making too long names for rpms or search paths
%if %kpatch
%define buildrpmrel     0.%{kpatch}.%{mdvrelease}%{rpmtag}
%else
%define buildrpmrel     %{mdvrelease}%{rpmtag}
%endif

%define buildrel        %{kversion}-%{buildrpmrel}

%define vserver_notice NOTE: This kernel is built with Vserver support. \
It has no Mandriva patches and no third-party drivers. \
Linux-VServer provides virtualization for GNU/Linux systems. \
This is accomplished by kernel level isolation. It allows to run \
multiple virtual units at once. Those units are sufficiently isolated \
to guarantee the required security, but utilize available resources \
efficiently, as they run on the same kernel.


# having different top level names for packges means that you have to remove them by hard :(
%define top_dir_name    %{kname}-%{_arch}

%define build_dir       ${RPM_BUILD_DIR}/%{top_dir_name}
%define src_dir         %{build_dir}/linux-%{tar_ver}

# disable useless debug rpms...
%define _enable_debug_packages  %{nil}
%define debug_package           %{nil}

# build defines
%define build_doc 0
%define build_source 1
%define build_devel 1

%define build_up 1
%define build_smp 0

%define distro_branch %(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1.$2"' /etc/mandriva-release)

# End of user definitions
%{?_without_up: %global build_up 0}
%{?_without_smp: %global build_smp 0}
%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}
%{?_without_devel: %global build_devel 0}

%{?_with_up: %global build_up 1}
%{?_with_smp: %global build_smp 1}
%{?_with_doc: %global build_doc 1}
%{?_with_source: %global build_source 1}
%{?_with_devel: %global build_devel 1}


%if %(if [ -z "$CC" ] ; then echo 0; else echo 1; fi)
%define kmake %make CC="$CC"
%else
%define kmake %make 
%endif
# there are places where parallel make don't work
%define smake make

# Aliases for amd64 builds (better make source links?)
%define target_cpu	%(echo %{_target_cpu} | sed -e "s/amd64/x86_64/")
%define target_arch	%(echo %{_arch} | sed -e "s/amd64/x86_64/" -e "s/sparc/%{_target_cpu}/")

# src.rpm description
Summary: 	The Linux kernel (the core of the Linux operating system)
Name:           %{kname}
Version:        %{vserver_version}
Epoch:		1
Release:        %{rpmrel}
License: 	GPL
Group: 		System/Cluster
ExclusiveArch: 	%{ix86} x86_64
ExclusiveOS: 	Linux
URL: 		http://wiki.mandriva.com/en/Docs/Howto/Manbo_Kernels#kernel-vserver

####################################################################
#
# Sources
#
### This is for full SRC RPM
Source0:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2
Source1:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2.sign

Source4:  README.kernel-sources
Source5:  README.MandrivaLinux

Source20: kernel-2.6.22-i386.config
Source21: kernel-2.6.22-x86_64.config


####################################################################
#
# Patches

#
# Patch0 to Patch100 are for core kernel upgrades.
#

# Pre linus patch: ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing

%if %kpatch
Patch1:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}.bz2
Source10:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}.bz2.sign
%endif
%if %kstable
Patch1:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.bz2
Source10:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.bz2.sign
%endif

# VServer patches
Patch200: http://ftp.linux-vserver.org/pub/kernel/vs2.2/testing/patch-%{kversion}-vs%{vserver_version}.diff

#END
####################################################################

# Defines for the things that are needed for all the kernels
%define requires1 module-init-tools >= 3.0-%mkrel 7
%define requires2 mkinitrd >= 3.4.43-%mkrel 10
%define requires3 bootloader-utils >= 1.9
%define requires4 sysfsutils module-init-tools >= 0.9.15

%define kprovides kernel = %{tar_ver}, alsa, kernel-vserver-krgversion = %{vserver_version}-%{rpmrel}

BuildRoot: 	%{_tmppath}/%{name}-%{kversion}-build-%{_arch}
Autoreqprov: 	no
BuildRequires: 	gcc module-init-tools >= 0.9.15

%description
Source package to build the Linux kernel.

%{vserver_notice}



#
# kernel: UP kernel
#

%package -n %{kname}-%{buildrel}
Version:	%{fakever}
Release:	%{fakerel}
Summary:        The Linux kernel (the core of the Linux operating system) with Vserver support
Group: 	  	System/Cluster
Provides: 	module-info, %kprovides
Requires: 	%requires1
Requires: 	%requires2
Requires: 	%requires3
Requires: 	%requires4

%description -n %{kname}-%{buildrel}
The kernel package contains the Linux kernel (vmlinuz), the core of your
Mandriva Linux operating system. The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.

For instructions for update, see:
http://www.mandriva.com/en/security/kernelupdate

%{vserver_notice}



#
# kernel-smp: Symmetric MultiProcessing kernel
#

%package -n %{kname}-smp-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Summary:  The Linux Kernel compiled for SMP machines
Group: 	  System/Kernel and hardware
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3
Requires: %requires4

%description -n %{kname}-smp-%{buildrel}
This package includes a SMP version of the Linux %{kversion} kernel. It is
required only on machines with two or more CPUs, although it should work
fine on single-CPU boxes.

For instructions for update, see:
http://www.mandriva.com/en/security/kernelupdate

%{vserver_notice}



#
# kernel-source: kernel sources
#

%package -n %{kname}-source-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Provides: %{kname}-source, kernel-source = %{kverrel}, kernel-devel = %{kverrel}
Requires: glibc-devel, ncurses-devel, make, gcc, perl
Summary:  The source code for the Linux kernel
Group:    System/Cluster
Autoreqprov: no

%description -n %{kname}-source-%{buildrel}
The %{kname}-source package contains the source code files for the Linux 
kernel. Theese source files are only needed if you want to build your own 
custom kernel that is better tuned to your particular hardware.

If you only want the files needed to build 3rdparty (nVidia, Ati, dkms-*,...)
drivers against, install the *-devel-* rpm that is matching your kernel.

For instructions for update, see:
http://www.mandriva.com/en/security/kernelupdate

%{vserver_notice}



# 
# kernel-devel-up: stripped kernel sources 
#

%package -n %{kname}-devel-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Provides: kernel-devel = %{kverrel}
Summary:  The %{kname} devel files for 3rdparty modules build
Group:    System/Cluster
Autoreqprov: no
Requires: glibc-devel, ncurses-devel, make, gcc, perl

%description -n %{kname}-devel-%{buildrel}
This package contains the kernel-devel files that should be enough to build 
3rdparty drivers against for use with %{kname}-%{buildrel}.

If you want to build your own kernel, you need to install the full 
%{kname}-source-%{buildrel} rpm.

%{vserver_notice}



# 
# kernel-devel-smp: stripped kernel sources 
#

%package -n %{kname}-smp-devel-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Provides: kernel-devel = %{kverrel}
Summary:  The %{kname}-smp devel files for 3rdparty modules build
Group:    Development/Kernel
Autoreqprov: no
Requires: glibc-devel, ncurses-devel, make, gcc, perl

%description -n %{kname}-smp-devel-%{buildrel}
This package contains the kernel-devel files that should be enough to build 
3rdparty drivers against for use with the %{kname}-smp-%{buildrel}.

If you want to build your own kernel, you need to install the full 
%{kname}-source-%{buildrel} rpm.

%{vserver_notice}



#
# kernel-doc: documentation for the Linux kernel
#

%package -n %{kname}-doc-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Summary:  Various documentation bits found in the kernel source
Group:    Books/Computer books

%description -n %{kname}-doc-%{buildrel}
This package contains documentation files form the kernel source. Various
bits of information about the Linux kernel and the device drivers shipped
with it are documented in these files. You also might want install this
package if you need a reference to the options that can be passed to Linux
kernel modules at load time.

For instructions for update, see:
http://www.mandriva.com/en/security/kernelupdate

%{vserver_notice}



#
# kernel-latest: virtual rpm
#

%package -n %{kname}-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-%{buildrel}

%description -n %{kname}-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname} installed...

%{vserver_notice}



#
# kernel-smp-latest: virtual rpm
#

%package -n %{kname}-smp-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-smp
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-smp-%{buildrel}

%description -n %{kname}-smp-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-smp installed...

%{vserver_notice}



#
# kernel-source-latest: virtual rpm
#

%package -n %{kname}-source-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-source
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-source-%{buildrel}

%description -n %{kname}-source-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-source installed...

%{vserver_notice}



#
# kernel-devel-latest: virtual rpm
#

%package -n %{kname}-devel-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-devel
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-devel-%{buildrel}
Obsoletes:	%{kname}-headers-latest

%description -n %{kname}-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-devel installed...

%{vserver_notice}



#
# kernel-smp-devel-latest: virtual rpm
#

%package -n %{kname}-smp-devel-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-smp-devel
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-smp-devel-%{buildrel}
Obsoletes:	%{kname}-smp-headers-latest

%description -n %{kname}-smp-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-smp-devel installed...

%{vserver_notice}



#
# kernel-doc-latest: virtual rpm
#

%package -n %{kname}-doc-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-doc
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-doc-%{buildrel}

%description -n %{kname}-doc-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-doc installed...

%{vserver_notice}



#
# End packages - here begins build stage
#
%prep
%setup -q -n %top_dir_name -c

pushd %src_dir
%if %kpatch
%patch1 -p1
%endif
%if %kstable
%patch1 -p1
%endif

# vserver patches
%patch200 -p1
popd
# PATCH END



#
# Setup Begin
#

pushd ${RPM_SOURCE_DIR}

#
# Copy our defconfigs into place.
for i in i386 sparc64 x86_64; do
	[ ! -f kernel-%{tar_ver}-$i.config ] || cp -f kernel-%{tar_ver}-$i.config %{build_dir}/linux-%{tar_ver}/arch/$i/defconfig
done
popd

# make sure the kernel has the sublevel we know it has...
LC_ALL=C perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" linux-%{tar_ver}/Makefile



%build
# Common target directories
%define _kerneldir /usr/src/%{kname}-%{buildrel}
%define _bootdir /boot
%define _modulesdir /lib/modules
%define _up_develdir /usr/src/%{kname}-devel-%{buildrel}
%define _smp_develdir /usr/src/%{kname}-devel-%{buildrel}smp



# Directories definition needed for building
%define temp_root %{build_dir}/temp-root
%define temp_source %{temp_root}%{_kerneldir}
%define temp_boot %{temp_root}%{_bootdir}
%define temp_modules %{temp_root}%{_modulesdir}
%define temp_up_devel %{temp_root}%{_up_develdir}
%define temp_smp_devel %{temp_root}%{_smp_develdir}



PrepareKernel() {
	name=$1
	extension=$2
	echo "Prepare compilation of kernel $extension"

	if [ "$name" ]; then
		config_name="defconfig-$name"
	else
		config_name="defconfig"
	fi

	# make sure EXTRAVERSION says what we want it to say
	%if %kstable
		LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = .%{kstable}-$extension/" Makefile
	%else
		LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -$extension/" Makefile
	%endif

	%smake -s mrproper
	cp arch/%{target_arch}/$config_name .config
	%smake oldconfig
}



BuildKernel() {
	KernelVer=$1
	echo "Building kernel $KernelVer"

	%kmake all

	## Start installing stuff
	install -d %{temp_boot}
	install -m 644 System.map %{temp_boot}/System.map-$KernelVer
	install -m 644 .config %{temp_boot}/config-$KernelVer

	%ifarch sparc64
	gzip -9c vmlinux > %{temp_boot}/vmlinuz-$KernelVer
	%else
	cp -f arch/%{target_arch}/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
	%endif

	# modules
	install -d %{temp_modules}/$KernelVer
	%smake INSTALL_MOD_PATH=%{temp_root} KERNELRELEASE=$KernelVer modules_install 
}



SaveDevel() {
	flavour=$1
	if [ "$flavour" = "up" ]; then
		DevelRoot=%{temp_up_devel}
	else
		DevelRoot=%{temp_smp_devel}
	fi
	mkdir -p $DevelRoot
	for i in $(find . -name Makefile -o -name Makefile-* -o -name Makefile.*); do cp -R --parents $i $DevelRoot;done
	for i in $(find . -name Kconfig -o -name Kconfig.* -o -name Kbuild -o -name Kbuild.*); do cp -R --parents $i $DevelRoot;done
	cp -fR include $DevelRoot
	cp -fR scripts $DevelRoot
	cp -fR arch/%{target_arch}/kernel/asm-offsets.{c,s} $DevelRoot/arch/%{target_arch}/kernel/
	%ifarch %{ix86}
	cp -fR arch/%{target_arch}/kernel/sigframe.h $DevelRoot/arch/%{target_arch}/kernel/
	%endif
	cp -fR .config Module.symvers $DevelRoot
	
### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
#	mkdir -p $DevelRoot/arch/s390/crypto/
#	cp -fR arch/s390/crypto/Kconfig $DevelRoot/arch/s390/crypto/
	
        # Needed for truecrypt build (Danny)
	#mkdir -p $DevelRoot/drivers/md/
	#cp -fR drivers/md/dm.h $DevelRoot/drivers/md/

	# fix permissions
	chmod -R a+rX $DevelRoot
	
	# Clean the scripts tree
	pushd $DevelRoot >/dev/null
		%smake -s clean
	popd >/dev/null
	
}



CreateFiles() {
	kernversion=$1
	output=../kernel_files.$kernversion

	echo "%defattr(-,root,root)" > $output
	echo "%{_bootdir}/config-${kernversion}" >> $output
	echo "%{_bootdir}/vmlinuz-${kernversion}" >> $output
	echo "%{_bootdir}/System.map-${kernversion}" >> $output
	echo "%dir %{_modulesdir}/${kernversion}/" >> $output
	echo "%{_modulesdir}/${kernversion}/kernel" >> $output
	echo "%{_modulesdir}/${kernversion}/modules.*" >> $output
	echo "%doc README.kernel-sources" >> $output
	echo "%doc README.MandrivaLinux" >> $output
#	echo "%doc README.urpmi" >> $output
}



CreateKernel() {
	flavour=$1

	if [ "$flavour" = "up" ]; then
		KernelVer=%{buildrel}
		PrepareKernel "" %{buildrpmrel}
	else
		KernelVer=%{buildrel}$flavour
		PrepareKernel $flavour %{buildrpmrel}$flavour
	fi

	BuildKernel $KernelVer
	%if %build_devel
	    SaveDevel $flavour
	%endif
        CreateFiles $KernelVer
}



###
# DO it...
###



# Create a simulacro of buildroot
rm -rf %{temp_root}
install -d %{temp_root}



#make sure we are in the directory
cd %src_dir

%if %build_smp
CreateKernel smp
%endif

%if %build_up
CreateKernel up
%endif



# We don't make to repeat the depend code at the install phase
%if %build_source
PrepareKernel "" %{buildrpmrel}
# From > 2.6.13 prepare-all is deprecated and relies on include/linux/autoconf
# To have modpost and others scripts, one has to use the target scripts
%smake -s prepare
%smake -s scripts
%smake -s clean
%endif



###
### install
###
%install
install -m 644 %{SOURCE4}  .
install -m 644 %{SOURCE5}  .
#install -m 644 %{SOURCE6}  README.urpmi

cd %src_dir
# Directories definition needed for installing
%define target_source %{buildroot}/%{_kerneldir}
%define target_boot %{buildroot}%{_bootdir}
%define target_modules %{buildroot}%{_modulesdir}
%define target_up_devel %{buildroot}%{_up_develdir}
%define target_smp_devel %{buildroot}%{_smp_develdir}

# We want to be able to test several times the install part
rm -rf %{buildroot}
cp -a %{temp_root} %{buildroot}

# Create directories infastructure
%if %build_source
install -d %{target_source} 

tar cf - . | tar xf - -C %{target_source}
chmod -R a+rX %{target_source}



# we remove all the source files that we don't ship

# first architecture files
for i in alpha arm arm26 avr32 blackfin cris frv h8300 ia64 mips m32r m68k m68knommu parisc powerpc ppc sh sh64 s390 v850 xtensa; do
	rm -rf %{target_source}/arch/$i
	rm -rf %{target_source}/include/asm-$i

### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
#	mkdir -p %{target_source}/arch/s390/crypto/
#	cp -fR arch/s390/crypto/Kconfig %{target_source}/arch/s390/crypto/
%if %build_devel
	rm -rf %{target_up_devel}/arch/$i
	rm -rf %{target_up_devel}/include/asm-$i
	rm -rf %{target_smp_devel}/arch/$i
	rm -rf %{target_smp_devel}/include/asm-$i

### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
#	mkdir -p %{target_up_devel}/arch/s390/crypto/
#	mkdir -p %{target_smp_devel}/arch/s390/crypto/
#	cp -fR arch/s390/crypto/Kconfig %{target_up_devel}/arch/s390/crypto/
#	cp -fR arch/s390/crypto/Kconfig %{target_smp_devel}/arch/s390/crypto/

        # Needed for truecrypt build (Danny)
#	mkdir -p %{target_up_devel}/drivers/md/
#	mkdir -p %{target_smp_devel}/drivers/md/
#	cp -fR drivers/md/dm.h %{target_up_devel}/drivers/md/
#	cp -fR drivers/md/dm.h %{target_smp_devel}/drivers/md/

%endif	
done

# remove arch files based on target arch
%ifnarch %{ix86} x86_64
	rm -rf %{target_source}/arch/i386
	rm -rf %{target_source}/arch/x86_64
	rm -rf %{target_source}/include/asm-i386
	rm -rf %{target_source}/include/asm-x86_64
%if %build_devel
	rm -rf %{target_up_devel}/arch/i386
	rm -rf %{target_up_devel}/arch/x86_64
	rm -rf %{target_up_devel}/include/asm-i386
	rm -rf %{target_up_devel}/include/asm-x86_64
	rm -rf %{target_smp_devel}/arch/i386
	rm -rf %{target_smp_devel}/arch/x86_64
	rm -rf %{target_smp_devel}/include/asm-i386
	rm -rf %{target_smp_devel}/include/asm-x86_64
%endif
%endif
%ifnarch sparc sparc64
	rm -rf %{target_source}/arch/sparc
	rm -rf %{target_source}/arch/sparc64
	rm -rf %{target_source}/include/asm-sparc
	rm -rf %{target_source}/include/asm-sparc64
%if %build_devel
	rm -rf %{target_up_devel}/arch/sparc
	rm -rf %{target_up_devel}/arch/sparc64
	rm -rf %{target_up_devel}/include/asm-sparc
	rm -rf %{target_up_devel}/include/asm-sparc64
	rm -rf %{target_smp_devel}/arch/sparc
	rm -rf %{target_smp_devel}/arch/sparc64
	rm -rf %{target_smp_devel}/include/asm-sparc
	rm -rf %{target_smp_devel}/include/asm-sparc64
%endif	
%endif


# other misc files
rm -f %{target_source}/{.config.old,.config.cmd,.tmp_gas_check,.mailmap,.missing-syscalls.d}

#endif %build_source
%endif



# gzipping modules
find %{target_modules} -name "*.ko" | xargs gzip -9



# We used to have a copy of PrepareKernel here
# Now, we make sure that the thing in the linux dir is what we want it to be

for i in %{target_modules}/*; do
  rm -f $i/build $i/source $i/modules.*
done



# sniff, if we gzipped all the modules, we change the stamp :(
# we really need the depmod -ae here

pushd %{target_modules}
for i in *; do
	/sbin/depmod -u -ae -b %{buildroot} -r -F %{target_boot}/System.map-$i $i
	echo $?
done

for i in *; do
	pushd $i
	echo "Creating module.description for $i"
	modules=`find . -name "*.ko.gz"`
	echo $modules | xargs /sbin/modinfo-25 \
	| perl -lne 'print "$name\t$1" if $name && /^description:\s*(.*)/; $name = $1 if m!^filename:\s*(.*)\.k?o!; $name =~ s!.*/!!' > modules.description
	popd
done
popd



###
### clean
###

%clean
rm -rf %{buildroot}
# We don't want to remove this, the whole reason of its existence is to be 
# able to do several rpm --short-circuit -bi for testing install 
# phase without repeating compilation phase
#rm -rf %{temp_root} 



###
### scripts
###

### UP kernel
%preun -n %{kname}-%{buildrel}
/sbin/installkernel -R %{buildrel}
if [ -L /lib/modules/%{buildrel}/build ]; then
    rm -f /lib/modules/%{buildrel}/build
fi
if [ -L /lib/modules/%{buildrel}/source ]; then
    rm -f /lib/modules/%{buildrel}/source
fi
exit 0

%post -n %{kname}-%{buildrel}
/sbin/installkernel -L %{buildrel}
if [ -d /usr/src/%{kname}-devel-%{buildrel} ]; then
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/build
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/source
fi

%postun -n %{kname}-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}



### SMP kernel
%preun -n %{kname}-smp-%{buildrel}
/sbin/installkernel -R %{buildrel}smp
if [ -L /lib/modules/%{buildrel}smp/build ]; then
    rm -f /lib/modules/%{buildrel}smp/build
fi
if [ -L /lib/modules/%{buildrel}smp/source ]; then
    rm -f /lib/modules/%{buildrel}smp/source
fi
exit 0

%post -n %{kname}-smp-%{buildrel}
/sbin/installkernel -L %{buildrel}smp
if [ -d /usr/src/%{kname}-devel-%{buildrel}smp ]; then
    ln -sf /usr/src/%{kname}-devel-%{buildrel}smp /lib/modules/%{buildrel}smp/build
    ln -sf /usr/src/%{kname}-devel-%{buildrel}smp /lib/modules/%{buildrel}smp/source
fi

%postun -n %{kname}-smp-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}smp



### kernel-devel
%post -n %{kname}-devel-%{buildrel}
# place /build and /source symlinks in place.
if [ -d /lib/modules/%{buildrel} ]; then
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/build
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/source
fi

%preun -n %{kname}-devel-%{buildrel}
# we need to delete <modules>/{build,source} at uninstall
if [ -L /lib/modules/%{buildrel}/build ]; then
    rm -f /lib/modules/%{buildrel}/build
fi
if [ -L /lib/modules/%{buildrel}/source ]; then
    rm -f /lib/modules/%{buildrel}/source
fi
exit 0



### kernel-smp-devel
%post -n %{kname}-smp-devel-%{buildrel}
# place /build and /source symlinks in place.
if [ -d /lib/modules/%{buildrel}smp ]; then
    ln -sf /usr/src/%{kname}-devel-%{buildrel}smp /lib/modules/%{buildrel}smp/build
    ln -sf /usr/src/%{kname}-devel-%{buildrel}smp /lib/modules/%{buildrel}smp/source
fi

%preun -n %{kname}-smp-devel-%{buildrel}
# we need to delete <modules>/{build,source} at uninstall
if [ -L /lib/modules/%{buildrel}smp/build ]; then
    rm -f /lib/modules/%{buildrel}smp/build
fi
if [ -L /lib/modules/%{buildrel}smp/source ]; then
    rm -f /lib/modules/%{buildrel}smp/source
fi
exit 0



### kernel-source
%post -n %{kname}-source-%{buildrel}
for i in /lib/modules/%{buildrel}*; do
	if [ -d $i ]; then
	        rm -f $i/{build,source}
	        ln -sf /usr/src/%{kname}-%{buildrel} $i/build
	        ln -sf /usr/src/%{kname}-%{buildrel} $i/source
	fi
done
								
%preun -n %{kname}-source-%{buildrel}
for i in /lib/modules/%{buildrel}/{build,source}; do
	if [ -L $i ]; then
		rm -f $i
	fi
done
exit 0
												

###
### file lists
###

%if %build_up
%files -n %{kname}-%{buildrel} -f kernel_files.%{buildrel}
%endif

%if %build_smp
%files -n %{kname}-smp-%{buildrel} -f kernel_files.%{buildrel}smp
%endif

%if %build_source
%files -n %{kname}-source-%{buildrel}
%defattr(-,root,root)
%dir %{_kerneldir}
%dir %{_kerneldir}/arch
%dir %{_kerneldir}/include
%{_kerneldir}/.config
%{_kerneldir}/.gitignore
%{_kerneldir}/COPYING
%{_kerneldir}/CREDITS
%{_kerneldir}/Documentation
%{_kerneldir}/Kbuild
%{_kerneldir}/MAINTAINERS
%{_kerneldir}/Makefile
%{_kerneldir}/README
%{_kerneldir}/REPORTING-BUGS
### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
#%{_kerneldir}/arch/s390
%ifarch sparc sparc64
%{_kerneldir}/arch/sparc
%{_kerneldir}/arch/sparc64
%endif
%ifarch %{ix86} x86_64
%{_kerneldir}/arch/i386
%{_kerneldir}/arch/x86_64
%endif
%{_kerneldir}/arch/um
%{_kerneldir}/block
%{_kerneldir}/crypto
%{_kerneldir}/drivers
%{_kerneldir}/fs
%{_kerneldir}/include/Kbuild
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm
%{_kerneldir}/include/asm-generic
%ifarch sparc sparc64
%{_kerneldir}/include/asm-sparc
%{_kerneldir}/include/asm-sparc64
%endif
%ifarch %{ix86} x86_64
%{_kerneldir}/include/asm-i386
%{_kerneldir}/include/asm-x86_64
%endif
%{_kerneldir}/include/asm-um
%{_kerneldir}/include/config
%{_kerneldir}/include/crypto
%{_kerneldir}/include/linux
%{_kerneldir}/include/math-emu
%{_kerneldir}/include/net
%{_kerneldir}/include/pcmcia
%{_kerneldir}/include/scsi
%{_kerneldir}/include/sound
%{_kerneldir}/include/video
%{_kerneldir}/include/media
%{_kerneldir}/include/mtd
%{_kerneldir}/include/rxrpc
%{_kerneldir}/include/keys
%{_kerneldir}/include/rdma
%{_kerneldir}/init
%{_kerneldir}/ipc
%{_kerneldir}/kernel
%{_kerneldir}/lib
%{_kerneldir}/mm
%{_kerneldir}/net
%{_kerneldir}/security
%{_kerneldir}/scripts
%{_kerneldir}/sound
%{_kerneldir}/usr
%doc README.kernel-sources
%doc README.MandrivaLinux
%endif

%if %build_devel
# kernel-devel
%if %build_up
%files -n %{kname}-devel-%{buildrel}
%defattr(-,root,root)
%dir %{_up_develdir}
%dir %{_up_develdir}/arch
%dir %{_up_develdir}/include
%{_up_develdir}/.config
%{_up_develdir}/Documentation
%{_up_develdir}/Kbuild
%{_up_develdir}/Makefile
%{_up_develdir}/Module.symvers
### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
#%{_up_develdir}/arch/s390
%ifarch sparc sparc64
%{_up_develdir}/arch/sparc
%{_up_develdir}/arch/sparc64
%endif
%ifarch %{ix86} x86_64
%{_up_develdir}/arch/i386
%{_up_develdir}/arch/x86_64
%endif
%{_up_develdir}/arch/um
%{_up_develdir}/block
%{_up_develdir}/crypto
%{_up_develdir}/drivers
%{_up_develdir}/fs
%{_up_develdir}/include/Kbuild
%{_up_develdir}/include/acpi
%{_up_develdir}/include/asm
%{_up_develdir}/include/asm-generic
%ifarch sparc sparc64
%{_up_develdir}/include/asm-sparc
%{_up_develdir}/include/asm-sparc64
%endif
%ifarch %{ix86} x86_64
%{_up_develdir}/include/asm-i386
%{_up_develdir}/include/asm-x86_64
%endif
%{_up_develdir}/include/asm-um
%{_up_develdir}/include/config
%{_up_develdir}/include/crypto
%{_up_develdir}/include/keys
%{_up_develdir}/include/linux
%{_up_develdir}/include/math-emu
%{_up_develdir}/include/mtd
%{_up_develdir}/include/net
%{_up_develdir}/include/pcmcia
%{_up_develdir}/include/rdma
%{_up_develdir}/include/scsi
%{_up_develdir}/include/sound
%{_up_develdir}/include/video
%{_up_develdir}/include/media
%{_up_develdir}/include/rxrpc
%{_up_develdir}/init
%{_up_develdir}/ipc
%{_up_develdir}/kernel
%{_up_develdir}/lib
%{_up_develdir}/mm
%{_up_develdir}/net
%{_up_develdir}/scripts
%{_up_develdir}/security
%{_up_develdir}/sound
%{_up_develdir}/usr
%doc README.kernel-sources
%doc README.MandrivaLinux
%endif

# kernel-smp-devel
%if %build_smp
%files -n %{kname}-smp-devel-%{buildrel}
%defattr(-,root,root)
%dir %{_smp_develdir}
%dir %{_smp_develdir}/arch
%dir %{_smp_develdir}/include
%{_smp_develdir}/.config
%{_smp_develdir}/Documentation
%{_smp_develdir}/Kbuild
%{_smp_develdir}/Makefile
%{_smp_develdir}/Module.symvers
### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
#%{_smp_develdir}/arch/s390
%ifarch sparc sparc64
%{_smp_develdir}/arch/sparc
%{_smp_develdir}/arch/sparc64
%endif
%ifarch %{ix86} x86_64
%{_smp_develdir}/arch/i386
%{_smp_develdir}/arch/x86_64
%endif
%{_smp_develdir}/arch/um
%{_smp_develdir}/block
%{_smp_develdir}/crypto
%{_smp_develdir}/drivers
%{_smp_develdir}/fs
%{_smp_develdir}/include/Kbuild
%{_smp_develdir}/include/acpi
%{_smp_develdir}/include/asm
%{_smp_develdir}/include/asm-generic
%ifarch sparc sparc64
%{_smp_develdir}/include/asm-sparc
%{_smp_develdir}/include/asm-sparc64
%endif
%ifarch %{ix86} x86_64
%{_smp_develdir}/include/asm-i386
%{_smp_develdir}/include/asm-x86_64
%endif
%{_smp_develdir}/include/asm-um
%{_smp_develdir}/include/config
%{_smp_develdir}/include/crypto
%{_smp_develdir}/include/keys
%{_smp_develdir}/include/linux
%{_smp_develdir}/include/math-emu
%{_smp_develdir}/include/mtd
%{_smp_develdir}/include/net
%{_smp_develdir}/include/pcmcia
%{_smp_develdir}/include/rdma
%{_smp_develdir}/include/scsi
%{_smp_develdir}/include/sound
%{_smp_develdir}/include/video
%{_smp_develdir}/include/media
%{_smp_develdir}/include/rxrpc
%{_smp_develdir}/init
%{_smp_develdir}/ipc
%{_smp_develdir}/kernel
%{_smp_develdir}/lib
%{_smp_develdir}/mm
%{_smp_develdir}/net
%{_smp_develdir}/scripts
%{_smp_develdir}/security
%{_smp_develdir}/sound
%{_smp_develdir}/usr
%doc README.kernel-sources
%doc README.MandrivaLinux
#endif %build_devel
%endif
%endif

%if %build_doc
%files -n %{kname}-doc-%{buildrel}
%defattr(-,root,root)
%doc linux-%{tar_ver}/Documentation/*
%endif

%if %build_up
%files -n %{kname}-latest
%defattr(-,root,root)
%endif

%if %build_smp
%files -n %{kname}-smp-latest
%defattr(-,root,root)
%endif

%if %build_source
%files -n %{kname}-source-latest
%defattr(-,root,root)
%endif

%if %build_devel
%files -n %{kname}-devel-latest
%defattr(-,root,root)

%if %build_smp
%files -n %{kname}-smp-devel-latest
%defattr(-,root,root)
%endif
%endif

%if %build_doc
%files -n %{kname}-doc-latest
%defattr(-,root,root)
%endif


