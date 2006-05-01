# TODO
# - CVE-2006-1010 http://security.gentoo.org/glsa/glsa-200604-11.xml
Summary:	Multiplayer roguelike game server
Summary(pl):	Serwer gry roguelike dla wielu graczy
Name:		crossfire
Version:	1.6.0
Release:	2
License:	GPL
Group:		Applications/Games
Source0:	http://dl.sourceforge.net/crossfire/%{name}-%{version}.tar.gz
# Source0-md5:	cac617806c2430821f8bd918726a66e1
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Patch0:		%{name}-python2.3.patch
URL:		http://crossfire.real-time.com/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	crossfire-maps
Requires:	rc-scripts
%pyrequires_eq  python
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

%description -l pl
To jest graficzna gra przygodowa dla ¶rodowiska X-Window. S± tak¿e
dostêpni klienci pod Windows i w Javie.

%package editor
Summary:	Crossfire map editor
Summary(pl):	Edytor map Crossfire
Group:		Applications/Games

%description editor
Crossfire map editor.

%description editor -l pl
Edytor map Crossfire.

%package doc
Summary:	Crossfire game documentation
Summary(pl):	Dokumentacja gry Crossfire
Group:		Documentation

%description doc
Crossfire documentation for players. Includes handbook and spoiler.

%description doc -l pl
Dokumentacja dla graczy Crossfire. Zawiera podrêcznik oraz spoiler.

%package plugin-python
Summary:	Python plugin for Crossfire server
Summary(pl):	Wtyczka Pythona dla serwera Crossfire
Group:		Applications/Games
Requires:	%{name} = %{version}-%{release}

%description plugin-python
Python plugin for Crossfire server.

%description plugin-python -l pl
Wtyczka Pythona dla serwera Crossfire.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/log,/etc/{sysconfig,%{name},logrotate.d},/etc/rc.d/init.d} \
	$RPM_BUILD_ROOT%{_localstatedir}/%{name}/{tmp,maps}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/crossfire/plugins/plugin_python.a
rm $RPM_BUILD_ROOT%{_bindir}/crossloop*
rm $RPM_BUILD_ROOT%{_mandir}/*/crossloop*
rm $RPM_BUILD_ROOT%{_bindir}/player_dl.pl
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
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
%doc DEVELOPERS README TODO ChangeLog
%doc doc/{alchemy.doc,experience,metaserver,multigod,plugins}
%attr(750,root,games) %{_bindir}/crossfire
%attr(755,root,games) %{_bindir}/crossfire-config
%dir %attr(750,root,games) %{_datadir}/crossfire
%{_datadir}/crossfire/*
%{_mandir}/man?/crossfire*
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
%attr(755,root,root) %{_libdir}/crossfire/add_throw.perl
%attr(755,root,root) %{_libdir}/crossfire/metaserver.pl
%attr(755,root,root) %{_libdir}/crossfire/mktable.script
%attr(755,root,root) %{_libdir}/crossfire/random_map

%files editor
%defattr(644,root,root,755)
%doc crossedit/doc/*.doc
%attr(755,root,root) %{_bindir}/crossedit
%{_mandir}/man?/crossedit*

%files doc
%defattr(644,root,root,755)
%doc doc/{handbook.ps,spoiler.ps}
%doc doc/{PlayerStats,RunTimeCommands,SurvivalGuide}
%doc doc/{skills.doc,spellcasters_guide_to_runes}
%doc doc/spell-docs/{*.txt,spell-list.ps,spell-summary.ps}

%files plugin-python
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/crossfire/plugins/plugin_python.*
