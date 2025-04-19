
from discord.ext import commands
import discord
import json
import os

USERS_PATH = "data/users.json"
CLOTHES = {
    "Nike Hoodie": 250,
    "Adidas Tracksuit": 300,
    "Supreme T-Shirt": 450,
    "Gucci Jacket": 900,
    "LV Sneakers": 650,
    "Balenciaga Pants": 700
}

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_PATH, "w") as f:
        json.dump(data, f, indent=4)

class Clothing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clothes(self, ctx):
        embed = discord.Embed(title="Магазин одежды", color=discord.Color.purple())
        for name, price in CLOTHES.items():
            embed.add_field(name=name, value=f"${price}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def buyclothes(self, ctx, *, item):
        users = load_users()
        uid = str(ctx.author.id)
        item = item.title()
        if item not in CLOTHES:
            return await ctx.send("Такой одежды нет в магазине.")
        price = CLOTHES[item]
        if users[uid]["balance"] < price:
            return await ctx.send("Недостаточно средств.")
        users[uid]["balance"] -= price
        users[uid].setdefault("clothes", []).append(item)
        save_users(users)
        await ctx.send(f"{ctx.author.mention}, вы купили {item} за ${price}")

    @commands.command()
    async def wear(self, ctx, *, item):
        users = load_users()
        uid = str(ctx.author.id)
        owned = users[uid].get("clothes", [])
        if item.title() not in owned:
            return await ctx.send("У вас нет этой одежды.")
        users[uid]["equipped"] = item.title()
        save_users(users)
        await ctx.send(f"{ctx.author.mention} надел {item.title()}")

    @commands.command()
    async def outfit(self, ctx):
        users = load_users()
        uid = str(ctx.author.id)
        current = users[uid].get("equipped")
        if current:
            await ctx.send(f"Сейчас на тебе: **{current}**")
        else:
            await ctx.send("Ты ничего не надел.")

async def setup(bot):
    await bot.add_cog(Clothing(bot))
