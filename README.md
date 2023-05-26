# tgbot_dispatch

simple application based on fastapi web service framework with python-telegram-bot to control some customized notifications.

### appendix

some nginx and supervisord conf, might be helpful

```shell
server {
    listen 80;
    server_name your_domain_name;
    access_log /var/log/nginx/tgbot_access.log;
    error_log /var/log/nginx/tgbot_error.log;

    location /tgbot {
        include /etc/nginx/proxy_params;
        proxy_pass http://127.0.0.1:7710;
    }
}
```

```shell
[group:tgbot]
programs=fastapi,tgbot

[program:fastapi]
user=whoyouare
priority=99
directory=/path/to/tgbot_dispatch
command=/home/whoyouare/miniconda3/envs/tgbot/bin/uvicorn main:app --port 7710
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/tgbot_fastapi.log

[program:tgbot]
user=whoyouare
priority=98
directory=/path/to/tgbot_dispatch
command=/home/whoyouare/miniconda3/envs/tgbot/bin/python3 activate_bot.py
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/tgbot.log
```
