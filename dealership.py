
from discord.ext import commands
import discord
import json
import os

USERS_PATH = "data/users.json"
CARS = {
    "BMW M5": 60000,
    "Mercedes-Benz G63": 120000,
    "Toyota Supra": 50000,
    "Nissan GT-R": 95000,
    "Tesla Model S": 80000,
    "Lamborghini Huracan": 200000
}

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_PATH, "w") as f:
        json.dump(data, f, indent=4)

class Dealership(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cars(self, ctx):
        embed = discord.Embed(title="Автосалон", color=discord.Color.blue())
        for name, price in CARS.items():
            embed.add_field(name=name, value=f"${price}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def buycar(self, ctx, *, car_name):
        users = load_users()
        uid = str(ctx.author.id)
        car_name = car_name.title()
        if car_name not in CARS:
            return await ctx.send("Такой машины нет в автосалоне.")
        price = CARS[car_name]
        if users[uid]["balance"] < price:
            return await ctx.send("Недостаточно средств.")
        users[uid]["balance"] -= price
        users[uid].setdefault("cars", []).append(car_name)
        save_users(users)
        await ctx.send(f"{ctx.author.mention}, вы купили {car_name} за ${price}")

    @commands.command()
    async def mycars(self, ctx):
        users = load_users()
        uid = str(ctx.author.id)
        cars = users[uid].get("cars", [])
        if not cars:
            await ctx.send("У тебя нет машин.")
        else:
            await ctx.send("Твои машины: " + ", ".join(cars))

async def setup(bot):
    await bot.add_cog(Dealership(bot))
