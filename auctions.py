
from discord.ext import commands, tasks
import discord
import json
import os
import asyncio
import random

USERS_PATH = "data/users.json"
AUCTIONS_PATH = "data/auctions.json"

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=4)

def load_auctions():
    if not os.path.exists(AUCTIONS_PATH):
        return {}
    with open(AUCTIONS_PATH, "r") as f:
        return json.load(f)

def save_auctions(data):
    with open(AUCTIONS_PATH, "w") as f:
        json.dump(data, f, indent=4)

class Auction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_auctions = {}
        self.check_auctions.start()

    @tasks.loop(seconds=60)
    async def check_auctions(self):
        for channel_id, auction in list(self.active_auctions.items()):
            auction["time"] -= 60
            if auction["time"] <= 0:
                channel = self.bot.get_channel(int(channel_id))
                if auction["highest"]:
                    winner = auction["highest"]
                    item = auction["item"]
                    price = auction["bid"]
                    users = load_users()
                    if users[winner]["balance"] >= price:
                        users[winner]["balance"] -= price
                        users[winner].setdefault("cars", []).append(item)
                        save_users(users)
                        await channel.send(f"Аукцион завершён! Победитель: <@{winner}>. Товар: {item} за ${price}")
                    else:
                        await channel.send(f"<@{winner}> не хватило денег. Аукцион завершён без победителя.")
                else:
                    await channel.send(f"Аукцион по товару **{auction['item']}** завершён без ставок.")
                del self.active_auctions[channel_id]

    @commands.command()
    async def startauction(self, ctx, *, item):
        if str(ctx.channel.id) in self.active_auctions:
            await ctx.send("Аукцион уже идёт.")
            return

        self.active_auctions[str(ctx.channel.id)] = {
            "item": item,
            "bid": 0,
            "highest": None,
            "time": 300
        }

        await ctx.send(f"Аукцион начался! Лот: **{item}**. Делайте ставки командой `!bid <сумма>`")

    @commands.command()
    async def bid(self, ctx, amount: int):
        user_id = str(ctx.author.id)
        channel_id = str(ctx.channel.id)
        users = load_users()

        if channel_id not in self.active_auctions:
            await ctx.send("Здесь сейчас нет аукциона.")
            return

        auction = self.active_auctions[channel_id]

        if amount <= auction["bid"]:
            await ctx.send("Ставка должна быть выше текущей.")
            return

        if users[user_id]["balance"] < amount:
            await ctx.send("У тебя недостаточно средств.")
            return

        auction["bid"] = amount
        auction["highest"] = user_id

        await ctx.send(f"{ctx.author.mention} сделал ставку: ${amount}")

async def setup(bot):
    await bot.add_cog(Auction(bot))
