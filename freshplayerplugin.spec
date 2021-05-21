#
# Conditional build:
%bcond_without	gles		# GLESv2 instead of ANGLE
%bcond_without	jack		# JACK support
%bcond_without	pulseaudio	# PulseAudio support
%bcond_without	ffmpeg		# ffmpeg with hardware acceleration (VA-API/VDPAU) support

Summary:	PPAPI-host NPAPI-plugin adapter for flashplayer in NPAPI based browsers
Summary(pl.UTF-8):	Przejściówka hostująca wtyczki PPAPI dla flashplayera w przeglądarkach opartych na NPAPI
Name:		freshplayerplugin
Version:	0.3.11
Release:	1
License:	MIT
Group:		X11/Applications/Multimedia
Source0:	https://github.com/i-rinat/freshplayerplugin/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c34383e281135b7d40e29444af189d34
URL:		https://github.com/i-rinat/freshplayerplugin
BuildRequires:	OpenGL-devel
%{?with_gles:BuildRequires:	OpenGLESv2-devel}
BuildRequires:	alsa-lib-devel
BuildRequires:	cairo-devel
BuildRequires:	cmake >= 2.8.8
# libavcodec libavutil
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel}
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	glib2-devel >= 2.0
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
BuildRequires:	libdrm-devel
BuildRequires:	libevent-devel
BuildRequires:	libicu-devel
BuildRequires:	libv4l-devel
%{?with_ffmpeg:BuildRequires:	libva-devel}
%{?with_ffmpeg:BuildRequires:	libva-x11-devel}
%{?with_ffmpeg:BuildRequires:	libvdpau-devel}
BuildRequires:	openssl-devel
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(gl)
%{?with_gles:BuildRequires:	pkgconfig(glesv2)}
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
BuildRequires:	ragel
BuildRequires:	rpmbuild(macros) >= 1.605
%{?with_jack:BuildRequires:	soxr-devel}
BuildRequires:	xorg-lib-libX11-devel
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
%cmake .. \
	-DCMAKE_SKIP_RPATH=ON \
	%{!?with_ffmpeg:-DWITH_HWDEC=OFF} \
	%{!?with_jack:-DWITH_JACK=OFF} \
	%{!?with_pulseaudio:-DWITH_PULSEAUDIO=OFF}

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
%doc ChangeLog LICENSE README.md data/freshwrapper.conf.example
%attr(755,root,root) %{_browserpluginsdir}/libfreshwrapper-flashplayer.so
