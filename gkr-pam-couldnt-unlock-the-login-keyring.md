# gkr-pam: couldn't unlock the login keyring

*Written 18/07/2024. Arch Linux, ly display manager, gnome-keyring.*

## What is this error

This is, and has been, one of the errors that comes up whenever I run `journalctl -b -p3`. I've been having this error for the longest time and tried to fix it without success several times.

I know this is related to the ly display manager, as the full error text that comes up is the following:

```
Jul 18 00:26:40 wasabi ly-dm[1462]: gkr-pam: couldn't unlock the login keyring.
```

I thought it was an issue because it was showing up in journalctl. However, it never actually created any problems aside from being flagged at boot. The keyring always worked fine, and therefore this has been left as one of the few innocuous error messages that just show up because they show up.

## The real cause and solution

This error didn't have a solution until a few weeks ago. I've noticed ly graphics are marginally different, so ly has been updated, and when checking the journal, one fewer error message showed up. 
Didn't think much of it. Until today.

After checking my dotfiles repo, I realised that the file `/etc/pam.d/ly` has been updated from this:

```
#%PAM-1.0

auth       include      login
auth       optional     pam_gnome_keyring.so
account    include      login
password   include      login
session    include      login
session    optional     pam_gnome_keyring.so auto_start
```

To this:

```
#%PAM-1.0

auth       include      login
account    include      login
password   include      login
session    include      login
```

And that fixed the error message.

### Why this problem in the first place

Well, it turns out that as I was setting up `gnome-keyring`, following instructions on the Arch Wiki on how to set it up properly, I edited the file that says to edit **in case the keyring doesn't work out of the box**. But of course, in my case it worked out of the box with ly, so *the step was redundant and created the error message*. I just didn't think of checking if the keyring worked before performing all of the instructions.

## Sources

- [GNOME/Keyring, PAM step - Arch Wiki](https://wiki.archlinux.org/title/GNOME/Keyring#PAM_step)
