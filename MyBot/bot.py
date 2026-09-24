from flask import Flask
import threading
import requests, re
import os
import telebot
from datetime import datetime
import pytz
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"
def run():
    app.run(host='0.0.0.0', port=10000)
def keep_alive():
    t = threading.Thread(target=run)
    t.start()
def get_live_weather(city="Indore"):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo = requests.get(geo_url, timeout=10).json()
        if 'results' not in geo: return None
        lat = geo['results'][0]['latitude']
        lon = geo['results'][0]['longitude']
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,relative_humidity_2m"
        w = requests.get(weather_url, timeout=10).json()
        temp = w['current']['temperature_2m']
        wind = w['current']['wind_speed_10m']
        hum = w['current']['relative_humidity_2m']
        ist = pytz.timezone('Asia/Kolkata')
        now = datetime.now(ist)
        time_str = now.strftime("%d-%m-%Y, %I:%M %p")
        return f"{city} ka LIVE Mausam: {temp}°C, Hawa {wind} km/h, Humidity {hum}%\nDate/Time: {time_str} (IST)"
    except:
        return None

@bot.message_handler(func=lambda m: True)
def handle(message):
    try:
        text = message.text.lower()
        if "mausam" in text or "mousam" in text or "weather" in text or "tapman" in text:
            city = "Indore"
            match = re.search(r"(\w+)\s+ka\s+(mausam|mousam|weather|tapman)", text)
            if match:
                city = match.group(1)
            elif "morena" in text: city = "Morena"
            elif "gwalior" in text: city = "Gwalior"

            weather = get_live_weather(city)
            if weather: bot.reply_to(message, weather)
            else: bot.reply_to(message, f"{city} ka mausam nahi mila")
        else:
            bot.reply_to(message, "Mausam pucho, jaise 'Indore ka mausam'")
    except Exception as e:
        print(e)

print("Bot chal raha hai...")
keep_alive()
bot.polling()
