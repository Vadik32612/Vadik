
from discord.ext import commands
import discord
import json
import os

USERS_PATH = "data/users.json"
CARS_PATH = "data/cars.json"

REAL_CARS = {
    "bmw_m5": {"name": "BMW M5", "price": 80000},
    "audi_rs6": {"name": "Audi RS6", "price": 90000},
    "mercedes_amg": {"name": "Mercedes-AMG", "price": 95000},
    "toyota_supra": {"name": "Toyota Supra", "price": 60000},
    "nissan_gtr": {"name": "Nissan GT-R", "price": 85000}
}

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=4)

class Cars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dealership(self, ctx):
        embed = discord.Embed(title="Автосалон", description="Доступные машины для покупки")
        for key, car in REAL_CARS.items():
            embed.add_field(name=car["name"], value=f"Цена: ${car['price']} | Код: {key}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def buycar(self, ctx, car_key: str):
        users = load_users()
        user_id = str(ctx.author.id)

        if user_id not in users:
            await ctx.send("Ты ещё не начал игру.")
            return

        car = REAL_CARS.get(car_key.lower())
        if not car:
            await ctx.send("Такой машины нет.")
            return

        if users[user_id]["balance"] < car["price"]:
            await ctx.send("Недостаточно денег на покупку.")
            return

        users[user_id]["balance"] -= car["price"]
        users[user_id].setdefault("cars", []).append(car["name"])
        save_users(users)

        await ctx.send(f"{ctx.author.mention}, ты купил {car['name']} за ${car['price']}.")

    @commands.command()
    async def mycars(self, ctx):
        users = load_users()
        user_id = str(ctx.author.id)
        if user_id not in users:
            await ctx.send("Ты ещё не начал игру.")
            return
        cars = users[user_id].get("cars", [])
        if not cars:
            await ctx.send("У тебя нет машин.")
        else:
            embed = discord.Embed(title="Твои машины", description="\n".join(cars))
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Cars(bot))
