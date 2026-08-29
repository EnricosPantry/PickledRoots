#!/bin/bash


##################################################################
### CODE TAKEN FROM DEFAULT .xinitrc IN /etc/X11/xinit/xinitrc ###
##################################################################


### NOT ESSENTIAL BUT COPIED ANYWAYS

userresources=$HOME/.Xresources
usermodmap=$HOME/.Xmodmap
sysresources=/etc/X11/xinit/.Xresources
sysmodmap=/etc/X11/xinit/.Xmodmap

# merge in defaults and keymaps

if [ -f $sysresources ]; then







    xrdb -merge $sysresources

fi

if [ -f $sysmodmap ]; then
    xmodmap $sysmodmap
fi

if [ -f "$userresources" ]; then







    xrdb -merge "$userresources"

fi

if [ -f "$usermodmap" ]; then
    xmodmap "$usermodmap"
fi


### ESSENTIAL AS DESCRIBED IN THE XINIT ARCH WIKI
##  start some nice programs

if [ -d /etc/X11/xinit/xinitrc.d ] ; then
 for f in /etc/X11/xinit/xinitrc.d/?*.sh ; do
  [ -x "$f" ] && . "$f"
 done
 unset f
fi


###########################################
### CODE THAT I WROTE, NO LONGER IN USE ###
###########################################


#Prevent file manager from starting with 25s delay:
#dbus-update-activation-environment --systemd DBUS_SESSION_BUS_ADDRESS DISPLAY XAUTHORITY
#NO LONGER NEEDED, problem solved by removing xdg-desktop-portal-gnome package, which is broken

#Map wacom tablet to native monitor
#xsetwacom set 'Wacom One by Wacom S Pen stylus' MapToOutput eDP1 &
#xsetwacom set 'Wacom One by Wacom S Pen eraser' MapToOutput eDP1 &

#Start insync, Google Drive client - UNINSTALLED
#insync start &


#################################
### CODE THAT I WROTE, IN USE ###
#################################


### SETS WALLPAPER AND START VARIETY

# /usr/bin/nitrogen --restore &
# /usr/bin/variety &
# 
# INFO: moved code lower in the list
# starting Variety and Nitrogen later in the boot process
# prevents WM from loading without backgroud when HDMI
# cable is connected before startup


### STARTS VARIETY

/usr/bin/variety &


### START NETWORK MANAGER APPLET

/usr/bin/nm-applet --indicator &


### START GRAPHICS

/usr/bin/picom &
/usr/bin/unclutter --jitter 10 --ignore-scrolling --start-hidden --fork
/usr/bin/dunst &


### START POLKIT AUTHENTICATION AGENT

/usr/bin/lxpolkit &


### DETECT DISPLAYS, UPDATE RESOLUTION AND TOUCHSCREEN
## First update resolution, then map touchscreen surface to native monitor

/usr/bin/autorandr -c
/usr/bin/xinput --map-to-output 'ELAN901C:00 04F3:2C4E' eDP1 &


### STARTS KEYRING AND SECRETS
## Can be placed before or after qtile start, needed for GIT integration, packages: gnome-keyring, libsecret

dbus-update-activation-environment --all
/usr/bin/gnome-keyring-daemon --start --components=secrets


### STARTS SCREEN BLANKING MANAGEMENT SCRIPT

/usr/local/bin/NoBlanking &


## RESTORES WALLPAPER

/usr/bin/nitrogen --restore &


### START QTILE WINDOW MANAGER

qtile start

