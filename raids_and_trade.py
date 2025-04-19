
from discord.ext import commands
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

class RaidsAndTrade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def raid(self, ctx, target: discord.Member):
        attacker = str(ctx.author.id)
        defender = str(target.id)
        users = load_users()

        if attacker not in users or defender not in users:
            return await ctx.send("Один из пользователей не зарегистрирован.")
        if users[attacker].get("gang") is None or users[defender].get("gang") is None:
            return await ctx.send("Оба игрока должны состоять в бандах.")

        chance = random.randint(1, 100)
        if chance <= 50:
            stolen = random.randint(100, 500)
            users[attacker]["money"] += stolen
            users[defender]["money"] = max(0, users[defender]["money"] - stolen)
            save_users(users)
            await ctx.send(f"Рейд успешен! {ctx.author.mention} украл {stolen}$ у {target.mention}.")
        else:
            await ctx.send("Рейд провалился. Полиция была на месте.")

    @commands.command()
    async def trade(self, ctx, member: discord.Member, amount: int):
        sender = str(ctx.author.id)
        receiver = str(member.id)
        users = load_users()

        if sender not in users or receiver not in users:
            return await ctx.send("Один из пользователей не зарегистрирован.")
        if users[sender]["money"] < amount:
            return await ctx.send("Недостаточно денег для сделки.")

        users[sender]["money"] -= amount
        users[receiver]["money"] += amount
        save_users(users)
        await ctx.send(f"{ctx.author.mention} передал {amount}$ {member.mention} в сделке.")

async def setup(bot):
    await bot.add_cog(RaidsAndTrade(bot))
