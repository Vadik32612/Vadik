
from discord.ext import commands
import discord
import json
import os
from datetime import datetime, timedelta

USERS_PATH = "data/users.json"

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=4)

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_user(self, user_id):
        users = load_users()
        user_id = str(user_id)
        if user_id not in users:
            users[user_id] = {
                "balance": 1000,
                "last_daily": None,
                "job": None,
                "bank": 0,
                "clothes": [],
                "gang": None,
                "gender": "male",
                "id": user_id
            }
            save_users(users)
        return users[user_id], users

    @commands.command()
    async def balance(self, ctx):
        user_data, _ = self.get_user(ctx.author.id)
        await ctx.send(f"{ctx.author.mention}, у тебя **${user_data['balance']}** на руках и **${user_data['bank']}** в банке.")

    @commands.command()
    async def daily(self, ctx):
        user_data, users = self.get_user(ctx.author.id)
        now = datetime.now()
        if user_data["last_daily"]:
            last = datetime.fromisoformat(user_data["last_daily"])
            if now - last < timedelta(hours=24):
                remaining = timedelta(hours=24) - (now - last)
                await ctx.send(f"{ctx.author.mention}, ты уже получал ежедневную награду. Приходи через {remaining}.")
                return

        user_data["balance"] += 200
        user_data["last_daily"] = now.isoformat()
        save_users(users)
        await ctx.send(f"{ctx.author.mention}, ты получил ежедневные **$200**!")

    @commands.command()
    async def work(self, ctx):
        user_data, users = self.get_user(ctx.author.id)
        job = user_data["job"] or "строитель"
        earnings = 100
        user_data["balance"] += earnings
        save_users(users)
        await ctx.send(f"{ctx.author.mention}, ты поработал как **{job}** и заработал **${earnings}**!")

    @commands.command()
    async def deposit(self, ctx, amount: int):
        user_data, users = self.get_user(ctx.author.id)
        if user_data["balance"] < amount:
            await ctx.send(f"{ctx.author.mention}, у тебя недостаточно денег.")
            return
        user_data["balance"] -= amount
        user_data["bank"] += amount
        save_users(users)
        await ctx.send(f"{ctx.author.mention}, ты положил **${amount}** в банк.")

    @commands.command()
    async def withdraw(self, ctx, amount: int):
        user_data, users = self.get_user(ctx.author.id)
        if user_data["bank"] < amount:
            await ctx.send(f"{ctx.author.mention}, у тебя недостаточно средств в банке.")
            return
        user_data["bank"] -= amount
        user_data["balance"] += amount
        save_users(users)
        await ctx.send(f"{ctx.author.mention}, ты снял **${amount}** с банковского счёта.")

async def setup(bot):
    await bot.add_cog(Economy(bot))
