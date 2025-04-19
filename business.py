
from discord.ext import commands, tasks
import discord
import json
import os

USERS_PATH = "data/users.json"
BUSINESSES = {
    "kfc": {"price": 3000, "income": 150, "name": "KFC"},
    "barbershop": {"price": 2000, "income": 100, "name": "Барбершоп"},
    "gas_station": {"price": 4000, "income": 200, "name": "Заправка"}
}

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=4)

class Business(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.passive_income.start()

    @commands.command()
    async def businesses(self, ctx):
        embed = discord.Embed(title="Бизнесы", description="Доступные для покупки бизнесы:")
        for key, info in BUSINESSES.items():
            embed.add_field(name=info["name"], value=f"Цена: ${info['price']} — Доход: ${info['income']} в 10 мин — `!buybiz {key}`", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def buybiz(self, ctx, business_key: str):
        users = load_users()
        user_id = str(ctx.author.id)
        business_key = business_key.lower()
        if user_id not in users:
            await ctx.send("Ты ещё не начал игру.")
            return
        if business_key not in BUSINESSES:
            await ctx.send("Такого бизнеса нет.")
            return
        user = users[user_id]
        business = BUSINESSES[business_key]
        if user["balance"] < business["price"]:
            await ctx.send("Недостаточно денег для покупки.")
            return
        if "businesses" not in user:
            user["businesses"] = []
        if business_key in user["businesses"]:
            await ctx.send("Ты уже владеешь этим бизнесом.")
            return
        user["balance"] -= business["price"]
        user["businesses"].append(business_key)
        save_users(users)
        await ctx.send(f"Ты купил бизнес **{business['name']}**!")

    @tasks.loop(minutes=10)
    async def passive_income(self):
        users = load_users()
        for user_id, data in users.items():
            if "businesses" in data:
                for biz in data["businesses"]:
                    if biz in BUSINESSES:
                        data["balance"] += BUSINESSES[biz]["income"]
        save_users(users)

    @passive_income.before_loop
    async def before_income(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Business(bot))
