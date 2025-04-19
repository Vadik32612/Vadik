
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

class Medicine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def health(self, ctx):
        users = load_users()
        uid = str(ctx.author.id)
        hp = users.get(uid, {}).get("health", 100)
        await ctx.send(f"Здоровье: {hp}/100")

    @commands.command()
    async def heal(self, ctx):
        users = load_users()
        uid = str(ctx.author.id)
        if users.get(uid, {}).get("balance", 0) < 100:
            return await ctx.send("Недостаточно средств на лечение. Стоимость: $100")
        users[uid]["balance"] -= 100
        users[uid]["health"] = 100
        save_users(users)
        await ctx.send("Вы вылечились. Здоровье восстановлено.")

    @commands.command()
    async def damage(self, ctx, amount: int):
        users = load_users()
        uid = str(ctx.author.id)
        users.setdefault(uid, {})
        users[uid]["health"] = max(0, users[uid].get("health", 100) - amount)
        save_users(users)
        await ctx.send(f"Вы получили урон: -{amount} HP")

    @commands.command()
    async def pharmacy(self, ctx):
        await ctx.send("Добро пожаловать в аптеку! Используй `!heal` для лечения ($100)")

async def setup(bot):
    await bot.add_cog(Medicine(bot))
