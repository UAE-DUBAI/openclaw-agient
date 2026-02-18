# Restore Instructions

## Overview
This repository contains the configuration and setup scripts for your OpenClaw assistant. Follow these instructions to restore your environment on a new machine.

## Prerequisites
- A fresh **Ubuntu 24.04** host (or similar).
- **SSH access** with sudo.
- **Git** and **Node.js** (v22+) installed.
- **OpenClaw** installed (`npm install -g openclaw`).

## Step 1: Clone Repository
Clone this repository to your new machine:
```bash
git clone https://github.com/UAE-DUBAI/openclaw-agient.git
cd openclaw-agient
```

## Step 2: System Hardening
Run the `scripts/harden_host.sh` script on the host machine as sudo to secure it (configure firewall, SSH, updates, timezone):
```bash
sudo chmod +x scripts/harden_host.sh
sudo ./scripts/harden_host.sh
```

## Step 3: Restore Configuration
1.  **Copy Configuration:**
    The `config/openclaw_config.json` file contains your user-specific settings. Copy it to your user's home directory:
    ```bash
    mkdir -p ~/.openclaw
    cp config/openclaw_config.json ~/.openclaw/openclaw.json
    ```

2.  **Restore Cron Jobs:**
    View `config/cron_list.txt` to see your scheduled tasks. Re-create them using `openclaw cron add`:
    ```bash
    # Example: Daily security audit
    openclaw cron add --name healthcheck:security-audit --schedule "0 9 * * 0" --tz "Asia/Dubai" --payload "Run openclaw security audit"
    
    # Example: Daily Git Backup (This one!)
    openclaw cron add --name backup:workspace-daily --schedule "0 4 * * *" --tz "Asia/Dubai" --payload "git add . && git commit -m 'Auto-backup' && git push"
    ```

3.  **Restore Workspace Files:**
    Copy the contents of this repository (excluding `.git` metadata if desired) to your workspace directory if it's different:
    ```bash
    cp -r * ~/.openclaw/workspace-telegram/
    ```

## Step 4: Verify
1.  Check open ports: `sudo ss -ltnup`
2.  Check OpenClaw status: `openclaw status`
3.  Check cron jobs: `openclaw cron list`

## Notes
- **Secrets:** This backup does *not* include sensitive secrets (API keys, auth tokens) unless you manually added them. Re-add these via `openclaw config set` or environment variables on the new machine.
- **SSH Keys:** You may need to generate new SSH keys for GitHub and add them to your account.
