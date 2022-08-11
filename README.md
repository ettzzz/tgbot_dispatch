# tgbot_dispatch

simple application based on fastapi web service framework with python-telegram-bot to control some customized notifications.

## how to use and deploy

1. pip install -r ./requirements.txt
2. sudo cp ./deploy/tgbot_nginx.conf /etc/nginx/conf.d/
3. sudo apt install supervisor -y
4. sudo cp ./deploy/tgbot_supervisor.conf /etc/supervisor/conf.d/
5. sudo supervisorctl update all

## TODO:

- [ ] re-read bot script examples, make it looks better
- [ ] finish designed functions in bot_apis
- [ ] is there a way to use variable in supervisor.conf?
