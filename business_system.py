
from discord.ext import commands, tasks
import discord
import json
import os

USERS_PATH = "data/users.json"
BUSINESSES_PATH = "data/businesses.json"

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_PATH, "w") as f:
        json.dump(data, f, indent=4)

def load_businesses():
    if not os.path.exists(BUSINESSES_PATH):
        return {}
    with open(BUSINESSES_PATH, "r") as f:
        return json.load(f)

def save_businesses(data):
    with open(BUSINESSES_PATH, "w") as f:
        json.dump(data, f, indent=4)

class BusinessSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.income_loop.start()

    @commands.command()
    async def buybusiness(self, ctx, *, name):
        user_id = str(ctx.author.id)
        users = load_users()
        businesses = load_businesses()

        if user_id not in users:
            return await ctx.send("Ты не зарегистрирован.")
        if name in businesses:
            return await ctx.send("Этот бизнес уже куплен.")
        if users[user_id]["money"] < 3000:
            return await ctx.send("Для покупки бизнеса нужно минимум 3000$.")

        users[user_id]["money"] -= 3000
        businesses[name] = {"owner": user_id, "profit": 150}
        save_users(users)
        save_businesses(businesses)
        await ctx.send(f"Ты купил бизнес **{name}**. Прибыль: 150$ каждые 10 минут.")

    @commands.command()
    async def mybusiness(self, ctx):
        user_id = str(ctx.author.id)
        businesses = load_businesses()
        owned = [name for name, data in businesses.items() if data["owner"] == user_id]
        if not owned:
            await ctx.send("У тебя нет бизнесов.")
        else:
            await ctx.send("Твои бизнесы: " + ", ".join(owned))

    @tasks.loop(minutes=10)
    async def income_loop(self):
        users = load_users()
        businesses = load_businesses()
        for name, data in businesses.items():
            owner = data["owner"]
            profit = data["profit"]
            if owner in users:
                users[owner]["money"] += profit
        save_users(users)

async def setup(bot):
    await bot.add_cog(BusinessSystem(bot))
