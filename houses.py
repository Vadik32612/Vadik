
from discord.ext import commands
import discord
import json
import os
import random

USERS_PATH = "data/users.json"
HOUSES_PATH = "data/houses.json"

HOUSE_LIST = {
    "Дом у озера": 10000,
    "Квартира в центре": 20000,
    "Вилла на холме": 50000,
    "Пентхаус в городе": 80000,
    "Особняк": 120000
}

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=4)

def load_houses():
    if not os.path.exists(HOUSES_PATH):
        with open(HOUSES_PATH, "w") as f:
            json.dump({}, f)
    with open(HOUSES_PATH, "r") as f:
        return json.load(f)

def save_houses(houses):
    with open(HOUSES_PATH, "w") as f:
        json.dump(houses, f, indent=4)

class Houses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def houses(self, ctx):
        embed = discord.Embed(title="Недвижимость", description="Доступные дома:")
        for name, price in HOUSE_LIST.items():
            embed.add_field(name=name, value=f"${price}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def buyhouse(self, ctx, *, house_name):
        users = load_users()
        houses = load_houses()
        user_id = str(ctx.author.id)

        if house_name not in HOUSE_LIST:
            await ctx.send("Такого дома нет.")
            return

        price = HOUSE_LIST[house_name]
        if users[user_id]["balance"] < price:
            await ctx.send("Недостаточно средств.")
            return

        if user_id in houses:
            await ctx.send("У тебя уже есть дом.")
            return

        users[user_id]["balance"] -= price
        houses[user_id] = house_name

        save_users(users)
        save_houses(houses)

        await ctx.send(f"{ctx.author.mention}, ты купил: **{house_name}** за ${price}")

    @commands.command()
    async def myhouse(self, ctx):
        houses = load_houses()
        user_id = str(ctx.author.id)

        house = houses.get(user_id)
        if house:
            await ctx.send(f"{ctx.author.mention}, твой дом: **{house}**")
        else:
            await ctx.send("У тебя пока нет дома.")

    @commands.command()
    async def sellhouse(self, ctx):
        users = load_users()
        houses = load_houses()
        user_id = str(ctx.author.id)

        if user_id not in houses:
            await ctx.send("У тебя нет дома для продажи.")
            return

        house_name = houses[user_id]
        refund = HOUSE_LIST.get(house_name, 0) // 2
        users[user_id]["balance"] += refund
        del houses[user_id]

        save_users(users)
        save_houses(houses)

        await ctx.send(f"{ctx.author.mention}, ты продал **{house_name}** за ${refund}")

async def setup(bot):
    await bot.add_cog(Houses(bot))
