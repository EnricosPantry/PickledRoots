# Keyboard layout reverts to US

*Written 29/04/2024. Arch Linux, Xorg, Qtile window manager.*

## The problem

My keyboard layout changes from US (default) to UK at boot; it is triggered by the command `setxkbmap -layout gb` within the `.xinitrc` file.

Ever since I can remember, I've had problems with this. The keyboard seemed to switch back to the default US on its own during boot, and it seemed to be *random*; when I boot the laptop one day, the GB layout loads correctly; another day it doesn't.

I've tried to change the order in which the `.xinitrc` commands were executed, putting the keyboard command first on the line, then last on the line even after loading the WM, and then just before the WM startup command; nothing worked permanently, and as it seemed to happen infrequently and didn't bother me too much, the problem was unsolved for the longest time.

### A clue

Today I finally understood that the switching back is not random at all. I've had to unplug my external monitor, and after connecting it back, the keyboard layout switched.

It seemed to be related to the monitor somehow; how could this be?

I've done some research and found a *Reddit post* that links to some resources in the *Arch Wiki*, and after reading it all, I finally got it.

> In order to check current keyboard settings, the command `setxkbmap -print -verbose 10` can be run.

## The solution

When HDMI is connected, the device is loaded, and somehow other devices are unloaded and reloaded too, including the keyboard.

The layout kept being changed because the device was being reloaded as if it was unplugged and plugged back in. After this operation, a new command would need to be issued to change the layout back to GB, but it was not, as `.xinitrc` only runs once at initial boot.

This caused it to revert back to the US layout even on boot whenever an external monitor was plugged in (and it was most of the time). It seemed random, though, because sometimes the monitor would be loaded before, and sometimes after, the `.xinitrc` command.

Reading the *Arch Wiki* page, this is actually mentioned very briefly in the xinitrc section.

Since there are multiple methods to set up settings for the keyboard, I simply used another one, and that worked.

### What I did to make it work

I've created an Xorg configuration file in `/etc/X11/xorg.conf.d/` named `00-keyboard.conf` with the following content:

```
Section "InputClass"
	Identifier "system-keyboard"
	MatchIsKeyboard "on"
	Option "XkbLayout" "gb,it"
	Option "XkbOptions" "grp:win_space_toggle"
EndSection
```

This sets the *default layout* of my keyboard to *GB* and sets the *secondary layout* to *IT*. It also adds the *keybinding win+space* to *toggle between layouts*.

I've removed the `setxkbmap` command from `.xinitrc`. I've also unplugged and plugged the HDMI monitor several times and rebooted; the problem seems to be completely resolved, finally.

## Sources

- [My keyboard layout automatically changes - reddit](https://www.reddit.com/r/archlinux/comments/14wjhfk/my_keyboard_layout_automatically_changes/)
- [Keyboard configuration - Arch Wiki](https://wiki.archlinux.org/title/Xorg/Keyboard_configuration#Using_X_configuration_files)
