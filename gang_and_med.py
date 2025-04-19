
from discord.ext import commands
import discord
import json
import os
import random

USERS_PATH = "data/users.json"

BANDS = {
    "grove": {"name": "Grove Street", "color": 0x00ff00},
    "ballas": {"name": "Ballas", "color": 0xff00ff},
    "vagos": {"name": "Vagos", "color": 0xffff00}
}

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=4)

class GangAndMed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joingang(self, ctx, gang_name: str):
        users = load_users()
        user_id = str(ctx.author.id)
        gang_name = gang_name.lower()

        if gang_name not in BANDS:
            await ctx.send("Такой банды нет.")
            return
        if user_id not in users:
            await ctx.send("Ты ещё не начал игру.")
            return

        users[user_id]["gang"] = gang_name
        save_users(users)
        await ctx.send(f"{ctx.author.mention}, ты вступил в банду **{BANDS[gang_name]['name']}**.")

    @commands.command()
    async def gang(self, ctx):
        users = load_users()
        user_id = str(ctx.author.id)
        gang = users.get(user_id, {}).get("gang")
        if gang:
            info = BANDS.get(gang)
            embed = discord.Embed(title="Твоя банда", description=info["name"], color=info["color"])
            await ctx.send(embed=embed)
        else:
            await ctx.send("Ты не состоишь в банде.")

    @commands.command()
    async def heal(self, ctx):
        users = load_users()
        user_id = str(ctx.author.id)
        if user_id not in users:
            await ctx.send("Ты ещё не начал игру.")
            return
        cost = 100
        if users[user_id]["balance"] < cost:
            await ctx.send("Недостаточно средств на лечение.")
            return
        users[user_id]["balance"] -= cost
        save_users(users)
        await ctx.send(f"{ctx.author.mention}, ты вылечился за ${cost}.")

    @commands.command()
    async def lawyer(self, ctx, member: discord.Member):
        users = load_users()
        user_id = str(member.id)
        if user_id in users and users[user_id].get("jailed", False):
            chance = random.randint(1, 100)
            if chance <= 50:
                users[user_id]["jailed"] = False
                result = "успешно освободил"
            else:
                result = "не смог освободить"
            save_users(users)
            await ctx.send(f"{ctx.author.mention} {result} {member.mention} из тюрьмы.")
        else:
            await ctx.send("Этот человек не находится в тюрьме.")

async def setup(bot):
    await bot.add_cog(GangAndMed(bot))
