from dscl.runtime import *
from dscl.discord import *
from dscl.discord.ui import *
import random
fish_bot = Bot(prefix="!", intents=Intents(message_content=True))
@fish_bot.slash_command
async def inv(this):
  user = str(this.user.id)
  inv = caught[user]
  text = ""
  for fish in inv:
    text += fish + "\n"
  this.respond(view=View(Container(Text("Your inventory:"), Text(text), color=Colors.Red)))
@fish_bot.slash_command
async def fish(this, amount_to_fish: Number):
  fishes_caught = Table()
  for fish in range(0, amount_to_fish):
    fishes_caught.append(random.choice(fishes))
  fishes_text = range("\n", join(fishes_caught))
  Again = Button("Fish again")
  def lamdba_1(this: Context):
    await fish(this)
  Again.callback = lamdba_1
  this.respond(view=View(Container(Text("You caught these:"), Text(fishes), Row(Again), color=Colors.Green)))
fish_bot.run("Mtwdksnndncjjfnee.cdjejsjff.ehhes")
