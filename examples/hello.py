from discord.ext import commands
from discord import Intents
import random
intents = Intents()
prefix = "!"
TOKEN = "MY_VERY_SECRET_TOKEN"
intents.on_messages=True
bot = Bot(
  prefix, 
  intents
)
@bot.slash_command
async def hello(this, person: discord.Member):
@bot.slash_command
async def roll_dice(this, min: int, max: int):
  number = random.randint(min, max)
  this.respond("Your random number is: %s" % number)
bot.run(TOKEN)
