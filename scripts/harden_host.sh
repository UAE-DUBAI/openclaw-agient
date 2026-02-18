#!/bin/bash
# OpenClaw Host Hardening Script (Run as sudo on host)
# Usage: sudo ./harden_host.sh

set -e

echo "🔒 Starting Host Hardening..."

# 1. Update & Install Essentials
apt update && apt install -y ufw fail2ban unattended-upgrades

# 2. Configure Firewall (UFW)
echo "🔥 Configuring Firewall..."
ufw default deny incoming
ufw default allow outgoing

# Allow Critical Services
ufw allow 22/tcp comment 'SSH'
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'

# Enable UFW
echo "⚠️ Enabling UFW..."
ufw --force enable

# 3. Harden SSH
echo "🔑 Hardening SSH..."
if [ -f /etc/ssh/sshd_config ]; then
    cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
    # Disable Root Login
    sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
    # Restart SSH
    systemctl restart ssh
fi

# 4. Enable Automatic Updates
echo "🔄 Enabling Unattended Upgrades..."
dpkg-reconfigure -plow unattended-upgrades

# 5. Set Timezone
echo "Cc: Setting Timezone to Dubai..."
timedatectl set-timezone Asia/Dubai

echo "✅ Hardening Complete. Verify access before closing session."
ufw status verbose
