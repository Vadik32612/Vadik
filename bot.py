import discord
from discord.ext import commands
import config

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

extensions = ['commands.economy', 'commands.crime', 'commands.justice', 'commands.profile', 'commands.shop']

for ext in extensions:
    bot.load_extension(ext)

bot.run(config.TOKEN)
