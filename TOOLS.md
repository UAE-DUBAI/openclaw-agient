# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Environment: Proxmox VM (UAE-DUBAI)

This environment has strict outbound firewall rules blocking standard SSH (port 22).

### GitHub Access (SSH over HTTPS)
- **Problem:** Port 22 is blocked outbound.
- **Solution:** Use SSH over HTTPS port 443 via `ssh.github.com`.
- **Config:** `~/.ssh/config` must contain:
  ```ssh
  Host github.com
    Hostname ssh.github.com
    Port 443
    User git
  ```
- **Verification:** `ssh -T git@github.com` (should connect successfully).

### Cameras
- (None configured yet)

### SSH
- (None configured yet)

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.
