# Arch Linux & Windows 11 dual-boot setup

## BEFORE INSTALLING ARCH LINUX

- Install Windows 11 and its bootloader.
- Prepare partitions beforehand: boot into an external drive with GParted Live, leave the space for Windows as "unallocated" space.
  - No need to create a separate EFI partition at this stage, as it will be created automatically through the Windows installation.
  - Leave the intended space for Arch Linux on a separate partition, unallocated or formatted as a Linux partition.
  - These spaces can be expanded or contracted later on, but it's risky and may result in data loss, so better to set everything now, before any OS is installed. I managed to resize partitions with GParted Live after OS installation multiple times, without errors or data loss, but there is still a risk, and it's generally better to avoid doing that.
- Start the Windows installation media and select "Customized: install...".
- Select the unallocated space meant for Windows.
- After initial installation, when you get to language selection again, open Terminal with Shift+F10 and type `OOBE\BYPASSNRO`, all caps, to bypass the internet connection requirement.
- After the automatic reboot, continue with installation; you can now select "I don't have internet" and complete the installation.

#### EXTEND EFI PARTITION AFTER WINDOWS IS INSTALLED

- Using GParted Live, extend the EFI partition; ensure it has enough space if you intend to install multiple kernels. The recommended size from the Arch Wiki is 1-4GB, I chose 1GB and never had low-space issues.
- If Windows doesn't boot at this point, use the Windows live image and click on "Repair your computer".
  - Select the option to "repair startup problems".

#### WINDOWS SETUP

- After Windows installation is complete and the EFI partition is the desired size, install the following programs on Windows:
  - Steam
  - Firefox
- Disable "Fast Startup" and hibernation: in an admin PowerShell run: `powercfg /H off`. Remember: PowerShell is generally not case-sensitive.
- Optimise Windows according to your preference; also make sure to turn Secure Boot off.
- Once Windows is fully set up, reboot into a live USB containing the Arch Linux ISO.

## INSTALLING ARCH LINUX

- Follow the installation guide on the Arch Wiki; my system is UEFI, but there are differences if the system uses legacy BIOS.
- Set keyboard layout to "UK" using: `loadkeys uk`.
- Just in case, verify boot mode using: `cat /sys/firmware/efi/fw_platform_size`. It should return "64"; if it doesn't, either the system is 32-bit or uses legacy BIOS; see guide.
- Connect to the internet, run: `iwctl`.
  - In the iwd prompt, run `help` for information, then find network adaptor name with `dpp list` and use it to connect to internet: run `dpp <wlan> start-enrollee` then run `station <wlan> get-networks` and connect to one using `station <wlan> connect <networkname>` and then typing in the password. Type `exit` and check if connected using `ping google.com`.
- Check that the system clock is accurate after connecting by using: `timedatectl`.
- Partition the disk, run `fdisk -l` to find current partitions, then run `fdisk /dev/<diskname>`; use `fdisk` on the path to the main disk, not one of its partitions.
  - Within the `fdisk` prompt, type `p` to print the partition table; if the Linux partition was formatted already, delete it first using `d` and selecting the correct partition number.
  - Do not touch Windows partitions, especially the EFI partition.
  - Once Linux partition has been deleted, or if it was unallocated in the first place, create a new partition using `n`, leave number and first sector unchanged, and on the last sector, specify the size of the partition in bytes; this will be swap and I will make it 8GB so I will type `+8G`. Create another partition for the filesystem, this time leaving the last sector unchanged.
  - Using `t`, change the type of these two partitions to "Linux swap" and "Linux root (x86-64)".
  - Double-check the partition table with `p` and write changes and exit with `w`.
- Format partitions using the following:
  - `mkfs.ext4 /dev/<rootpartition>` for the root partition.
  - `mkswap /dev/<swappartition>` for the swap partition.
  - Do not format or alter in any way the EFI partition containing the Windows bootloader.
- Mount partitions using the following:
  - `mount /dev/<rootpartition> /mnt`.
  - `mount --mkdir /dev/<efipartition> /mnt/boot`.
  - and turn swap on with `swapon /dev/<swappartition>`.
- Update mirrorlist by using `systemctl start reflector` and then check mirrorlist on `/etc/pacman.d/mirrorlist` for mistakes; refresh reflector if necessary.
- Install the base system using `pacstrap -K /mnt base linux linux-firmware`, you can substitute `linux` with any other kernel you want, install only one for now, later while chrooted more packages can be installed.
- Generate an fstab file using: `genfstab -U /mnt >> /mnt/etc/fstab`.
- Run `arch-chroot /mnt`.
- Set timezone: `ln -sf /usr/share/zoneinfo/<region>/<city> /etc/localtime`
  - Run `hwclock --systohc`
- Uncomment in `/etc/locale.gen` any needed locales, then run `locale-gen`. My locale is `en_GB.UTF-8 UTF-8`, then create the file `/etc/locale.conf` containing: `LANG=en_GB.UTF-8`. Also create a persistent keymap file: `/etc/vconsole.conf` containing `KEYMAP=uk`.
- Create the network hostname file in `/etc/hostname` containing simply the hostname in lowercase.
- Install additional packages now using pacman.
  - Base system:

    ```bash
    pacman -S nano sudo networkmanager grub efibootmgr linux-lts linux-zen neofetch os-prober intel-ucode reflector man-db man-pages texinfo tldr sof-firmware bluez bluez-utils polkit tlp xdg-user-dirs
    ```

  - Graphical environment:

    ```bash
    pacman -S qtile xorg xorg-xinit picom unclutter alacritty noto-fonts otf-font-awesome ttf-font-awesome papirus-icon-theme rofi firefox pavucontrol dunst python-dateutil python-psutil acpi nemo nemo-fileroller lxappearance pamixer xf86-video-intel ly variety nitrogen
    ```

- Set the root password by running `passwd`.
- To install GRUB, make sure to be inside the chroot and that the packages efibootmgr and grub are installed, then run: `grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB`.
- To detect Windows from GRUB, make sure that the package os-prober is installed, then uncomment `GRUB_DISABLE_OS_PROBER=false` inside `/etc/default/grub`.
- When this is done, and if the GRUB installation gave no errors, run: `grub-mkconfig -o /boot/grub/grub.cfg`.
- Note: before running `grub-mkconfig`, make sure the package intel-ucode is installed; GRUB will then auto-detect it and enable microcode updates on boot, which are very important.
- Run `exit` to exit chroot and run `reboot` to reboot into the new Arch installation; remember to remove the external USB.

## THINGS TO DO ON FIRST REBOOT OF FRESHLY INSTALLED ARCH

- Enable and start NetworkManager using:
  - `systemctl enable --now NetworkManager`
  - `systemctl enable --now NetworkManager-wait-online`
  - Then connect to a network using `nmtui`.
- To allow GRUB to detect Windows, edit `/etc/default/grub` and uncomment `GRUB_DISABLE_OS_PROBER=false`.
  - I also uncomment `GRUB_DISABLE_SUBMENU` and `GRUB_SAVEDEFAULT` and I change `GRUB_DEFAULT=0` to `GRUB_DEFAULT=saved` then update GRUB config with `grub-mkconfig -o /boot/grub/grub.cfg`.
- Add an unprivileged user with: `useradd -m -G <groups> <username>`.
  - Groups that I add a user to are: wheel, audio, video, storage.
  - Then change the user's password with `passwd <username>`.
- Add wheel to the sudoers file using: `EDITOR=nano visudo` and uncommenting the line that says `%wheel ALL=(ALL:ALL) ALL`. This allows users in the wheel group to run any command using sudo.
- Enable reflector and refresh mirrors:
  - `systemctl enable reflector`.
  - `systemctl start reflector`.
- Set up the firewall using iptables: follow the guide in the Arch Wiki page called "simple stateful firewall". Also install fail2ban, create a file in `/etc/fail2ban/jail.local` containing:

  ```bash
  [DEFAULT]
  bantime=1d
  ```

  - enable & start fail2ban service.
  - Note: Instead of creating a firewall from scratch using the Arch Wiki, `ufw` can be installed; the setup process is much simpler and quicker, keeping fail2ban too.
- To get Bluetooth to work, make sure bluez and bluez-utils are installed and start/enable Bluetooth using `systemctl enable --now bluetooth` and add the user to the lp group using `usermod -aG lp <username>`
- Install TLP and enable it with `systemctl enable --now tlp`.
- Install polkit and its graphical prompt, lxsession-gtk3, and autostart it by appending the following to xinitrc: `/usr/bin/lxpolkit &`.

#### GRAPHICAL ENVIRONMENT

- Install qtile and its dependencies: qtile, xorg-server, xorg-xinit; the package group `xorg` can be installed instead of xorg-server; it includes xorg-apps, which contains useful additions.
- Create a `.xinitrc` file in the home directory and write `qtile start`. Install a default terminal emulator; mine is alacritty, and then qtile can be started by running `startx`.
  - If qtile doesn't display characters correctly, install the `noto-fonts` package.
- The "Super + Enter" key combination should bring up the terminal.
- Now qtile can be configured. I grab my config from an external drive and paste it as `~/.config/qtile/config.py`; otherwise, `config.py` might need to be created manually.
- I also paste my `.xinitrc` and make sure everything is commented out apart from `qtile start` for now.
- I use picom and unclutter; I install them and make sure their `.xinitrc` lines are uncommented.
- For my qtile widgets, the following dependencies are required: python-dateutil, python-psutil, dunst.
  - Also remember to copy the changeBrightness and changeVolume scripts from `/usr/local/bin/` onto the new system.
  - Install the ttf-font-awesome, otf-font-awesome and papirus-icon-theme as they are also required.
- To change GTK global theme install lxappearance and download Dracula theme GTK from the official website extracting and copying it to `/usr/share/themes` and `~/.themes` applying it with lxappearance and also with `sudo lxappearance`.
- To get volume and backlight controls to work, add user to the video group `usermod -aG video <username>`, install pamixer, xf86-video-intel and dunst packages, and uncomment dunst section in `.xinitrc`, copy its `~/.config/dunst/dunstrc` from drive and reboot.
- To change the Rofi theme, run `rofi-theme-selector`; make sure `which` is installed, as it's a dependency.
- Also change the icon theme to the Dracula icon theme, download it from the official website and extract it into the `~/.icons` folder, then apply it with lxappearance.
- Copy all the content of `/etc/X11/xorg.conf.d/` from backup media to set resolution and touchpad click.
- Copy `~/.config/alacritty/alacritty.toml` from backup media.
- Copy `~/.bashrc` from backup media.
- Install ly display manager and enable it with `systemctl enable ly`, then edit the file at `/usr/share/xsessions/qtile.desktop` to replace `Exec=qtile start` with `Exec=/home/<username>/.xinitrc`. Now reboot and log in through the qtile session; it should use xinitrc and start all your programs.
- Install variety and nitrogen, uncomment their line in xinitrc, also make sure in the file `~/.config/variety/scripts/set_wallpaper` the section of the loop where it detects window manager and nitrogen or feh is uncommented, see more at peterlevi.com/variety/how-to-install/.
- If QT5 apps are installed, such as flameshot, then also install the `qt5ct` package and add the environment variable `QT_QPA_PLATFORMTHEME=qt5ct` to `/etc/environment`.
  - Also download the QT5 Dracula theme to `~/.themes`, then copy `Dracula.conf` into `~/.config/qt5ct/colors/` and apply theme through qt5ct.
- To manage dual monitors install `autorandr` and `arandr` and enable autorandr with `systemctl enable --now autorandr`, while not connected to monitor run `autorandr --save <profilename>`, connect HDMI now and it should adjust to two screens automatically, make positioning adjustments with arandr, apply and save profile again with autorandr on a different name. Also copy `~/.config/variety/scripts/set_wallpaper` from backup.

#### FIREFOX

- Install the Firefox package.
- Login into Firefox account to get all extensions and settings.
- Type in the search bar `about:config` and create a new line with `ui.systemUsesDarkTheme` and set it to `1` or `true`.
- In settings, go to General -> Website Appearance and set it to "Dark".
- To have pixel-perfect trackpad scrolling, set a global variable by editing `/etc/environment` and adding the following line: `MOZ_USE_XINPUT2=1`, then reboot.
- To use compact mode in `about:config` set `browser.uidensity` to `1`.
- To disable the keybinding Ctrl + Q to quit Firefox, create the option `browser.quitShortcut.disabled` and set it to true.

#### AUR, FLATPAK AND MULTILIB REPO

- To enable the multilib repository, which contains 32-bit packages that run on 64-bit systems, such as Wine and Steam, uncomment the line in `/etc/pacman.conf`:

  ```bash
  [multilib]
  Include=/etc/pacman.d/mirrorlist
  ```

- To install AUR packages, better to do that manually and not use a pacman wrapper, as it may lead to a defective system. To do that, I've created `~/.aur` where I pull `PKGBUILD` from git using `git clone <link>` where `<link>` is the git clone URL, then cd into the directory and install using `makepkg -si`. Remember to check the `PKGBUILD` file for malicious software.
  - To update AUR packages manually, follow the same procedure but replace `git clone` with `git pull`. Also enable notifications by email to get notified when a package is updated.
- To install Flatpak, install flatpak, xdg-desktop-portal and a back end such as xdg-desktop-portal-gtk, more at the Arch Wiki "xdg-desktop-portal" page, then reboot.
  - Themes in flatpaks have to be installed individually; after installing Betterbird and configuring its layout, install the Dracula theme on it, optionally the Dark Reader extension.
- In Obsidian, install the Dracula-official theme and, in appearance settings, set the window frame to "native frame".

#### REMOVE MIN, MAX, CLOSE WINDOW BUTTONS IN GTK

- In the file `~/.config/gtk-3.0/settings.ini` add the following line: `gtk-decoration-layout=appmenu:none`.

#### SET UP GNOME KEYRING TO WORK WITH GIT

- GNOME keyring is needed to use libsecret as an authentication helper by git to push to GitHub; ensure gnome-keyring, libsecret, and seahorse (optional GUI) are installed. Also make sure the "secrets" section in my xinitrc is unticked.
- To initialize the keyring edit `/etc/pam.d/<displaymanager>` substituting in the display manager name, add: `auth optional pam_gnome_keyring.so` at the end of the "auth" section, and: `session optional pam_gnome_keyring.so auto_start` at the end of the "session" section.
- To ensure setup is working, check Seahorse, reboot, and check Seahorse again; a default keyring named "login" that wasn't there before should have appeared.
- Ensure the "login" keyring password is the same as the user; this way it will auto-unlock.

#### GIT & GITHUB FOR DOTFILES MANAGEMENT

- Ensure the package git is installed.
- To set up git on first use, run the following:
  - `git config --global user.name "<username>"`.
  - `git config --global user.email "<githubemail>"`.
  - `git config --global core.editor "nano -w"`.
  - `git config --global init.defaultbranch "<branchname>"`.
  - `git config --global credential.helper /usr/lib/git-core/git-credential-libsecret`.
  - For `<branchname>` I put the name of the machine; you can check settings with `git config --list`.
- To initialize the repository, run `git init --bare $HOME/.dotfiles` then create an alias in bashrc as follows: `alias dotfiles="/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=/"`.
- After that, use the alias to run `dotfiles config status.showUntrackedFiles no`.
- In GitHub, create an empty repository and copy the URL, then add it to dotfiles with `dotfiles remote add origin <pasteurl>`, then run `dotfiles branch -M <branchname>`.
- On GitHub, go to Settings -> Developer Settings -> Personal Access Tokens -> Fine-grained tokens -> Create new token, set name, expiry date, and set permission to either all repositories or select the newly created repository; remember to set all permissions individually in the "permissions" section.
- Once created, copy the access token.
- Run `dotfiles push -u origin`.
- Authenticate with GitHub username and paste the access token instead of the password.
- Once authenticated, check Seahorse; the default login keyring should contain GitHub credentials now.

#### GIT COMMANDS AND USAGE

- If not using alias dotfiles, make sure to cd into the repository directory and substitute dotfiles with git.
- To add a file or signal a modified file, use `dotfiles add /path/to/file`.
- To see the status of pending changes `dotfiles status`.
- To commit changes `dotfiles commit`.
- To push a commit to GitHub, run `dotfiles push -u origin <branchname>` or, more simply, `dotfiles push`.
- To see a list of all files being tracked, cd into / and run `dotfiles ls-files`.

## TROUBLESHOOTING AND COMMON ISSUES

#### REBUILD GRUB

- Boot into the Arch Linux installation medium.
- Use `fdisk -l` to find the Linux filesystem.
- Mount the partition using `mount /dev/... /mnt`.
- Chroot into the partition using `arch-chroot /mnt`.
- Find the EFI partition using `fdisk -l`.
- Mount the EFI partition in `/mnt`.
- Install GRUB using `grub-install --efi-directory=/mnt`.

#### RE-CREATE WINDOWS BOOT PARTITION

- Boot from a Windows live image and press Shift+F10 for the terminal.
- Run `diskpart`, use `list disk`, `select disk`, `list partition`, `select partition` to select the existing EFI partition.
- Run `format fs=fat32 quick` to format it.
- Use `list volume` to find the letter of the volume where the Windows files are.
- Type `exit` to exit diskpart and run `bcdboot C:\Windows`. C = the letter of the volume with Windows files.
