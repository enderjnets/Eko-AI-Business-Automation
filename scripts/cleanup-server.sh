#!/bin/bash
# cleanup-server.sh — Eko AI Server Disk Cleanup
# Run this on the server when disk usage > 90%
# Requires: docker, journalctl, logrotate

set -euo pipefail

LOGDIR="/var/log/eko-ai"
BACKUP_DIR="/app/backups"
DOCKER_DIR="/var/lib/docker"

echo "=== Eko AI Server Cleanup ==="
echo "Date: $(date)"
echo "Disk BEFORE:"
df -h / | tail -1

# 1. Docker system prune (images, containers, networks, volumes not in use)
echo ""
echo "[1/6] Pruning Docker system..."
docker system prune -af --volumes || true

# 2. Clean old Docker build cache
echo ""
echo "[2/6] Cleaning Docker build cache..."
docker builder prune -af || true

# 3. Rotate and compress logs
echo ""
echo "[3/6] Rotating logs..."
mkdir -p "$LOGDIR"

# Create logrotate config if not exists
if [ ! -f /etc/logrotate.d/eko-ai ]; then
cat << 'EOF' | sudo tee /etc/logrotate.d/eko-ai
/var/log/eko-ai/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 root root
}
EOF
fi

# Truncate large container logs (>100MB)
find "$DOCKER_DIR/containers" -name "*.log" -size +100M -exec sh -c 'truncate -s 0 "$1"' _ {} \; || true

# 4. Clean old backups (keep last 14 days)
echo ""
echo "[4/6] Cleaning old backups..."
find "$BACKUP_DIR" -type f -mtime +14 -delete || true

# 5. Clean package caches
echo ""
echo "[5/6] Cleaning package caches..."
apt-get autoclean || true

# 6. Clean /tmp
echo ""
echo "[6/6] Cleaning /tmp..."
find /tmp -type f -atime +3 -delete || true

echo ""
echo "Disk AFTER:"
df -h / | tail -1

echo ""
echo "=== Cleanup complete ==="
