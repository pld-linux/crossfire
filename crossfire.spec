Summary:	Multiplayer roguelike game server
Summary(pl.UTF-8):	Serwer gry roguelike dla wielu graczy
Name:		crossfire
Version:	1.75.0
Release:	4
License:	GPL v2+
Group:		X11/Applications/Games
Source0:	https://downloads.sourceforge.net/crossfire/%{name}-%{version}.tar.gz
# Source0-md5:	7d2e39294056ad521f603dfc31c2cf7f
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Patch0:		python3.patch
Patch1:		%{name}-python3.patch
URL:		https://crossfire.real-time.com/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	check
BuildRequires:	cproto
BuildRequires:	libtool
BuildRequires:	python3-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXt-devel
Requires(post,preun):	/sbin/chkconfig
%pyrequires_eq	python3
Requires:	crossfire-maps
Requires:	rc-scripts
Conflicts:	logrotate < 3.8.0
Obsoletes:	crossfire-editor < 1.75.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_localstatedir	/var/lib

%description
This is a multiplayer graphical arcade and adventure game made for the
X-Window environment. There are also Windows and Java clients
available.

It has certain flavours from other games, especially Gauntlet (TM) and
Nethack/Moria.

Any number of players can move around in their own window, finding and
sing items and battle monsters. They can choose to cooperate or
compete in the same "world".

%description -l pl.UTF-8
To jest graficzna gra przygodowa dla środowiska X-Window. Są także
dostępni klienci pod Windows i w Javie.

%package editor
Summary:	Crossfire map editor
Summary(pl.UTF-8):	Edytor map Crossfire
Group:		X11/Applications/Games

%description editor
Crossfire map editor.

%description editor -l pl.UTF-8
Edytor map Crossfire.

%package doc
Summary:	Crossfire game documentation
Summary(pl.UTF-8):	Dokumentacja gry Crossfire
Group:		Documentation

%description doc
Crossfire documentation for players. Includes handbook and spoiler.

%description doc -l pl.UTF-8
Dokumentacja dla graczy Crossfire. Zawiera podręcznik oraz spoiler.

%package plugin-python
Summary:	Python plugin for Crossfire server
Summary(pl.UTF-8):	Wtyczka Pythona dla serwera Crossfire
Group:		X11/Applications/Games
Requires:	%{name} = %{version}-%{release}

%description plugin-python
Python plugin for Crossfire server.

%description plugin-python -l pl.UTF-8
Wtyczka Pythona dla serwera Crossfire.

%package plugin-anim
Summary:	Animation plugin for Crossfire server
Summary(pl.UTF-8):	Wtyczka animacji dla serwera Crossfire
Group:		X11/Applications/Games
Requires:	%{name} = %{version}-%{release}

%description plugin-anim
Animation plugin for Crossfire server.

%description plugin-anim -l pl.UTF-8
Wtyczka animacji dla serwera Crossfire.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
      utils/cfdb_convert

%build
%configure \
	PYTHON=%{__python3} \
	PYTHON_LIBS="`python3-config --libs --embed`" \
	--disable-static

%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/log,/etc/{sysconfig,%{name},logrotate.d},/etc/rc.d/init.d} \
	$RPM_BUILD_ROOT%{_localstatedir}/%{name}/{tmp,maps}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/crossfire/plugins/*.la
%{__rm} $RPM_BUILD_ROOT%{_bindir}/crossloop*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man6/crossloop*.6*
%{__rm} $RPM_BUILD_ROOT%{_bindir}/player_dl.pl
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
touch $RPM_BUILD_ROOT/var/log/crossfire

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add crossfire
%service crossfire restart "Crossfire server"

%preun
if [ "$1" = "0" ]; then
	%service crossfire stop
	/sbin/chkconfig --del crossfire
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README.rst ChangeLog
%attr(750,root,games) %{_bindir}/crossfire-server
%attr(755,root,games) %{_bindir}/cfdb_convert
%dir %attr(750,root,games) %{_datadir}/crossfire
%{_datadir}/crossfire/animations
%{_datadir}/crossfire/archetypes
%{_datadir}/crossfire/artifacts
%{_datadir}/crossfire/attackmess
%{_datadir}/crossfire/bmaps.paths
%{_datadir}/crossfire/crossfire.*
%{_datadir}/crossfire/def_help
%{_datadir}/crossfire/faces
%{_datadir}/crossfire/formulae
%{_datadir}/crossfire/image_info
%{_datadir}/crossfire/materials
%{_datadir}/crossfire/messages
%{_datadir}/crossfire/races
%{_datadir}/crossfire/smooth
%{_datadir}/crossfire/treasures
%{_datadir}/crossfire/adm
%dir %{_datadir}/crossfire/help
%{_datadir}/crossfire/help/*.en
%lang(fr) %{_datadir}/crossfire/help/*.fr
%dir %{_datadir}/crossfire/i18n
%{_datadir}/crossfire/i18n/*.en
%lang(fr) %{_datadir}/crossfire/i18n/*.fr
%dir %{_datadir}/crossfire/wizhelp
%{_datadir}/crossfire/wizhelp/*.en
%lang(fr) %{_datadir}/crossfire/wizhelp/*.fr
%{_mandir}/man6/crossfire-server.6*
%dir %attr(770,root,games) %{_localstatedir}/crossfire
%dir %attr(770,root,games) %{_localstatedir}/crossfire/players
%dir %attr(770,root,games) %{_localstatedir}/crossfire/unique-items
%dir %attr(770,root,games) %{_localstatedir}/crossfire/tmp
%dir %attr(770,root,games) %{_localstatedir}/crossfire/maps
%attr(660,root,games) %config(noreplace) %verify(not md5 mtime size) %{_localstatedir}/crossfire/bookarch
%attr(660,root,games) %config(noreplace) %verify(not md5 mtime size) %{_localstatedir}/crossfire/highscore
%attr(660,root,games) %config(noreplace) %verify(not md5 mtime size) %{_localstatedir}/crossfire/temp.maps
%attr(660,root,games) %config(noreplace) %verify(not md5 mtime size) %{_localstatedir}/crossfire/clockdata
%attr(660,root,games) %config(noreplace) %verify(not md5 mtime size) %{_localstatedir}/crossfire/banish_file
%dir %{_sysconfdir}/crossfire
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/crossfire/*
%attr(754,root,root) /etc/rc.d/init.d/crossfire
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/crossfire
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/crossfire
%attr(660,root,games) %config(noreplace) %verify(not md5 mtime size) /var/log/crossfire
%dir %{_libdir}/crossfire
%dir %{_libdir}/crossfire/plugins
%attr(755,root,root) %{_libdir}/crossfire/plugins/cfcitybell.so
%attr(755,root,root) %{_libdir}/crossfire/plugins/citylife.so
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/crossfire
%endif
%attr(755,root,root) %{_libexecdir}/crossfire/random_map

%files doc
%defattr(644,root,root,755)
%doc doc/{handbook.ps,spoiler.ps}
%doc doc/{stats.txt,commands.txt,survival-guide.txt}
%doc doc/{skills.txt,runes-guide.txt}

%files plugin-python
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/crossfire/plugins/cfpython.so

%files plugin-anim
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/crossfire/plugins/cfanim.so
