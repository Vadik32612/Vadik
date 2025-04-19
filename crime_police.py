
from discord.ext import commands, tasks
import discord
import json
import os
import random

USERS_PATH = "data/users.json"

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_PATH, "w") as f:
        json.dump(data, f, indent=4)

class CrimePolice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.crime_decay.start()

    @commands.command()
    async def crime(self, ctx):
        uid = str(ctx.author.id)
        users = load_users()
        if uid not in users:
            return await ctx.send("Ты не зарегистрирован.")
        chance = random.randint(1, 100)
        if chance <= 60:
            amount = random.randint(100, 500)
            users[uid]["money"] += amount
            users[uid]["wanted"] = users[uid].get("wanted", 0) + 1
            save_users(users)
            await ctx.send(f"Ты совершил преступление и заработал {amount}$! Уровень розыска: {users[uid]['wanted']}")
        else:
            users[uid]["jailed"] = True
            users[uid]["wanted"] = 0
            save_users(users)
            await ctx.send("Тебя поймала полиция. Ты попал в тюрьму.")

    @commands.command()
    async def wanted(self, ctx):
        uid = str(ctx.author.id)
        users = load_users()
        level = users.get(uid, {}).get("wanted", 0)
        await ctx.send(f"Твой уровень розыска: {level}")

    @commands.command()
    async def jailstatus(self, ctx):
        uid = str(ctx.author.id)
        users = load_users()
        if users.get(uid, {}).get("jailed", False):
            await ctx.send("Ты находишься в тюрьме.")
        else:
            await ctx.send("Ты на свободе.")

    @commands.command()
    async def release(self, ctx):
        uid = str(ctx.author.id)
        users = load_users()
        if users.get(uid, {}).get("jailed", False):
            users[uid]["jailed"] = False
            save_users(users)
            await ctx.send("Ты освобождён из тюрьмы.")
        else:
            await ctx.send("Ты не в тюрьме.")

    @tasks.loop(minutes=30)
    async def crime_decay(self):
        users = load_users()
        changed = False
        for uid in users:
            if users[uid].get("wanted", 0) > 0:
                users[uid]["wanted"] -= 1
                changed = True
        if changed:
            save_users(users)

async def setup(bot):
    await bot.add_cog(CrimePolice(bot))
