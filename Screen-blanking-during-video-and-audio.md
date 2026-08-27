# Screen blanking while playing videos and music

*Written 29/04/2024. Arch Linux, Xorg, Qtile window manager, PulseAudio.*

## What was going on

The screen has always been turning off automatically after a while, due to power settings.

This becomes a problem when I am listening to music on the laptop, and I am connected to my HDMI external monitor, which the speakers connect to. When the screen turns off, the speakers do too.

## The solution

I found an idea for the solution in a post on the Arch forum asking how to prevent screen blanking (the screen turning off).

The idea is to write a script that detects when audio is being played and simulates keystrokes in the background in order to prevent blanking.

This is the implementation that was suggested in the forum:

```bash
#!/bin/bash

while true; do
  sleep 30
  RUNNING=$(pacmd list-sink-inputs  | grep -w state | grep RUNNING)
  if [ -n "${RUNNING}" ]; then
    xdotool key shift
  fi
done
```

However, I've asked ChatGPT to write a script for me, compared the two, and decided to do some testing on my own and write a simpler script myself.

I was using the Shift key initially, and having it pressed down for one second every 5 seconds. The problem is that this makes writing very difficult, as I was getting capital letters even when I didn't want to.

So I decided that the solution would be to switch to the Meta key instead. Since my keyboard has a Windows key rather than a Meta key, I didn't know if it would work, so I decided to run some tests. 

### How I tested the solution

The way I tested the Meta key is by running the following:

```bash
sleep 10 && xdotool key meta &
```

This simulates a keystroke in 10 seconds and sends the command to the background, so that the terminal is free to run another command:

```bash
xset dpms force off
```

This forces activation of screen blanking.

After the screen has been turned off, I found out it reactivates after a few seconds, meaning the delayed Meta keystroke worked and had the effect of turning the screen back on, preventing screen blanking.

### Writing the final script

I decided to change the frequency of the simulated keystroke to every 60 seconds, as it makes no difference to the blanking timer.

This is the final script I wrote myself:

```bash
#!/bin/bash

while true;
do
   if
      pacmd list-sink-inputs | grep -q "state: RUNNING";
   then
      xdotool key meta
   fi
sleep 60
done
```

The last thing I did was to save the script with the name `NoBlanking` and add the command `/usr/local/bin/NoBlanking &` to `.xinitrc`, so that the script is activated after logging in and runs continuously in the background as long as Xorg is active.

## Sources

- [Disable turn off screen while youtube is watching - Arch forum](https://bbs.archlinux.org/viewtopic.php?id=148267)
- [Display Power Management Signaling - Arch Wiki](https://wiki.archlinux.org/title/Display_Power_Management_Signaling)
