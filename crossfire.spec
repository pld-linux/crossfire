Summary:	Multiplayer roguelike game server
Summary(pl):	Serwer gry roguelike dla wielu graczy
Name:		crossfire
Version:	1.0.0
Release:	1
License:	GPL
Group:		Applications/Games
Source0:	ftp://ftp.scruz.net/users/mwedel/public/%{name}-%{version}.tar.bz2
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-directories.patch
Patch2:		%{name}-tmp_maps.patch
URL:		http://crossfire.real-time.com
BuildRequires:	XFree86-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Prereq:		/sbin/chkconfig

%define		_prefix	/usr/X11R6
%define		_localstatedir /var/lib

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
Group(de):	Applikationen/Spiele
Group(pl):	Aplikacje/Gry

%description editor
Crossfire map editor.

%description editor -l pl
Edytor map crossfire.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/log,/etc/{sysconfig,%{name},logrotate.d},/etc/rc.d/init.d}
install -d $RPM_BUILD_ROOT%{_localstatedir}/%{name}/tmp
%{__make} install DESTDIR="$RPM_BUILD_ROOT"
mv -f $RPM_BUILD_ROOT%{_datadir}/%{name}/{ban_file,settings,dm_file,motd,forbid} \
	$RPM_BUILD_ROOT/etc/%{name}
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
%doc CHANGES CREDITS DEVELOPERS DONE README TODO 
%doc doc/{PlayerStats,RunTimeCommands,SurvivalGuide,alchemy.doc,experience,multigod}
%doc doc/{skills.doc,spell-paths,spellcasters_guide_to_runes,spells}
%attr(750,root,games) %{_bindir}/crossfire
%attr(750,root,games) %{_bindir}/random_map
%dir %attr(750,root,games) %{_datadir}/crossfire
%{_datadir}/crossfire/*
%{_mandir}/man?/crossfire*
%dir %attr(750,root,games) %{_localstatedir}/crossfire
%dir %attr(770,root,games) %{_localstatedir}/crossfire/players
%dir %attr(770,root,games) %{_localstatedir}/crossfire/unique-items
%dir %attr(770,root,games) %{_localstatedir}/crossfire/tmp
%attr(660,root,games) %config(noreplace) %verify(not size mtime md5) %{_localstatedir}/crossfire/bookarch
%attr(660,root,games) %config(noreplace) %verify(not size mtime md5) %{_localstatedir}/crossfire/highscore
%attr(660,root,games) %config(noreplace) %verify(not size mtime md5) %{_localstatedir}/crossfire/temp.maps
%dir /etc/crossfire
%config(noreplace) %verify(not size mtime md5) /etc/crossfire/*
%attr(754,root,root) /etc/rc.d/init.d/crossfire
%attr(660,root,root) /etc/logrotate.d/crossfire
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/crossfire
%attr(660,root,games) %config(noreplace) %verify(not size mtime md5) /var/log/crossfire

%files editor
%defattr(644,root,root,755)
%doc doc/{Crossedit.doc,RandomMaps.doc,Styles.doc,mapguide,mapmakers_guide_to_runes,teleporter.doc}
%attr(755,root,root) %{_bindir}/crossedit
%{_mandir}/man?/crossedit*
