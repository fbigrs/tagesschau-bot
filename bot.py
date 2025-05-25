import discord
import aiohttp
import asyncio
import json
import os
import logging
from dotenv import load_dotenv

# 🔐 .env laden
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
ROLE_ID = os.getenv('DISCORD_ROLE_ID')
API_URL = 'https://www.tagesschau.de/api2u/homepage'
SAVE_FILE = 'last_ids.json'

# 🪵 Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
last_posted_ids = set()

def load_last_ids():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return set(data.get("posted_ids", []))
    return set()

def save_last_ids(id_set):
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump({"posted_ids": list(id_set)}, f, ensure_ascii=False, indent=2)

async def fetch_eilmeldungen():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as resp:
            if resp.status == 200:
                data = await resp.json()
                return [
                    n for n in data.get('news', [])
                    if any(tag.get('tag', '').lower() == 'eilmeldung' for tag in n.get('tags', []))
                ]
            logging.warning(f"API antwortete mit Statuscode {resp.status}")
            return []

async def check_for_updates():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    global last_posted_ids

    last_posted_ids = load_last_ids()

    while not client.is_closed():
        try:
            meldungen = await fetch_eilmeldungen()
            new_meldungen = [m for m in meldungen if m['sophoraId'] not in last_posted_ids]

            for meldung in reversed(new_meldungen):
                embed = discord.Embed(
                    title=f"🛑 {meldung['title']}",
                    description=meldung.get('firstSentence', 'Keine Vorschau verfügbar.'),
                    url=meldung.get('shareURL', 'https://www.tagesschau.de/'),
                    color=0xD7263D
                )
                embed.set_footer(text="Quelle: tagesschau.de")
                embed.timestamp = discord.utils.parse_time(meldung.get("date", None))

                image_url = meldung.get("teaserImage", {}).get("imageVariants", {}).get("16x9-640")
                if image_url:
                    embed.set_image(url=image_url)

                # Role mention hinzufügen
                role_mention = f"<@&{ROLE_ID}>" if ROLE_ID else ""
                await channel.send(content=role_mention, embed=embed)
                last_posted_ids.add(meldung['sophoraId'])
                save_last_ids(last_posted_ids)
                logging.info(f"Gepostet: {meldung['title']}")

            await asyncio.sleep(60)
        except Exception as e:
            logging.error(f"Fehler beim Posten der Eilmeldungen: {e}")
            await asyncio.sleep(60)

@client.event
async def on_ready():
    logging.info(f'Bot gestartet als {client.user.name}')
    client.loop.create_task(check_for_updates())

client.run(TOKEN)
