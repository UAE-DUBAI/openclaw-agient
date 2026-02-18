# Remediation Plan: Restrict SSH to Tailscale Only

**Goal:** Close port 22 to the public internet and allow SSH access ONLY via the Tailscale private network (IP range `100.110.179.28` / Tailscale interface).

**Current Posture:**
*   SSH (sshd) listening on `0.0.0.0:22` (ALL interfaces).
*   Potential public exposure if not blocked by external cloud firewall.

**Risk:**
If you lock yourself out of Tailscale, you will lose SSH access unless you have console/VNC access via your hosting provider.

**Steps:**
1.  Verify UFW is installed/active (checked earlier, failed non-root - assuming `sudo` needed).
2.  Allow SSH from Tailscale interface (`in on tailscale0`).
3.  Deny SSH from everywhere else.
4.  Reload UFW.

**Commands to Execute:**
```bash
# 1. Allow SSH specifically from Tailscale interface (safer than IP which might change)
sudo ufw allow in on tailscale0 to any port 22 proto tcp comment 'Allow SSH via Tailscale'

# 2. If you have a specific management IP (e.g. static home IP), allow it too as backup:
# sudo ufw allow from <YOUR_STATIC_IP> to any port 22 proto tcp

# 3. Deny other SSH traffic (this overrides the default allow if present)
sudo ufw delete allow 22/tcp
sudo ufw delete allow ssh

# 4. Enable firewall if not already active (DANGER: Ensure at least one allow rule exists first!)
sudo ufw enable
```

**Rollback Plan:**
If you get locked out, access the server via your cloud provider's web console (VNC/TTY) and run:
`sudo ufw disable`
