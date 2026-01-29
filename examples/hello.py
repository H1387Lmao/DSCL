from dscl.runtime import *
from dscl.discord import *
import random
intents = Intents()
prefix = "!"
TOKEN = "MY_VERY_SECRET_TOKEN"
intents.message_content = True
bot = Bot(
  prefix, 
  intents
)
@bot.slash_command
async def hello(this, personUser):
  if (person.bot):
    this.respond("Hi fellow bot!")
  else:
    this.respond("Hi%s" % person)
@bot.slash_command
async def roll_dice(this, min: int, max: int):
  number = random.randint(min, max)
  this.respond("Your random number is: %s" % number)
bot.run(TOKEN)
