#
# Conditional build:
%bcond_with	gtk3		# GTK+ 3.x instead of 2.x
%bcond_without	jack		# JACK support
%bcond_without	pulseaudio	# PulseAudio support
%bcond_without	vaapi		# VA-API support

Summary:	PPAPI-host NPAPI-plugin adapter for flashplayer in NPAPI based browsers
Summary(pl.UTF-8):	Przejściówka hostująca wtyczki PPAPI dla flashplayera w przeglądarkach opartych na NPAPI
Name:		freshplayerplugin
Version:	0.3.4
Release:	1
License:	MIT
Group:		X11/Applications/Multimedia
Source0:	https://github.com/i-rinat/freshplayerplugin/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e5d5df12de8dbb1caf4e349b4e4ae520
URL:		https://github.com/i-rinat/freshplayerplugin
BuildRequires:	Mesa-libEGL-devel
BuildRequires:	Mesa-libGLES-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	cmake >= 2.8.8
BuildRequires:	ffmpeg-devel
BuildRequires:	freetype-devel
BuildRequires:	glib2-devel
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0}
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
BuildRequires:	libevent-devel
BuildRequires:	libv4l-devel
%{?with_vaapi:BuildRequires:	libva-devel}
BuildRequires:	libva-x11-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
BuildRequires:	ragel
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
Requires:	browser-plugins >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PPAPI-host NPAPI-plugin adapter for flashplayer in npapi based
browsers.

%description -l pl.UTF-8
Przejściówka hostująca wtyczki PPAPI (pod kątem flashplayera) w
przeglądarkach opartych na NPAPI.

%prep
%setup -q

%build
install -d build
cd build
%cmake \
	-DCMAKE_SKIP_RPATH=1 \
	%{?with_jack:-DJACK=1} \
	%{?with_pulseaudio:-DPULSEAUDIO=1} \
	-DWITH_GTK=%{!?with_gtk3:2}%{?with_gtk3:3} \
	-DWITH_HWDEC=%{!?with_vaapi:0}%{?with_vaapi:1} \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_browserpluginsdir}

install -p build/libfreshwrapper-flashplayer.so $RPM_BUILD_ROOT%{_browserpluginsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog data/freshwrapper.conf.example README.md
%attr(755,root,root) %{_browserpluginsdir}/libfreshwrapper-flashplayer.so
