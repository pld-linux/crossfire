Summary:	Multiplayer roguelike game server
Summary(pl):	Serwer gry roguelike dla wielu graczy
Name:		crossfire
Version:	1.5.0
Release:	2
Group:		Applications/Games
License:	GPL
Source0:	http://dl.sourceforge.net/crossfire/%{name}-%{version}.tar.gz
# Source0-md5:	b22556499a1aa99a19e6c5c7b33d501f
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Patch0:		%{name}-perlpath.patch
URL:		http://crossfire.real-time.com/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	python-devel >= 2.3
Requires(post,preun):	/sbin/chkconfig
Requires:	crossfire-maps
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
Summary(pl):	Edytor map crossfire
Group:		Applications/Games

%description editor
Crossfire map editor.

%description editor -l pl
Edytor map crossfire.

%package doc
Summary:	Crossfire game documentation
Summary(pl):	Dokumentacja gry crossfire
Group:		Applications/Games

%description doc
Crossfire documentation for players. Includes handbook and spoiler.

%description doc -l pl
Dokumentacja dla graczy Crossfire. Zawiera podrêczniek oraz spoiler.

%package plugin-python
Summary:	python plugin for crossfire server
Group:		Applications/Games
Requires:	%{name} = %{version}

%description plugin-python
Python plugin for crossfire server.

%prep
%setup -q
%patch0 -p1

%build
%{__autoconf}
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
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
touch $RPM_BUILD_ROOT/var/log/crossfire

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add crossfire
if [ -r /var/lock/subsys/crossfire ]; then
	/etc/rc.d/init.d/crossfire restart >&2
else
	echo "Run \"/etc/rc.d/init.d/crossfire start\" to start Crossfire server."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/crossfire ]; then
		/etc/rc.d/init.d/crossfire stop >&2
	fi
	/sbin/chkconfig --del crossfire
fi

%files
%defattr(644,root,root,755)
%doc DEVELOPERS README TODO
%doc doc/{alchemy.doc,experience,multigod,spell_params.doc}
%doc doc/{spell-paths,spellcasters_guide_to_runes,metaserver}
%doc doc/Developers utils/crossloop{,.web,.pl}
%attr(750,root,games) %{_bindir}/crossfire
%attr(755,root,games) %{_bindir}/crossfire-config
%dir %attr(750,root,games) %{_datadir}/crossfire
%{_datadir}/crossfire/*
%{_mandir}/man?/crossfire*
%dir %attr(750,root,games) %{_localstatedir}/crossfire
%dir %attr(770,root,games) %{_localstatedir}/crossfire/players
%dir %attr(770,root,games) %{_localstatedir}/crossfire/unique-items
%dir %attr(770,root,games) %{_localstatedir}/crossfire/tmp
%dir %attr(770,root,games) %{_localstatedir}/crossfire/maps
%attr(660,root,games) %config(noreplace) %verify(not size mtime md5) %{_localstatedir}/crossfire/bookarch
%attr(660,root,games) %config(noreplace) %verify(not size mtime md5) %{_localstatedir}/crossfire/highscore
%attr(660,root,games) %config(noreplace) %verify(not size mtime md5) %{_localstatedir}/crossfire/temp.maps
%attr(660,root,games) %config(noreplace) %verify(not size mtime md5) %{_localstatedir}/crossfire/clockdata
%dir /etc/crossfire
%config(noreplace) %verify(not size mtime md5) /etc/crossfire/*
%attr(754,root,root) /etc/rc.d/init.d/crossfire
%attr(660,root,root) /etc/logrotate.d/crossfire
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/crossfire
%attr(660,root,games) %config(noreplace) %verify(not size mtime md5) /var/log/crossfire
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
%doc doc/{skills.doc,spellcasters_guide_to_runes,spells*}

%files plugin-python
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/crossfire/plugins/plugin_python.*
