
from discord.ext import commands, tasks
import discord
import json
import os
import random
import time

USERS_PATH = "data/users.json"
JAILED_PATH = "data/jailed.json"

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=4)

def load_jailed():
    if not os.path.exists(JAILED_PATH):
        return {}
    with open(JAILED_PATH, "r") as f:
        return json.load(f)

def save_jailed(jailed):
    with open(JAILED_PATH, "w") as f:
        json.dump(jailed, f, indent=4)

class Law(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tax_collector.start()
        self.jail_checker.start()

    @commands.command()
    async def tax(self, ctx):
        users = load_users()
        user_id = str(ctx.author.id)
        if user_id not in users:
            await ctx.send("Ты ещё не начал игру.")
            return

        tax_amount = int(users[user_id]["balance"] * 0.05)
        users[user_id]["balance"] -= tax_amount
        save_users(users)

        await ctx.send(f"{ctx.author.mention}, с тебя взяли налог в размере ${tax_amount} (5%).")

    @tasks.loop(hours=24)
    async def tax_collector(self):
        users = load_users()
        for user_id in users:
            tax_amount = int(users[user_id]["balance"] * 0.05)
            users[user_id]["balance"] -= tax_amount
        save_users(users)

    @commands.command()
    async def jail(self, ctx, member: discord.Member, *, reason="Без причины"):
        jailed = load_jailed()
        users = load_users()
        user_id = str(member.id)

        if user_id not in users:
            await ctx.send("Пользователь не зарегистрирован в игре.")
            return

        jailed[user_id] = {"reason": reason, "release": int(time.time()) + 300}
        save_jailed(jailed)

        await ctx.send(f"{member.mention} посажен в тюрьму. Причина: {reason} (5 минут)")

    @commands.command()
    async def release(self, ctx, member: discord.Member):
        jailed = load_jailed()
        user_id = str(member.id)

        if user_id not in jailed:
            await ctx.send("Этот пользователь не в тюрьме.")
            return

        del jailed[user_id]
        save_jailed(jailed)

        await ctx.send(f"{member.mention} выпущен из тюрьмы.")

    @commands.command()
    async def myjail(self, ctx):
        jailed = load_jailed()
        user_id = str(ctx.author.id)

        if user_id not in jailed:
            await ctx.send("Ты не в тюрьме.")
            return

        remaining = jailed[user_id]["release"] - int(time.time())
        await ctx.send(f"Ты в тюрьме. Осталось секунд: {max(0, remaining)}. Причина: {jailed[user_id]['reason']}.")

    @tasks.loop(seconds=60)
    async def jail_checker(self):
        jailed = load_jailed()
        changed = False
        now = int(time.time())

        for user_id in list(jailed.keys()):
            if jailed[user_id]["release"] <= now:
                del jailed[user_id]
                changed = True

        if changed:
            save_jailed(jailed)

async def setup(bot):
    await bot.add_cog(Law(bot))
