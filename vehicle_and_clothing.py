
from discord.ext import commands
import discord
import json
import os
import random

USERS_PATH = "data/users.json"
VEHICLES = {
    "BMW M5": 55000,
    "Mercedes S63": 70000,
    "Toyota Supra": 45000,
    "Lamborghini Aventador": 120000,
    "Audi RS7": 60000
}

CLOTHES = {
    "Nike Hoodie": 300,
    "Adidas Tracksuit": 250,
    "Supreme T-Shirt": 500,
    "Gucci Jacket": 2000,
    "Balenciaga Sneakers": 1500
}

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=4)

class VehiclesClothing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cars(self, ctx):
        embed = discord.Embed(title="Автосалон", description="Список доступных машин:")
        for name, price in VEHICLES.items():
            embed.add_field(name=name, value=f"${price}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def buycar(self, ctx, *, car_name):
        users = load_users()
        user_id = str(ctx.author.id)

        if car_name not in VEHICLES:
            await ctx.send("Такой машины нет в продаже.")
            return

        price = VEHICLES[car_name]
        if users[user_id]["balance"] < price:
            await ctx.send("Недостаточно средств.")
            return

        users[user_id]["balance"] -= price
        users[user_id].setdefault("cars", []).append(car_name)
        save_users(users)

        await ctx.send(f"{ctx.author.mention}, ты купил {car_name} за ${price}!")

    @commands.command()
    async def mycars(self, ctx):
        users = load_users()
        user_id = str(ctx.author.id)
        cars = users[user_id].get("cars", [])

        if not cars:
            await ctx.send("У тебя нет машин.")
            return

        embed = discord.Embed(title="Твои машины", description="
".join(cars))
        await ctx.send(embed=embed)

    @commands.command()
    async def clothing(self, ctx):
        embed = discord.Embed(title="Магазин одежды", description="Выбирай стиль:")
        for name, price in CLOTHES.items():
            embed.add_field(name=name, value=f"${price}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def buyclothes(self, ctx, *, item_name):
        users = load_users()
        user_id = str(ctx.author.id)

        if item_name not in CLOTHES:
            await ctx.send("Такой одежды нет в продаже.")
            return

        price = CLOTHES[item_name]
        if users[user_id]["balance"] < price:
            await ctx.send("Недостаточно средств.")
            return

        users[user_id]["balance"] -= price
        users[user_id].setdefault("clothes", []).append(item_name)
        users[user_id]["outfit"] = item_name
        save_users(users)

        await ctx.send(f"{ctx.author.mention}, ты купил {item_name} за ${price} и надел её!")

    @commands.command()
    async def outfit(self, ctx):
        users = load_users()
        user_id = str(ctx.author.id)
        outfit = users[user_id].get("outfit")

        if not outfit:
            await ctx.send("Ты пока ничего не надел.")
            return

        await ctx.send(f"{ctx.author.mention}, твоя текущая одежда: {outfit}")

async def setup(bot):
    await bot.add_cog(VehiclesClothing(bot))
