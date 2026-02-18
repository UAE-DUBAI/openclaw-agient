# Host Firewall Configuration (Manual)

The following `ufw` commands were recommended but require manual execution on the host machine due to `no_new_privs` restrictions:

```bash
# Allow specific local subnets for SSH
sudo ufw allow from 192.168.0.0/24 to any port 22 proto tcp comment 'SSH Default Network'
sudo ufw allow from 192.168.16.0/24 to any port 22 proto tcp comment 'SSH PBX Network'
sudo ufw allow from 192.168.17.0/24 to any port 22 proto tcp comment 'SSH Servers Network'

# Allow SSH via Tailscale
sudo ufw allow in on tailscale0 to any port 22 proto tcp comment 'SSH Tailscale'

# Remove open-to-world SSH if it exists (check 'ufw status' first)
sudo ufw delete allow 22/tcp
sudo ufw delete allow ssh

# Enable UFW (if not already active)
sudo ufw enable
```

**Status:** PENDING MANUAL EXECUTION by Mahir.
