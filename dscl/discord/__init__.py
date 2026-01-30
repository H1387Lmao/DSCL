from discord.ext import bridge
import discord

class Intents(discord.Intents):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Bot(bridge.Bot):
    def __init__(self, prefix="!", intents=Intents()):
        super().__init__(
            command_prefix=prefix,
            intents=intents
        )
