# Bad behaviour: wrong system time after change to BST

*Written 02/04/2024, with a related problem added 15/05/2024. Arch Linux and Windows 11 dual-boot, Qtile window manager.*

## What happened

I am currently using a dual-boot system with Windows 11 and Arch Linux. I've installed Windows first on this machine, and Arch after, as recommended in the Arch Wiki.

I've also enabled automatic timezone in Arch Linux whenever the computer connects to a network. I followed the instructions on the Arch Wiki page System Time to do so.

After the change this year to BST (one hour forward) on the 31st of March, the time displayed in the Qtile bar skipped automatically forward by 2 hours instead of one. When checking `timedatectl` the timezone is correct, and all seems to be working fine.

## How to fix it

I've found out by reading the System time page that it is recommended to set Windows to UTC when dual-booting. This needs to be changed from a fresh install, as Windows is automatically set to local time.
This is a problem because when Windows writes the local time to the hardware clock, Linux then reads it as if it were UTC. When the time changes in summer, the +1 offset gets written to the RTC by Windows; it then gets read as UTC by Linux, which then applies a second offset of +1, resulting in a 2-hour offset.

To change Windows time to UTC on an existing install, press `WIN+R` and type `regedit` to enter the registry editor, navigate to `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\TimeZoneInformation` and add a DWORD value named `RealTimeIsUniversal`, then set the hexadecimal value to 1.

Now right-click the time on the taskbar at the bottom right and click on "Adjust date & time". A settings page will pop up. Scroll down and click on the "Sync now" button, which will update the date and time.

Reboot into Linux, and the time should have adjusted itself. Otherwise, set the timezone again using:

```bash
timedatectl set-timezone Europe/London
```

In my case, I didn't need to do that, and the time was displayed correctly as soon as I rebooted into Linux.

## A similar problem: the Qtile clock widget showing UTC

*15/05/2024.*

Whenever I travel back home, the time changes by 1 hour as my timezone changes from London to Rome. The system local time is changed automatically whenever NetworkManager connects to a network, thanks to a NetworkManager dispatcher script I created by following the instructions in the Arch Wiki page linked below. Remember that the executable bit needs to be set on the script for it to work.

The issue is that the Qtile clock widget displays Universal Time and not local time; therefore, any update performed when the timezone changes is not shown.

After researching, I found a thread on the Qtile GitHub page, linked below, with a code snippet said to make the clock widget timezone-aware. There are no instructions on where to place the code, but after testing by pasting it into my `config.py` file, it definitely works. The system has to be rebooted, or Qtile restarted, for timezone changes to show.

## Sources

- [System time, UTC in Microsoft Windows - Arch Wiki](https://wiki.archlinux.org/title/System_time#UTC_in_Microsoft_Windows)
- [System time, setting based on geolocation - Arch Wiki](https://wiki.archlinux.org/title/System_time#Setting_based_on_geolocation)
- [System time, update timezone every time NetworkManager connects to a network - Arch Wiki](https://wiki.archlinux.org/title/System_time#Update_timezone_every_time_NetworkManager_connects_to_a_network)
- [Make the clock widget timezone-aware - Qtile GitHub](https://github.com/qtile/qtile/issues/1170)
