
from discord.ext import commands
import discord
import json
import os
import random
import time

USERS_PATH = "data/users.json"
GANGS_PATH = "data/gangs.json"

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=4)

def load_gangs():
    if not os.path.exists(GANGS_PATH):
        return {}
    with open(GANGS_PATH, "r") as f:
        return json.load(f)

def save_gangs(gangs):
    with open(GANGS_PATH, "w") as f:
        json.dump(gangs, f, indent=4)

class Crime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rob(self, ctx, member: discord.Member):
        if member.id == ctx.author.id:
            await ctx.send("Ты не можешь ограбить сам себя.")
            return

        users = load_users()
        attacker = str(ctx.author.id)
        victim = str(member.id)

        if attacker not in users or victim not in users:
            await ctx.send("Оба игрока должны быть зарегистрированы.")
            return

        if users[victim]["balance"] < 100:
            await ctx.send("У жертвы слишком мало денег.")
            return

        success = random.choice([True, False])
        if success:
            amount = random.randint(50, 300)
            users[attacker]["balance"] += amount
            users[victim]["balance"] -= amount
            await ctx.send(f"{ctx.author.mention} успешно ограбил {member.mention} и получил ${amount}.")
        else:
            fine = 100
            users[attacker]["balance"] = max(0, users[attacker]["balance"] - fine)
            await ctx.send(f"{ctx.author.mention} провалил ограбление и был оштрафован на ${fine}.")

        save_users(users)

    @commands.command()
    async def create_gang(self, ctx, *, gang_name):
        gangs = load_gangs()
        users = load_users()
        user_id = str(ctx.author.id)

        if user_id not in users:
            await ctx.send("Ты не зарегистрирован.")
            return

        if users[user_id].get("gang"):
            await ctx.send("Ты уже состоишь в банде.")
            return

        if gang_name in gangs:
            await ctx.send("Такая банда уже существует.")
            return

        gangs[gang_name] = {
            "leader": user_id,
            "members": [user_id]
        }
        users[user_id]["gang"] = gang_name

        save_gangs(gangs)
        save_users(users)
        await ctx.send(f"{ctx.author.mention} создал банду **{gang_name}**!")

    @commands.command()
    async def join_gang(self, ctx, *, gang_name):
        gangs = load_gangs()
        users = load_users()
        user_id = str(ctx.author.id)

        if gang_name not in gangs:
            await ctx.send("Такой банды не существует.")
            return

        if users[user_id].get("gang"):
            await ctx.send("Ты уже в банде.")
            return

        gangs[gang_name]["members"].append(user_id)
        users[user_id]["gang"] = gang_name

        save_gangs(gangs)
        save_users(users)
        await ctx.send(f"{ctx.author.mention} вступил в банду **{gang_name}**.")

    @commands.command()
    async def gang(self, ctx):
        users = load_users()
        gangs = load_gangs()
        user_id = str(ctx.author.id)

        gang_name = users[user_id].get("gang")
        if not gang_name:
            await ctx.send("Ты не состоишь в банде.")
            return

        gang = gangs.get(gang_name)
        embed = discord.Embed(title=f"Банда: {gang_name}", description=f"Лидер: <@{gang['leader']}>")
        members = "
".join([f"<@{m}>" for m in gang["members"]])
        embed.add_field(name="Участники", value=members, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def heal(self, ctx):
        users = load_users()
        user_id = str(ctx.author.id)

        if user_id not in users:
            await ctx.send("Ты не зарегистрирован.")
            return

        cost = 150
        if users[user_id]["balance"] < cost:
            await ctx.send("Недостаточно средств на лечение.")
            return

        users[user_id]["balance"] -= cost
        save_users(users)
        await ctx.send(f"{ctx.author.mention}, ты прошёл лечение за ${cost}.")

async def setup(bot):
    await bot.add_cog(Crime(bot))
