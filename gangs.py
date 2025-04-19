
from discord.ext import commands
import discord
import json
import os

USERS_PATH = "data/users.json"
GANGS = {
    "Backwoods": {"color": "green"},
    "Bloods": {"color": "red"},
    "Crips": {"color": "blue"},
    "Vagos": {"color": "yellow"}
}

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_PATH, "w") as f:
        json.dump(data, f, indent=4)

class Gangs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gangs(self, ctx):
        embed = discord.Embed(title="Доступные банды", color=discord.Color.dark_gold())
        for gang in GANGS:
            embed.add_field(name=gang, value=f"Цвет: {GANGS[gang]['color']}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def joingang(self, ctx, *, name):
        name = name.title()
        if name not in GANGS:
            return await ctx.send("Такой банды нет.")
        users = load_users()
        uid = str(ctx.author.id)
        if uid not in users:
            return await ctx.send("Вы не зарегистрированы.")
        users[uid]["gang"] = name
        save_users(users)
        await ctx.send(f"{ctx.author.mention}, теперь вы состоите в банде **{name}**.")

    @commands.command()
    async def mygang(self, ctx):
        users = load_users()
        uid = str(ctx.author.id)
        gang = users[uid].get("gang")
        if gang:
            await ctx.send(f"Ты в банде: **{gang}**")
        else:
            await ctx.send("Ты не состоишь в банде.")

    @commands.command()
    async def leavegang(self, ctx):
        users = load_users()
        uid = str(ctx.author.id)
        if "gang" in users[uid]:
            del users[uid]["gang"]
            save_users(users)
            await ctx.send("Ты вышел из банды.")
        else:
            await ctx.send("Ты не в банде.")

async def setup(bot):
    await bot.add_cog(Gangs(bot))
