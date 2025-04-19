
from discord.ext import commands
import discord
import json
import os
import random

USERS_PATH = "data/users.json"
JAIL_PATH = "data/jail.json"
TAX_RATE = 0.05

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_PATH, "w") as f:
        json.dump(data, f, indent=4)

def load_jail():
    if not os.path.exists(JAIL_PATH):
        with open(JAIL_PATH, "w") as f:
            json.dump({}, f)
    with open(JAIL_PATH, "r") as f:
        return json.load(f)

def save_jail(data):
    with open(JAIL_PATH, "w") as f:
        json.dump(data, f, indent=4)

class Law(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def arrest(self, ctx, member: discord.Member, *, reason="Не указано"):
        jail = load_jail()
        jail[str(member.id)] = reason
        save_jail(jail)
        await ctx.send(f"{member.mention} был арестован. Причина: {reason}")

    @commands.command()
    async def jail(self, ctx, member: discord.Member = None):
        jail = load_jail()
        target = member or ctx.author
        reason = jail.get(str(target.id))
        if reason:
            await ctx.send(f"{target.mention} в тюрьме. Причина: {reason}")
        else:
            await ctx.send(f"{target.mention} на свободе.")

    @commands.command()
    async def release(self, ctx, member: discord.Member):
        jail = load_jail()
        if str(member.id) in jail:
            del jail[str(member.id)]
            save_jail(jail)
            await ctx.send(f"{member.mention} был освобождён.")
        else:
            await ctx.send("Этот человек не в тюрьме.")

    @commands.command()
    async def tax(self, ctx):
        users = load_users()
        uid = str(ctx.author.id)
        if uid not in users:
            return await ctx.send("Ты не зарегистрирован.")
        tax = int(users[uid]["balance"] * TAX_RATE)
        users[uid]["balance"] -= tax
        save_users(users)
        await ctx.send(f"С тебя списано налогов: ${tax}")

    @commands.command()
    async def join_gang(self, ctx, *, gang_name):
        users = load_users()
        uid = str(ctx.author.id)
        users[uid]["gang"] = gang_name
        save_users(users)
        await ctx.send(f"{ctx.author.mention} вступил в банду: **{gang_name}**")

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
    async def court(self, ctx, member: discord.Member, *, reason):
        verdict = random.choice(["Виновен", "Оправдан"])
        await ctx.send(f"Суд над {member.mention} завершён. Вердикт: **{verdict}**. Причина: {reason}")

async def setup(bot):
    await bot.add_cog(Law(bot))
