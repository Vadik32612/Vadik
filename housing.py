
from discord.ext import commands
import discord
import json
import os
import random

USERS_PATH = "data/users.json"
HOUSES = {
    "Квартира в центре": 50000,
    "Дом на окраине": 30000,
    "Вилла у моря": 150000,
    "Пентхаус": 200000
}

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_PATH, "w") as f:
        json.dump(data, f, indent=4)

class Housing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def houses(self, ctx):
        embed = discord.Embed(title="Рынок недвижимости", color=discord.Color.orange())
        for name, price in HOUSES.items():
            embed.add_field(name=name, value=f"${price}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def buyhouse(self, ctx, *, name):
        users = load_users()
        uid = str(ctx.author.id)
        name = name.title()
        if name not in HOUSES:
            return await ctx.send("Такого дома нет.")
        price = HOUSES[name]
        if users[uid]["balance"] < price:
            return await ctx.send("Недостаточно средств.")
        users[uid]["balance"] -= price
        users[uid]["house"] = name
        save_users(users)
        await ctx.send(f"{ctx.author.mention}, вы купили дом: {name} за ${price}")

    @commands.command()
    async def myhouse(self, ctx):
        users = load_users()
        uid = str(ctx.author.id)
        house = users[uid].get("house")
        if house:
            await ctx.send(f"Твой дом: {house}")
        else:
            await ctx.send("У тебя нет дома.")

    @commands.command()
    async def auction(self, ctx):
        item = random.choice(list(HOUSES.keys()))
        price = int(HOUSES[item] * random.uniform(0.5, 1.2))
        await ctx.send(f"Аукцион: {item} — начальная цена: ${price}. Напиши `!bid {price}` чтобы сделать ставку.")

    @commands.command()
    async def bid(self, ctx, price: int):
        users = load_users()
        uid = str(ctx.author.id)
        if users[uid]["balance"] < price:
            return await ctx.send("Недостаточно средств для ставки.")
        users[uid]["balance"] -= price
        users[uid]["house"] = "Аукционный дом"
        save_users(users)
        await ctx.send(f"{ctx.author.mention}, ты выиграл дом на аукционе за ${price}!")

async def setup(bot):
    await bot.add_cog(Housing(bot))
