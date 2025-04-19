
from discord.ext import commands
import discord
import json
import os
import random

USERS_PATH = "data/users.json"

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_PATH, "w") as f:
        json.dump(data, f, indent=4)

class Justice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hirelawyer(self, ctx):
        uid = str(ctx.author.id)
        users = load_users()
        if users.get(uid, {}).get("jailed", False):
            chance = random.randint(1, 100)
            if chance <= 70:
                users[uid]["jailed"] = False
                save_users(users)
                await ctx.send("Адвокат успешно освободил тебя из тюрьмы.")
            else:
                await ctx.send("Адвокат проиграл дело. Ты остаёшься в тюрьме.")
        else:
            await ctx.send("Ты не в тюрьме.")

    @commands.command()
    async def prosecute(self, ctx, member: discord.Member):
        users = load_users()
        uid = str(member.id)
        if uid not in users or users[uid].get("jailed", False):
            return await ctx.send("Пользователь уже в тюрьме или не зарегистрирован.")
        chance = random.randint(1, 100)
        if chance <= 30:
            users[uid]["jailed"] = True
            save_users(users)
            await ctx.send(f"Прокуратура выиграла дело. {member.mention} отправлен в тюрьму.")
        else:
            await ctx.send("Суд не поддержал обвинение. Пользователь остался на свободе.")

    @commands.command()
    async def paytax(self, ctx):
        uid = str(ctx.author.id)
        users = load_users()
        balance = users.get(uid, {}).get("money", 0)
        tax = int(balance * 0.1)
        if balance >= tax:
            users[uid]["money"] -= tax
            save_users(users)
            await ctx.send(f"Ты заплатил налог в размере {tax}$.")
        else:
            await ctx.send("Недостаточно средств для уплаты налога.")

async def setup(bot):
    await bot.add_cog(Justice(bot))
