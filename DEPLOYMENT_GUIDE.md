# Deployment Guide — srspady.com on UbuntuServ

Target: FastAPI + Uvicorn on the Ubuntu server (UbuntuServ), served to
the public through a Cloudflare Tunnel. No inbound ports. Deploy is
Spencer's step: pull + restart.

DNS and hosting decisions are Spencer's step and are **not** covered here.
This guide assumes the domain already points at the tunnel and the
tunnel already routes the site's hostname to the local service.

## First install (once)

```bash
# On UbuntuServ, as the service user:
git clone https://github.com/spencerawlson/srspady.com.git ~/srspady.com
cd ~/srspady.com
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## systemd unit — `srspady.service`

Create `/etc/systemd/system/srspady.service` (adjust the user and paths
to the real install):

```ini
[Unit]
Description=srspady.com — S. R. Spady, A Life in Progress
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=sspady
WorkingDirectory=/home/sspady/srspady.com
Environment=PATH=/home/sspady/srspady.com/.venv/bin
ExecStart=/home/sspady/srspady.com/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now srspady.service
sudo systemctl status srspady.service
curl http://127.0.0.1:8000/healthz
```

## Cloudflare Tunnel

The tunnel routes the site's public hostname to `http://127.0.0.1:8000`
on UbuntuServ — same pattern as SpencerLab. The app itself listens only
on loopback; nothing is exposed directly. Tunnel configuration (tunnel
name, hostname routing, DNS records) is Spencer's step.

## Deploy (every change)

```bash
cd ~/srspady.com
git pull
source .venv/bin/activate
pip install -r requirements.txt   # only when requirements.txt changed
sudo systemctl restart srspady.service
curl http://127.0.0.1:8000/healthz
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/
```

Verify a couple of section pages return 200 after the restart
(`/travels`, `/lab`, `/built`) before calling the deploy done.

## Troubleshooting

- `systemctl status srspady.service` — check the unit is active and read
  the last log lines.
- `journalctl -u srspady.service -n 50` — recent app output.
- `curl http://127.0.0.1:8000/healthz` — should return
  `{"status": "ok", "sections": 21}`. If it fails, uvicorn is not up or
  not listening on 127.0.0.1:8000.
- Template errors surface at first request for the affected page, not at
  startup — after a deploy, curl the homepage plus a few sections.
- No secrets live in this repository. If a deploy ever needs one, it
  goes in the systemd unit (`Environment=` / `EnvironmentFile=`), never
  in git.
```

## Rollback

```bash
cd ~/srspady.com
git log --oneline -5        # find the last good commit
git reset --hard <commit>   # only with Spencer's go
sudo systemctl restart srspady.service
```
