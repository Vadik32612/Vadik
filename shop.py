
from discord.ext import commands
import discord
import json
import os

USERS_PATH = "data/users.json"
SHOP_ITEMS = {
    "nike_shirt": {"price": 200, "name": "Футболка Nike"},
    "adidas_jacket": {"price": 350, "name": "Куртка Adidas"},
    "gucci_pants": {"price": 500, "name": "Брюки Gucci"}
}

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=4)

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(title="Магазин одежды", description="Вот что у нас есть:")
        for item, info in SHOP_ITEMS.items():
            embed.add_field(name=info["name"], value=f"Цена: ${info['price']} — `!buy {item}`", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, item: str):
        item = item.lower()
        users = load_users()
        user_id = str(ctx.author.id)
        if user_id not in users:
            await ctx.send("Ты ещё не начал играть.")
            return
        if item not in SHOP_ITEMS:
            await ctx.send("Такой вещи нет в магазине.")
            return
        user = users[user_id]
        if user["balance"] < SHOP_ITEMS[item]["price"]:
            await ctx.send("У тебя недостаточно денег.")
            return
        user["balance"] -= SHOP_ITEMS[item]["price"]
        user["clothes"].append(item)
        save_users(users)
        await ctx.send(f"Ты купил **{SHOP_ITEMS[item]['name']}**!")

    @commands.command()
    async def clothes(self, ctx):
        users = load_users()
        user_id = str(ctx.author.id)
        if user_id not in users:
            await ctx.send("Ты ещё не начал играть.")
            return
        clothes = users[user_id]["clothes"]
        if not clothes:
            await ctx.send("У тебя нет одежды.")
        else:
            desc = "\n".join([SHOP_ITEMS[c]["name"] for c in clothes if c in SHOP_ITEMS])
            await ctx.send(f"Ты носишь:
{desc}")

async def setup(bot):
    await bot.add_cog(Shop(bot))
