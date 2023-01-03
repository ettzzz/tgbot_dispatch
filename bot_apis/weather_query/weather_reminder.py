import requests

# from telegram.ext import CallbackContext
from telegram.ext import ContextTypes
from telegram import Update


def weather_broadcast(citycode=101010300):
    """
    check citycode at http://api.help.bj.cn/api/CityCode.XLS
    """
    url = "http://api.help.bj.cn/apis/weather"
    params = {"id": str(citycode)}
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return f"天气API网络错误 code {r.status_code}"
    res = r.json()

    today = res.get("today")
    uptime = res.get("uptime")
    temp = res.get("temp")
    wd = res.get("wd")
    wdforce = res.get("wdforce")
    humidity = res.get("humidity")
    aqi = res.get("aqi")
    precipitation_24h = res.get("prcp24h")

    text = f"{today} {uptime}实时天气：温度 {temp}°C，湿度 {humidity}，风速 {wd}{wdforce}，空气指数 {aqi}，24小时降雨量 {precipitation_24h}。"
    return text


# def call_weather_reminder(update: Update, _: CallbackContext):  # _ is a must...
async def call_weather_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = weather_broadcast()  ## todo: how can we use variable?
    html_text = f'<a href="">{text}</a>'
    # update.message.reply_html(html_text, disable_web_page_preview=True)
    await update.message.reply_html(html_text, disable_web_page_preview=True)
