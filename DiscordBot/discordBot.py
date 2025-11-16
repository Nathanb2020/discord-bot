import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True  # Needed to get member info

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- CONFIGURATION ----------
AUDIO_FILE = "join_Sound.mp3"  # Make sure this file is in the same folder
PLAY_AUDIO = False               # <-- Set to False to disable audio
TEXT_CHANNEL_ID = 1439333025862127699  # Replace with your text channel ID
# -----------------------------------

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    # Ignore bots
    if member.bot:
        return

    # Detect user joining a voice channel
    if before.channel is None and after.channel is not None:
        channel = after.channel

        try:
            # Send message to text channel
            text_channel = bot.get_channel(TEXT_CHANNEL_ID)
            if text_channel:
                await text_channel.send(f"{member.display_name} has joined {channel.name}!")

            # Only play audio if toggle is True
            if PLAY_AUDIO:
                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio(AUDIO_FILE))

                while vc.is_playing():
                    await asyncio.sleep(0.1)

                await vc.disconnect()

        except Exception as e:
            print("Error while processing voice join:", e)

# ---- Put your bot token here ----
bot.run(os.getenv("DISCORD_TOKEN"))

