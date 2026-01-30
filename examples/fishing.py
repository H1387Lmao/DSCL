from dscl.runtime import *
from dscl.discord import *
from dscl.discord.ui import *
import random
fishes = Table("cod", "salmon", "pufferfish")
caught = UserDatabase()
fish_bot = Bot(prefix="!", intents=Intents(message_content=True))
@fish_bot.slash_command(name='inv')
async def inv(this):
  user = str(this.user.id)
  inv = caught[user]
  text = ""
  for fish in inv:
    text += fish + "\n"
  this.respond(view=View(Container(Text("Your inventory:"), Text(text), color=Colors.Red)))
@fish_bot.slash_command(name='fish')
async def fish(this, amount_to_fish: int):
  fishes_caught = Table()
  for fish in 0.amount_to_fish:
    fishes_caught.append(random.choice(fishes))
  fishes_text = "\n".join(fishes_caught)
  async def lamdba_1(this: Context):
    await fish(this)
  this.respond(view=View(Container(Text("You caught these:"), Text(fishes), Row(Button("Fish Again", callback=lamdba_1)), color=Colors.Green)))
fish_bot.run("Mtwdksnndncjjfnee.cdjejsjff.ehhes")
