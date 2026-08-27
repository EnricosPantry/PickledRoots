# PickledRoots

This is a repository of notes from a personal Arch Linux and Windows 11 dual-boot setup.
The system was in use between 2022 and 2025. The purpose of this documentation is to capture a snapshot of how it was during its active years, rather than to provide an up-to-date guide. The vast majority of the processes can still be followed today; bear in mind, however, that some packages and commands may be out of date.

## About

The setup is for an Arch Linux installation as the main daily driver, with a minimal Windows 11 used for gaming alongside Arch.
The system ran on a Lenovo ThinkPad X1 Carbon Gen 9, with an Intel processor and graphics.

The Arch installation used a minimal window manager, Qtile, rather than a full desktop environment, and deliberately ran the lowest possible number of packages. This ensured the system was simple and stable, even when updating daily.

The system and files were backed up in the following ways:
- A custom-made Rsync script copied configuration file changes from anywhere in the filesystem to an external drive. It separately backed up the user home folder to a second partition of the drive.
- A bare Git repository was used to track changes and upload commits to GitHub. The dotfiles themselves are not published.

Ly was used as the display manager, Firefox as the browser, Alacritty as the terminal emulator, and Rofi as the system and application menu.

## Contents

- [Arch Linux and Windows 11 dual-boot setup](Arch-Windows11-dual-boot-setup.md)
- [Keyboard layout reverts to US](Keyboard layout reverts to US)

## Sources

The notes and setup guide will refer multiple times to the Arch Wiki, which was used consistently and thoroughly whilst building this setup.
Visiting the [Arch Linux Wiki](https://wiki.archlinux.org/title/Main_page) is highly recommended for up-to-date instructions and as a general Linux knowledge base.

## Disclaimer

The guide and troubleshooting notes reflect personal system setup and taste. These instructions are not guaranteed to work on different hardware. Some steps involve repartitioning disks and modifying bootloaders, and may cause data loss. Backing up your data is recommended.
