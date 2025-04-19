
from discord.ext import commands
import discord
import json
import os
from utils.image_generator import generate_profile_image

USERS_PATH = "data/users.json"

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx):
        users = load_users()
        user_id = str(ctx.author.id)
        if user_id not in users:
            await ctx.send("Ты ещё не начал играть.")
            return
        user_data = users[user_id]
        path = generate_profile_image(user_data)
        file = discord.File(path, filename="profile.png")
        embed = discord.Embed(title=f"Профиль {ctx.author.display_name}")
        embed.set_image(url="attachment://profile.png")
        await ctx.send(file=file, embed=embed)

async def setup(bot):
    await bot.add_cog(Profile(bot))
