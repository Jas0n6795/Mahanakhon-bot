import discord
from discord.ext import commands
from flask import Flask, request
import threading, random, os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
app = Flask(__name__)

MESSAGES = [
    "🔧 ลูกสูบเกิดแล้ว! รีบไปแย่งกันเลย!",
    "⚡ ร้านลูกสูบรีสต็อกแล้ว ของดีมีน้อย ใครช้าอด!",
    "🏁 โอกาสมาแล้ว! ลูกสูบ {name} เกิดที่ {place} รีบไปซื้อด่วน!",
    "💰 ใครกำลังหาลูกสูบอยู่ ตอนนี้เกิดแล้วนะ ไปตำกันได้เลย!"
]

@app.route('/piston', methods=['POST'])
def piston():
    data = request.json or {}
    name = data.get("name", "ลูกสูบ")
    place = data.get("place", "ร้านค้ากลาง")
    msg = random.choice(MESSAGES).format(name=name, place=place)
    async def send():
        ch = bot.get_channel(CHANNEL_ID)
        if ch:
            e = discord.Embed(title="🔧 ร้านลูกสูบเกิดแล้ว!", description=msg + f"\n\n**ของ:** {name}\n**จุดเกิด:** {place}", color=0xFFD700)
            e.set_footer(text="MAHANAKHON RACING • AI Bot")
            await ch.send(embed=e)
    bot.loop.create_task(send())
    return {"ok": True}

@app.route('/')
def home():
    return "Bot Online!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask).start()
bot.run(TOKEN)
