Summary:	Multiplayer roguelike game server.
Name:		crossfire
Version:	0.95.8
Release:	1
License:	GPL
Group:		Applications/Games
Source0:	ftp://ftp.scruz.net/users/mwedel/public/%{name}-%{version}.tar.bz2
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-crossloop.patch
URL:		http://crossfire.real-time.com
BuildRequires:	XFree86-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix	/usr/X11R6
%define		_localstatedir /var/lib

%description 
This is a multiplayer graphical arcade and adventure game made for the
X-Windows environment. There are also Windows and Java clients
available.

It has certain flavours from other games, especially Gauntlet (TM) and
Nethack/Moria.

Any number of players can move around in their own window, finding and
sing items and battle monsters. They can choose to cooperate or
compete in the same "world".

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/log/crossfire,/etc/sysconfig,/etc/rc.d/init.d}
%{__make} install DESTDIR="$RPM_BUILD_ROOT"
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

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
%attr(750,root,games) %{_bindir}/crossfire
%attr(750,root,games) %{_bindir}/random_map
%attr(750,root,games) %{_bindir}/crossloop
%attr(755,root,root) %{_bindir}/crossedit
%dir %attr(750,root,games) %{_datadir}/crossfire
%{_datadir}/crossfire/*
%{_mandir}/man?/*
%dir %attr(750,root,games) %{_localstatedir}/crossfire
%attr(770,root,games) %{_localstatedir}/crossfire/players
%attr(770,root,games) %{_localstatedir}/crossfire/unique-items
%attr(660,root,games) %{_localstatedir}/crossfire/bookarch
%attr(660,root,games) %{_localstatedir}/crossfire/highscore
%attr(660,root,games) %{_localstatedir}/crossfire/temp.maps
%attr(770,root,games) /var/log/crossfire

%attr(754,root,root) /etc/rc.d/init.d/crossfire
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/crossfire
