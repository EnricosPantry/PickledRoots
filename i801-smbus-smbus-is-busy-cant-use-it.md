# Kernel error: i801_smbus: SMBus is busy, can't use it**!**

*Written 20/03/2024. Arch Linux, kernel 6.8.1.*

## What happened

After an update, I can't remember exactly which one, but a little before kernel 6.8.1, I started getting the following error messages after running `journalctl -b -p3`:

```
kernel: i801_smbus 0000:00:1f.4: Transaction timeout
kernel: i801_smbus 0000:00:1f.4: Failed terminating the transaction
kernel: i801_smbus 0000:00:1f.4: SMBus is busy, can't use it!
kernel: i801_smbus 0000:00:1f.4: SMBus is busy, can't use it!
kernel: i801_smbus 0000:00:1f.4: SMBus is busy, can't use it!
kernel: i801_smbus 0000:00:1f.4: SMBus is busy, can't use it!
kernel: i801_smbus 0000:00:1f.4: SMBus is busy, can't use it!
kernel: i801_smbus 0000:00:1f.4: SMBus is busy, can't use it!
kernel: i801_smbus 0000:00:1f.4: SMBus is busy, can't use it!
```

Exactly how it is written, precisely this many times.

I could find no other problem apart from these error messages showing in journalctl, and the system was running as smoothly as if nothing happened.

## The solution

I found a similar error that a user posted on the Arch Forums page listed below, and in the thread somebody suggested the name of the kernel module, which is `i2c_i801`, and advised to blacklist the module (prevent it from loading at boot).

So, on the Kernel module Arch Wiki page listed below, I found how to do that. In `/etc/default/grub`, on the line where it says `GRUB_CMDLINE_LINUX_DEFAULT=`, append either `module_blacklist=i2c_i801`, which will completely refuse to load the module, or `modprobe.blacklist=i2c_i801`, which will only prevent implicit loading and let you load the module later.
I ran both options and tested the outcomes:

- Completely refusing to load the module worked in getting rid of the errors, but replaced them with another error message saying that the module has been blacklisted.
- Only preventing implicit loading got rid of the original error messages and didn't seem to have any impact on overall system operations.

So I've ended up choosing the less invasive option and only preventing implicit loading. I've added `modprobe.blacklist=i2c_i801` to the file and reloaded the grub configuration by running:

```
grub-mkconfig -o /boot/grub/grub.cfg
```

Rebooted once it was done, and that's it. The error message disappeared.
This is a mitigation rather than a long-term solution, as it does not fix the underlying issue. I decided to keep it for now as it does not impact any other system functionality at all.

## Sources

- [What are i801_smbus timeout and rmi4 errors? - Arch Forums](https://bbs.archlinux.org/viewtopic.php?id=254885)
- [Kernel module, blacklisting - Arch Wiki](https://wiki.archlinux.org/title/Kernel_module#Blacklisting)
