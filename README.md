# tgbot_dispatch

simple application based on fastapi web service framework with python-telegram-bot to control some customized notifications.

## how to use and deploy

0. copy `private_vars.py` to `./configs/` from your base
1. run `sudo apt install supervisor nginx -y`
2. run `pip install -r ./requirements.txt`
3. run `sudo cp ./deploy/tgbot_nginx.conf /etc/nginx/conf.d/`
4. run `sudo cp ./deploy/tgbot_supervisor.conf /etc/supervisor/conf.d/`
5. manually change details of these conf files regards of deploy instances
6. run `sudo systemctl restart nginx`
7. run `sudo supervisorctl update`

## TODO:

- [x] re-read bot script examples, make it looks better
- [x] finish designed functions in bot_apis
- [ ] is there a way to use variable in supervisor.conf?
