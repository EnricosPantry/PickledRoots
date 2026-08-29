# PickledRoot

This is a repository of notes from a personal Arch Linux and Windows 11 dual-boot setup on a device affectionately named Wasabi.

The system was used as a main daily driver between 2022 and 2025. The purpose of this documentation is to capture a snapshot of how it was during its active years, rather than to provide an up-to-date guide. The vast majority of the processes can still be followed today; bear in mind, however, that some packages and commands may be out of date.

## About

The setup was for an Arch Linux installation as the main daily driver, with a minimal Windows 11 used for gaming alongside Arch.
The machine itself was a Lenovo ThinkPad X1 Carbon Gen 9, with an Intel processor and graphics.

The Arch installation used a minimal window manager, Qtile, rather than a full desktop environment, and deliberately ran the lowest possible number of packages. This ensured the system was simple and stable, even when updating daily.

The system and files were backed up in the following ways:

- A custom-made rsync script copied configuration file changes from anywhere in the filesystem to an external drive. It separately backed up the user home folder to a second partition of the drive.
- A bare Git repository was used to track configuration file changes throughout the filesystem and upload commits to GitHub. The dotfiles themselves are published in this repository, inside the "Wasabi dotfiles preview" folder.

Ly was used as the display manager, Firefox as the browser, Alacritty as the terminal emulator, and Rofi as the system and application menu.

## Contents

### Setup guide

- [Wasabi setup guide: Arch Linux and Windows 11 dual-boot](arch-windows11-dual-boot-setup.md) - this is the full system setup guide. It includes Windows and Arch Linux step-by-step installation, and the post-installation to-do list.

### Troubleshooting notes

- [Bad behaviour: keyboard layout reverts to US](keyboard-layout-reverts-to-us.md) - the keyboard layout kept changing to US randomly for months, with no apparent solution; found the root cause after a seemingly unrelated action.
- [PAM error: gkr-pam: couldn't unlock the login keyring](gkr-pam-couldnt-unlock-the-login-keyring.md) - this innocuous error message showed up in journalctl after every boot; found the cause to be a single file that I configured wrongly.
- [Kernel error: i801_smbus: SMBus is busy, can't use it!](i801-smbus-smbus-is-busy-cant-use-it.md) - innocuous kernel error showing up in journalctl after boot; resolved by preventing the module's implicit loading.
- [Bad behaviour: screen blanking during media playback](screen-blanking-during-video-and-audio.md) - the screen kept on timing out (blanking) even whilst videos or music were playing; wrote a custom Bash script to prevent it from happening.
- [Bad behaviour: wrong system time after change to BST](system-time-error-after-change-to-bst.md) - the change to British Summer Time moved the clock forward in Linux by 2 hours rather than 1; the cause was a wrong time setup in Windows.

### Configuration files

- [Wasabi-dotfiles-preview](Wasabi-dotfiles-preview) - this is a folder containing all manually written and modified configuration files; it is structured the same way as the root folder on a Linux installation, with all original file paths preserved. All user-authored original scripts are stored in usr/local/bin.

## Sources

The notes and setup guide refer multiple times to the Arch Wiki, which was used consistently and thoroughly whilst building this setup.
Visiting the [Arch Wiki](https://wiki.archlinux.org/title/Main_page) is highly recommended for up-to-date instructions and as a general Linux knowledge base.

## Disclaimer

The guide and troubleshooting notes reflect personal system setup and taste. These instructions are not guaranteed to work on different hardware. Some steps involve repartitioning disks and modifying bootloaders, and may cause data loss. Backing up your data is recommended.
