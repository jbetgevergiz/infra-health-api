# Infra Health API

Flask-based infrastructure status API running directly on the Proxmox host. Provides real-time container status and Prometheus-compatible metrics for the homelab monitoring stack.

**Live:** https://status.betgevergiz.com/api/status

## Endpoints

### `GET /api/status`
Returns JSON with all container states, host metrics.

```json
{
  "host": "proxmox",
  "timestamp": "2026-04-02T20:00:00Z",
  "running_containers": 14,
  "containers": [
    {
      "id": 101,
      "name": "pihole",
      "status": "running",
      "uptime": "47d 3h"
    }
  ],
  "host_metrics": {
    "cpu_percent": 12.4,
    "memory_percent": 34.2,
    "disk_percent": 39.0
  }
}
```

### `GET /metrics`
Prometheus-compatible text format. Scraped by Prometheus in CT 133 every 15s.

```
# HELP proxmox_containers_running Number of running LXC containers
# TYPE proxmox_containers_running gauge
proxmox_containers_running 14

# HELP proxmox_host_cpu_percent Host CPU utilization
# TYPE proxmox_host_cpu_percent gauge
proxmox_host_cpu_percent 12.4
```

## Architecture

Runs as a systemd service directly on the Proxmox host (not in a container) so it has native access to `pct list` and `/proc` filesystem without SSH overhead. Exposed publicly via Cloudflare Tunnel through CT 103.

```
Prometheus (CT 133) ──scrape every 15s──▶ /metrics endpoint
                                              │
                                         Flask API
                                         (Proxmox host :5055)
                                              │
                                    pct list + /proc/meminfo
                                    + /proc/stat + /proc/diskstats
```

## Deployment

```bash
# Runs as systemd service on Proxmox host
# Service file: /etc/systemd/system/status-api.service

systemctl status status-api
systemctl restart status-api
journalctl -u status-api -f
```

## Why on the Host (Not a Container)

Running Flask in a container would require either:
- Mounting `/proc` from the host (messy, security concern)
- SSH-ing into the host from the container (overhead, key management)

Direct execution on the host gives native access to all metrics sources with no overhead. The tradeoff is that it runs as root — acceptable for a homelab, not for production.

## Related

- [Grafana Dashboard](https://monitor.betgevergiz.com) — live visualization
- [homelab](https://github.com/jbetgevergiz/homelab) — full infrastructure docs
