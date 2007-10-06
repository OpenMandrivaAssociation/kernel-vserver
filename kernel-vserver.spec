# -*- Mode: rpm-spec -*-

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
%define rpmrel		%mkrel %{mdvrelease}

# theese two never change, they are used to fool rpm/urpmi/smart
%define fakever		1
%define fakerel		%mkrel 1

# When we are using a pre/rc patch, the tarball is a sublevel -1
%if %kpatch
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}-0.%{kpatch}
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
%define buildrpmrel     %{mdvrelease}%{rpmtag}
%define buildrel        %{kversion}-%{buildrpmrel}

%define kvserver_notice NOTE: This kernel is built with VServer virtualization support.\
It has no Mandriva patches and no third-party drivers.

# having different top level names for packges means that you have to remove them by hard :(
%define top_dir_name    %{kname}-%{_arch}

%define build_dir       ${RPM_BUILD_DIR}/%{top_dir_name}
%define src_dir         %{build_dir}/linux-%{tar_ver}

# disable useless debug rpms...
%define _enable_debug_packages  %{nil}
%define debug_package           %{nil}

# build defines
%define build_kheaders 0
%define build_debug 0
%define build_doc 0
%define build_source 1

%define distro_branch %(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1.$2"' /etc/mandriva-release)
%define build_101 %(if [ `awk '{print $4}' /etc/mandriva-release` = 10.1 ];then echo 1; else echo 0; fi)
%define build_100 %(if [ `awk '{print $4}' /etc/mandriva-release` = 10.0 ];then echo 1; else echo 0; fi)
%define build_92 %(if [ `awk '{print $4}' /etc/mandriva-release` = 9.2 ];then echo 1; else echo 0; fi)

%define build_up 1
%define build_smp 0

%define build_secure 0

%ifarch %{ix86}
%define build_i586_up_1GB 0
%define build_i686_up_4GB 0
%define build_xbox 0
%else
%define build_i586_up_1GB 0
%define build_i686_up_4GB 0
%define build_xbox 0
%endif

%ifarch powerpc
%define build_power5 1
%define build_ppc970 0
%if ! %{build_ppc970}
# default to build for power5 only
%define build_up     0
%define build_smp    0
%endif
%else
%define build_power5 0
%endif

# End of user definitions
%{?_without_up: %global build_up 0}
%{?_without_smp: %global build_smp 0}
%{?_without_secure: %global build_secure 0}
%{?_without_i586up1GB: %global build_i586_up_1GB 0}
%{?_without_i686up4GB: %global build_i686_up_4GB 0}
%{?_without_xbox: %global build_xbox 0}
%{?_without_debug: %global build_debug 0}
%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}

%{?_with_up: %global build_up 1}
%{?_with_smp: %global build_smp 1}
%{?_with_secure: %global build_secure 1}
%{?_with_i586up1GB: %global build_i586_up_1GB 1}
%{?_with_i686up4GB: %global build_i686_up_4GB 1}
%{?_with_xbox: %global build_xbox 1}
%{?_with_debug: %global build_debug 1}
%{?_with_doc: %global build_doc 1}
%{?_with_source: %global build_source 1}

%{?_with_kheaders: %global build_kheaders 1}
%{?_with_92: %global build_92 1}
%{?_with_100: %global build_100 1}
%{?_with_101: %global build_101 1}

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
Version:        %{kversion}
Release:        %{rpmrel}
License: 	GPL
Group: 		System/Kernel and hardware
ExclusiveArch: 	%{ix86} alpha ppc powerpc ia64 x86_64 amd64 sparc sparc64
ExclusiveOS: 	Linux
URL: 		http://www.kernel.org/

####################################################################
#
# Sources
#
### This is for full SRC RPM
Source0:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2
Source1:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2.sign

Source4:  README.kernel-sources
Source5:  README.MandrivaLinux
Source14: kernel-linus-config.h
Source15: kernel-linus-mdvconfig.h
Source16: linux-merge-config.awk
Source17: update_configs

Source20: kernel-2.6.22-i386.config
Source22: kernel-2.6.22-x86_64.config

####################################################################
#
# Patches

#
# Patch0 to Patch100 are for core kernel upgrades.
#

# Pre linus patch: ftp://ftp.kernel.org/pub/linux/kernel/v2.%{major}/testing

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
%if %{build_100}
%define requires3 bootloader-utils >= 1.6
%else
%define requires3 bootloader-utils >= 1.9
%endif
%define requires4 sysfsutils module-init-tools >= 0.9.15

%define kprovides kernel = %{tar_ver}, alsa

BuildRoot: 	%{_tmppath}/%{name}-%{kversion}-build
Autoreqprov: 	no
BuildRequires: 	gcc module-init-tools >= 0.9.15

%description
Source package to build the Linux kernel.

%{kvserver_notice}

#
# kernel: UP kernel
#

%package -n %{kname}-%{buildrel}
Version:	%{fakever}
Release:	%{fakerel}
Summary: 	The Linux kernel (the core of the Linux operating system)
Group: 	  	System/Kernel and hardware
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
http://www.mandriva.com/security/kernelupdate

%{kvserver_notice}

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
http://www.mandriva.com/security/kernelupdate

%{kvserver_notice}

%package -n %{kname}-secure-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Summary:  The Linux Kernel compiled for SECURE machines
Group:    System/Kernel and hardware
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3
Requires: %requires4

%description -n %{kname}-secure-%{buildrel}
This package includes a SECURE version of the Linux %{kversion}
kernel. This package add options for kernel that make it more secure
for servers and such. See :

http://www.nsa.gov/selinux/

for list of features we have included.

For instructions for update, see:
http://www.mandriva.com/security/kernelupdate

%{kvserver_notice}

#
# kernel-xbox: XBox kernel
# 

%package -n %{kname}-xbox-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Summary:  The version of the Linux kernel used on XBox machines
Group:    System/Kernel and hardware
Url:      http://peoples.mandriva.com/~sbenedict/XBox/
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3
Requires: %requires4

%description -n %{kname}-xbox-%{buildrel}
This package includes a modified version of the Linux kernel.
This kernel is used for XBox machines only and should not
be used for a normal x86 machine.

For instructions for update, see:
http://www.mandriva.com/security/kernelupdate

%{kvserver_notice}

%package -n %{kname}-i586-up-1GB-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Summary:  The Linux Kernel compiled for up with less than 1GB
Group:    System/Kernel and hardware
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3
Requires: %requires4

%description -n %{kname}-i586-up-1GB-%{buildrel}
This package includes a kernel that has appropriate configuration options
enabled for the typical single processor desktop with up to 1GB of memory.

For instructions for update, see:
http://www.mandriva.com/security/kernelupdate

%{kvserver_notice}

%package -n %{kname}-i686-up-4GB-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Summary:  The Linux Kernel compiled for up with 4GB
Group:    System/Kernel and hardware
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3
Requires: %requires4

%description -n %{kname}-i686-up-4GB-%{buildrel}
This package includes a kernel that has appropriate configuration 
options enabled for the typical single processor machine with memory 
between 1GB and 4GB.

For instructions for update, see:
http://www.mandriva.com/security/kernelupdate

%{kvserver_notice}

%package -n %{kname}-i686-up-1GB-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Summary:  The Linux Kernel compiled for up with less than 1GB
Group:    System/Kernel and hardware
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3
Requires: %requires4

%description -n %{kname}-i686-up-1GB-%{buildrel}
This package includes a kernel that has appropriate configuration 
options enabled for the typical single processor machine with less 
than 1GB of memory.

For instructions for update, see:
http://www.mandriva.com/security/kernelupdate

%{kvserver_notice}

%package -n %{kname}-i686-smp-1GB-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Summary:  The Linux Kernel compiled for up with less than 1GB
Group:    System/Kernel and hardware
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3
Requires: %requires4

%description -n %{kname}-i686-smp-1GB-%{buildrel}
This package includes a kernel that has appropriate configuration 
options enabled for the typical multi processor (or Hyper-Threading) 
machines with less than 1GB of memory.

For instructions for update, see:
http://www.mandriva.com/security/kernelupdate

%{kvserver_notice}

#
# kernel-power5: Power5 kernel
#

%package -n %{kname}-power5-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Summary:  The POWER5 optimized kernel
Group:    System/Kernel and hardware
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3
Requires: %requires4

%description -n %{kname}-power5-%{buildrel}
The kernel-power5 package contains the POWER5 optimized kernel for
IBM OpenPower series systems.

%{kvserver_notice}

#
# kernel-source: kernel sources
#

%package -n %{kname}-source-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Provides: %{kname}-source, kernel-source
Requires: glibc-devel, ncurses-devel, make, gcc, perl
Summary:  The source code for the Linux kernel
Group:    Development/Kernel
Autoreqprov: no
Conflicts: %{kname}-source-stripped-%{buildrel}

%description -n %{kname}-source-%{buildrel}
The kernel-source package contains the source code files for the Linux
kernel. These source files are needed to build most C programs, since
they depend on the constants defined in the source code. The source
files can also be used to build a custom kernel that is better tuned to
your particular hardware, if you are so inclined (and you know what you're
doing).

For instructions for update, see:
http://www.mandriva.com/security/kernelupdate

%{kvserver_notice}

%package -n %{kname}-source-stripped-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Provides: %{kname}-source, kernel-source
Provides: %{kname}-source-2.%{major}
Requires: glibc-devel, ncurses-devel, make, gcc, perl
Summary:  The source code of the Linux kernel stripped for post build
Group:    Development/Kernel
Autoreqprov: no
Conflicts: %{kname}-source-%{buildrel}

%description -n %{kname}-source-stripped-%{buildrel}
The kernel-source package contains the source code files for the Linux
kernel. These source files are needed to build most C programs, since
they depend on the constants defined in the source code. The source
files can also be used to build a custom kernel that is better tuned to
your particular hardware, if you are so inclined (and you know what you're
doing).

%{kvserver_notice}

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
http://www.mandriva.com/security/kernelupdate

%{kvserver_notice}



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

%{kvserver_notice}



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

%{kvserver_notice}



#
# kernel-secure-latest: virtual rpm
#

%package -n %{kname}-secure-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-secure
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-secure-%{buildrel}

%description -n %{kname}-secure-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-secure installed...

%{kvserver_notice}



#
# kernel-xbox-latest: virtual rpm
#

%package -n %{kname}-xbox-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-xbox
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-xbox-%{buildrel}

%description -n %{kname}-xbox-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-xbox installed...

%{kvserver_notice}



#
# kernel-i586-up-1GB-latest: virtual rpm
#

%package -n %{kname}-i586-up-1GB-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-i586-up-1GB
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-i586-up-1GB-%{buildrel}

%description -n %{kname}-i586-up-1GB-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-i586-up-1GB installed...

%{kvserver_notice}



#
# kernel-i686-up-4GB-latest: virtual rpm
#

%package -n %{kname}-i686-up-4GB-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-i686-up-4GB
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-i686-up-4GB-%{buildrel}

%description -n %{kname}-i686-up-4GB-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-i686-up-4GB installed...

%{kvserver_notice}



#
# kernel-i686-up-1GB-latest: virtual rpm
#

%package -n %{kname}-i686-up-1GB-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-i686-up-1GB
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-i686-up-1GB-%{buildrel}

%description -n %{kname}-i686-up-1GB-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-i686-up-1GB installed...

%{kvserver_notice}



#
# kernel-power5-latest: virtual rpm
#

%package -n %{kname}-power5-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-power5
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-power5-%{buildrel}

%description -n %{kname}-power5-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-power5 installed...

%{kvserver_notice}



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

%{kvserver_notice}



#
# kernel-source-stripped-latest: virtual rpm
#

%package -n %{kname}-source-stripped-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-source-stripped
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-source-stripped-%{buildrel}

%description -n %{kname}-source-stripped-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-source-stripped installed...

%{kvserver_notice}



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

%{kvserver_notice}



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

# FIXME: Re-add config.h to support our Autoconf for now
install -m 644 %{SOURCE14} include/linux/config.h

# VServer patches
%patch200 -p1

popd

# Put here patchlevel patches

# PATCH END
#
# Setup Begin
#

pushd ${RPM_SOURCE_DIR}

# FIXME: The right way to it would be the loop only running through the arch's
# .config files. But the kernel build functions (defined in the %build
# section) expect the .config files exactly the way the current loop does.
# The build functions need to be fixed first.
for i in kernel-%{tar_ver}-*.config; do
	cp $i %{build_dir}/linux-%{tar_ver}/arch/%{target_arch}/$(basename $i)
done
popd

# make sure the kernel has the sublevel we know it has...
LC_ALL=C perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" linux-%{tar_ver}/Makefile

# get rid of unwanted files
# XXX: This was used in the previous mdv's kernel, doesn't seem needed any
# more. Let's keep it commented for now, can be totally removed if after
# more testing.
# find . -name '*~' -o -name '*.orig' -o -name '*.append' |xargs rm -f

%if %build_kheaders

kheaders_dirs=`echo $PWD/linux-%{tar_ver}/include/{asm-*,linux,sound}`

install -d kernel-headers/
cp -a $kheaders_dirs kernel-headers/
tar cf kernel-headers-%buildrel.tar kernel-headers/
bzip2 -9f kernel-headers-%buildrel.tar
rm -rf kernel-headers/
# build_kheaders
%endif

%build
# Common target directories
%define _kerneldir /usr/src/linux-%{buildrel}
%define _bootdir /boot
%ifarch ia64
%define _efidir %{_bootdir}/efi/mandriva
%endif
%define _modulesdir /lib/modules
%define _savedheaders ../../savedheaders/

# Directories definition needed for building
%define temp_root %{build_dir}/temp-root
%define temp_source %{temp_root}%{_kerneldir}
%define temp_boot %{temp_root}%{_bootdir}
%define temp_modules %{temp_root}%{_modulesdir}

PrepareKernel() {
	name=$1
	extension=$2
	# FIXME: Should be removed when we adopt a standard name for the
        # .config files
	config_name="kernel-%{tar_ver}-%{target_arch}.config"
	echo "Prepare compilation of kernel $extension"

	# We can't use only defconfig anymore because we have the autoconf patch,

	if [ "$name" ]; then
		config_name="kernel-%{tar_ver}-%{target_arch}-$name.config"
	fi

	# make sure EXTRAVERSION says what we want it to say
	%if %kpatch
		LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -0.%{kpatch}-$extension/" Makefile
	%else
	%if %kstable
		LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = .%{kstable}-$extension/" Makefile
	%else
		LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -$extension/" Makefile
	%endif
	%endif

	### FIXME MDV bugs #29744, #29074, #34055 c5, will be removed when fixed upstream
	LC_ALL=C perl -p -i -e "s/^source/### source/" drivers/crypto/Kconfig
	
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

	%ifarch alpha
	cp -f arch/alpha/boot/vmlinux.gz %{temp_boot}/vmlinuz-$KernelVer
	%endif
	%ifarch ia64
       	install -d %{temp_root}%{_efidir}
       	cp -f vmlinux.gz %{temp_root}%{_efidir}/vmlinuz-$KernelVer
       	pushd %{temp_boot}
       	ln -s %{_efidir}/vmlinuz-$KernelVer vmlinuz-$KernelVer
       	popd
       	%endif
	%ifarch sparc sparc64
	gzip -9c vmlinux > %{temp_boot}/vmlinuz-$KernelVer
	%endif
	%ifarch ppc
	cp -f vmlinux %{temp_boot}/vmlinuz-$KernelVer
	%endif
	%ifarch %{ix86}
	cp -f arch/i386/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
	%endif
	%ifarch x86_64
	cp -f arch/x86_64/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
	%endif
	%ifarch powerpc
	cp -f vmlinux %{temp_boot}/vmlinuz-$KernelVer
	%endif

	# modules
	install -d %{temp_modules}/$KernelVer
	%smake INSTALL_MOD_PATH=%{temp_root} KERNELRELEASE=$KernelVer modules_install 
}

SaveHeaders() {
	flavour=$1
	flavour_name="`echo $flavour | sed 's/-/_/g'`"
%if %build_source
	HeadersRoot=%{temp_source}/savedheaders
	HeadersArch=$HeadersRoot/%{target_cpu}/$flavour
	echo "Saving hearders for $flavour %{target_cpu}"

	# deal with the kernel headers that are version specific
	install -d $HeadersArch
	install -m 644 include/linux/autoconf.h $HeadersArch/autoconf.h
	install -m 644 include/linux/version.h $HeadersArch/version.h
	install -m 644 include/linux/utsrelease.h $HeadersArch/utsrelease.h
    	echo "%{target_cpu} $flavour_name %{_savedheaders}%{target_cpu}/$flavour/" >> $HeadersRoot/list
%endif
}

CreateFiles() {
	kernversion=$1
	output=../kernel_files.$kernversion

	echo "%defattr(-,root,root)" > $output
	echo "%{_bootdir}/config-${kernversion}" >> $output
	echo "%{_bootdir}/vmlinuz-${kernversion}" >> $output
%ifarch ia64
	echo "%{_efidir}/vmlinuz-${kernversion}" >> $output
%endif
	echo "%{_bootdir}/System.map-${kernversion}" >> $output
	echo "%dir %{_modulesdir}/${kernversion}/" >> $output
	echo "%{_modulesdir}/${kernversion}/kernel" >> $output
	echo "%{_modulesdir}/${kernversion}/modules.*" >> $output
	echo "%doc README.kernel-sources" >> $output
	echo "%doc README.MandrivaLinux" >> $output
}

CreateKernel() {
	flavour=$1

	if [ "$flavour" = "up" ]; then
		KernelVer=%{buildrel}
		PrepareKernel "" %buildrpmrel
	elif [ "$flavour" = "power5" ]; then
		KernelVer=%{buildrel}p5
		PrepareKernel $flavour %{buildrpmrel}p5
	else
		KernelVer=%{buildrel}$flavour
		PrepareKernel $flavour %{buildrpmrel}$flavour
	fi

	BuildKernel $KernelVer
	SaveHeaders $flavour
        CreateFiles $KernelVer
}


CreateKernelNoName() {
	arch=$1
	nprocs=$2
	memory=$3

        name=$arch-$nprocs-$memory
	extension="%buildrpmrel-$name"

	KernelVer="%{buildrel}-$arch-$nprocs-$memory"
	PrepareKernel $name $extension
	BuildKernel $KernelVer
	SaveHeaders $name
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

%if %build_power5
CreateKernel power5
%endif

%if %build_smp
CreateKernel smp
%endif

%if %build_i586_up_1GB
CreateKernelNoName i586 up 1GB
%endif

%if %build_i686_up_4GB
CreateKernelNoName i686 up 4GB
%endif

%if %build_xbox
CreateKernel xbox
%endif

%if %build_up
CreateKernel up
%endif

# We don't make to repeat the depend code at the install phase
%if %build_source
PrepareKernel "" %{buildrpmrel}custom
# From > 2.6.13 prepare-all is deprecated and relies on include/linux/autoconf
# To have modpost and others scripts, one has to use the target scripts
%smake -s prepare
%smake -s scripts
%endif

###
### install
###
%install
install -m 644 %{SOURCE4}  .
install -m 644 %{SOURCE5}  .

cd %src_dir
# Directories definition needed for installing
%define target_source %{buildroot}/%{_kerneldir}
%define target_boot %{buildroot}%{_bootdir}
%define target_modules %{buildroot}%{_modulesdir}

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
for i in arm avr32 cris mips mips64 parisc s390 s390x sh sh64 arm26 h8300 m68knommu v850 m32r frv; do
	rm -rf %{target_source}/arch/$i
	rm -rf %{target_source}/include/asm-$i
done
# ppc needs m68k headers
rm -rf %{target_source}/arch/m68k

# remove config split dir contents
rm -rf %{target_source}/include/config/*

# other misc files
rm -f %{target_source}/{.config.old,.config.cmd,.tmp_gas_check}

pushd %{target_source}/include/linux ; {
install -m 644 %{SOURCE15} rhconfig.h
rm -rf autoconf.h version.h

# Create autoconf.h file
echo '#include <linux/rhconfig.h>' > autoconf.h
sed 's,$,autoconf.h,' %{_savedheaders}list | awk -f %{SOURCE16} >> autoconf.h

# From 2.6.18-rcX onward autoconf setup is being reworked,
# /include/linux/autoconf.h is replaced with 
# /include/config/auto.conf and several other changes...
# FIXME: For now use autoconf.h to create auto.conf
grep '#' autoconf.h >>../config/auto.conf

# Create version.h
echo "#include <linux/rhconfig.h>" > version.h
loop_cnt=0
for i in up smp secure i686-up-4GB i686-up-1GB i686-smp-1GB i586-up-1GB power5; do
	if [ -d %{_savedheaders}%{target_cpu}/$i -a \
	     -f %{_savedheaders}%{target_cpu}/$i/version.h ]; then
		name=`echo $i | sed 's/-/_/g'`
		if [ $loop_cnt = 0 ]; then
      			buf="#if defined(__module__$name)"
    		else
 	     		buf="#elif defined(__module__$name)"
    		fi
		echo "$buf" >> version.h
		grep UTS_RELEASE %{_savedheaders}%{target_cpu}/$i/utsrelease.h >> version.h
		loop_cnt=$[loop_cnt + 1]
	fi
done

#write last lines
if [ $loop_cnt -eq 0 ]; then
	echo "You need to build at least one kernel"
	exit 1;
fi
echo "#else" >> version.h
echo '#define UTS_RELEASE "'%{buildrel}custom'"' >> version.h
echo "#endif" >> version.h

# From 2.6.18-rcX onward autoconf setup is being reworked,
# UTS_RELEASE defines in /include/linux/version.h
# has been moved to /include/linux/utsrelease.h
# FIXME: For now we simply duplicate the code
rm -rf utsrelease.h
cp version.h utsrelease.h

# Any of the version.h are ok, as they only differ in the first line
ls %{_savedheaders}%{target_cpu}/*/version.h | head -n 1 | xargs grep -v UTS_RELEASE >> version.h
rm -rf %{_savedheaders}
} ; popd
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
	echo $modules | xargs /sbin/modinfo \
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

%if %{build_100}
%define options_preun -a -R -S -c
%define options_post  -a -s -c
%else
%define options_preun -R
#%define options_post -C
%endif

%preun -n %{kname}-%{buildrel}
/sbin/installkernel %options_preun %{buildrel}
exit 0

%post -n %{kname}-%{buildrel}
/sbin/installkernel %options_post %{buildrel}

%postun -n %{kname}-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}


%preun -n %{kname}-smp-%{buildrel}
/sbin/installkernel %options_preun %{buildrel}smp
exit 0

%post -n %{kname}-smp-%{buildrel}
/sbin/installkernel %options_post %{buildrel}smp

%postun -n %{kname}-smp-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}smp

%preun -n %{kname}-xbox-%{buildrel}
/sbin/installkernel %options_preun %{buildrel}xbox
exit 0

%post -n %{kname}-xbox-%{buildrel}
/sbin/installkernel %options_post %{buildrel}xbox

%postun -n %{kname}-xbox-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}xbox

%preun -n %{kname}-secure-%{buildrel}
/sbin/installkernel %options_preun %{buildrel}secure
exit 0

%post -n %{kname}-secure-%{buildrel}
/sbin/installkernel %options_post %{buildrel}secure

%postun -n %{kname}-secure-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}secure


%preun -n %{kname}-i586-up-1GB-%{buildrel}
/sbin/installkernel %options_preun %{buildrel}-i586-up-1GB
exit 0

%post -n %{kname}-i586-up-1GB-%{buildrel}
/sbin/installkernel %options_post %{buildrel}-i586-up-1GB

%postun -n %{kname}-i586-up-1GB-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}-i586-up-1GB


%preun -n %{kname}-i686-up-4GB-%{buildrel}
/sbin/installkernel %options_preun %{buildrel}-i686-up-4GB
exit 0

%post -n %{kname}-i686-up-4GB-%{buildrel}
/sbin/installkernel %options_post %{buildrel}-i686-up-4GB

%postun -n %{kname}-i686-up-4GB-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}-i686-up-4GB


%preun -n %{kname}-i686-up-1GB-%{buildrel}
/sbin/installkernel %options_preun %{buildrel}-i686-up-1GB
exit 0

%post -n %{kname}-i686-up-1GB-%{buildrel}
/sbin/installkernel %options_post %{buildrel}-i686-up-1GB

%postun -n %{kname}-i686-up-1GB-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}-i686-up-1GB

%preun -n %{kname}-i686-smp-1GB-%{buildrel}
/sbin/installkernel %options_preun %{buildrel}-i686-smp-1GB
exit 0

%post -n %{kname}-i686-smp-1GB-%{buildrel}
/sbin/installkernel %options_post %{buildrel}-i686-smp-1GB

%postun -n %{kname}-i686-smp-1GB-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}-i686-smp-1GB


%preun -n %{kname}-power5-%{buildrel}
/sbin/installkernel %options_preun %{buildrel}p5
exit 0

%post -n %{kname}-power5-%{buildrel}
/sbin/installkernel %options_post %{buildrel}p5

%postun -n %{kname}-power5-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}p5


%post -n %{kname}-source-%{buildrel}
cd /usr/src
rm -f linux
ln -snf linux-%{buildrel} linux
/sbin/service kheader start 2>/dev/null >/dev/null || :
# we need to create /build only when there is a source tree.

for i in /lib/modules/%{buildrel}*; do
	if [ -d $i ]; then
		ln -sf /usr/src/linux-%{buildrel} $i/build
		ln -sf /usr/src/linux-%{buildrel} $i/source
	fi
done

%postun -n %{kname}-source-%{buildrel}
if [ -L /usr/src/linux ]; then 
    if [ -L /usr/src/linux -a `ls -l /usr/src/linux 2>/dev/null| awk '{ print $11 }'` = "linux-%{buildrel}" ]; then
	[ $1 = 0 ] && rm -f /usr/src/linux
    fi
fi
# we need to delete <modules>/build at unsinstall
for i in /lib/modules/%{buildrel}*/{build,source}; do
	if [ -L $i ]; then
		rm -f $i
	fi
done
exit 0

%post -n %{kname}-source-stripped-%{buildrel}
cd /usr/src
rm -f linux
ln -snf linux-%{buildrel} linux
/sbin/service kheader start 2>/dev/null >/dev/null || :
# we need to create /build only when there is a source tree.

for i in /lib/modules/%{buildrel}*; do
	if [ -d $i ]; then
		ln -sf /usr/src/linux-%{buildrel} $i/build
		ln -sf /usr/src/linux-%{buildrel} $i/source
	fi
done

%postun -n %{kname}-source-stripped-%{buildrel}
if [ -L /usr/src/linux ]; then 
    if [ -L /usr/src/linux -a `ls -l /usr/src/linux 2>/dev/null| awk '{ print $11 }'` = "linux-%{buildrel}" ]; then
	[ $1 = 0 ] && rm -f /usr/src/linux
    fi
fi
# we need to delete <modules>/{build,source} at unsinstall
for i in /lib/modules/%{buildrel}*/{build,source}; do
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

%if %build_xbox
%files -n %{kname}-xbox-%{buildrel} -f kernel_files.%{buildrel}xbox
%endif

%if %build_secure
%files -n %{kname}-secure-%{buildrel} -f kernel_files.%{buildrel}secure
%endif

%if %build_i586_up_1GB
%files -n %{kname}-i586-up-1GB-%{buildrel} -f kernel_files.%{buildrel}-i586-up-1GB
%endif

%if %build_i686_up_4GB
%files -n %{kname}-i686-up-4GB-%{buildrel} -f kernel_files.%{buildrel}-i686-up-4GB
%endif

%if %build_power5
%files -n %{kname}-power5-%{buildrel} -f kernel_files.%{buildrel}p5
%endif


%if %build_source
%files -n %{kname}-source-%{buildrel}
%defattr(-,root,root)
%dir %{_kerneldir}
%dir %{_kerneldir}/arch
%dir %{_kerneldir}/include
%{_kerneldir}/.config
%{_kerneldir}/.gitignore
%{_kerneldir}/.mailmap
%{_kerneldir}/.missing-syscalls.d
%{_kerneldir}/Kbuild
%{_kerneldir}/COPYING
%{_kerneldir}/CREDITS
%{_kerneldir}/Documentation
%{_kerneldir}/MAINTAINERS
%{_kerneldir}/Makefile
%{_kerneldir}/README
%{_kerneldir}/REPORTING-BUGS
%{_kerneldir}/arch/alpha
%{_kerneldir}/arch/i386
%{_kerneldir}/arch/ia64
%{_kerneldir}/arch/ppc
%{_kerneldir}/arch/powerpc
%{_kerneldir}/arch/sparc
%{_kerneldir}/arch/sparc64
%{_kerneldir}/arch/x86_64
%{_kerneldir}/arch/xtensa
%{_kerneldir}/arch/um
%{_kerneldir}/arch/blackfin
%{_kerneldir}/block
%{_kerneldir}/crypto
%{_kerneldir}/drivers
%{_kerneldir}/fs
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
%{_kerneldir}/include/Kbuild
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm
%{_kerneldir}/include/asm-alpha
%{_kerneldir}/include/asm-generic
%{_kerneldir}/include/asm-i386
%{_kerneldir}/include/asm-ia64
# This is needed by ppc
%{_kerneldir}/include/asm-m68k
%{_kerneldir}/include/asm-ppc
%{_kerneldir}/include/asm-powerpc
%{_kerneldir}/include/asm-sparc
%{_kerneldir}/include/asm-sparc64
%{_kerneldir}/include/asm-x86_64
%{_kerneldir}/include/asm-xtensa
%{_kerneldir}/include/asm-um
%{_kerneldir}/include/asm-blackfin
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
%doc README.kernel-sources
%doc README.MandrivaLinux

# source-stripped
%files -n %{kname}-source-stripped-%{buildrel}
%defattr(-,root,root)
%dir %{_kerneldir}
%dir %{_kerneldir}/arch
%dir %{_kerneldir}/include
%{_kerneldir}/.config
%{_kerneldir}/COPYING
%{_kerneldir}/CREDITS
%{_kerneldir}/Documentation
%{_kerneldir}/MAINTAINERS
%{_kerneldir}/Makefile
%{_kerneldir}/README
%{_kerneldir}/REPORTING-BUGS
%{_kerneldir}/arch/alpha
%{_kerneldir}/arch/i386
%{_kerneldir}/arch/ia64
%{_kerneldir}/arch/ppc
%{_kerneldir}/arch/powerpc
%{_kerneldir}/arch/sparc
%{_kerneldir}/arch/sparc64
%{_kerneldir}/arch/x86_64
%{_kerneldir}/arch/um
%{_kerneldir}/drivers/char
%{_kerneldir}/drivers/scsi
%{_kerneldir}/scripts
%{_kerneldir}/usr
%{_kerneldir}/include/Kbuild
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm
%{_kerneldir}/include/asm-alpha
%{_kerneldir}/include/asm-generic
%{_kerneldir}/include/asm-i386
%{_kerneldir}/include/asm-ia64
# This is needed by ppc
%{_kerneldir}/include/asm-m68k
%{_kerneldir}/include/asm-ppc
%{_kerneldir}/include/asm-powerpc
%{_kerneldir}/include/asm-sparc
%{_kerneldir}/include/asm-sparc64
%{_kerneldir}/include/asm-x86_64
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
%{_kerneldir}/include/rxrpc
%doc README.kernel-sources
%doc README.MandrivaLinux
#endif %build_source
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

%if %build_secure
%files -n %{kname}-secure-latest
%defattr(-,root,root)
%endif

%if %build_xbox
%files -n %{kname}-xbox-latest
%defattr(-,root,root)
%endif

%if %build_i586_up_1GB
%files -n %{kname}-i586-up-1GB-latest
%defattr(-,root,root)
%endif

%if %build_i686_up_4GB
%files -n %{kname}-i686-up-4GB-latest
%defattr(-,root,root)
%endif

#%if %build_i686_up_1GB
#%files -n %{kname}-i686-up-1GB-latest
#%defattr(-,root,root)
#%endif

%if %build_power5
%files -n %{kname}-power5-latest
%defattr(-,root,root)
%endif

%if %build_source
%files -n %{kname}-source-latest
%defattr(-,root,root)
%endif

%if %build_source
%files -n %{kname}-source-stripped-latest
%defattr(-,root,root)
%endif

%if %build_doc
%files -n %{kname}-doc-latest
%defattr(-,root,root)
%endif


