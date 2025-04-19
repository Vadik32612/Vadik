
from discord.ext import commands
import discord
import json
import os
import random
import time

USERS_PATH = "data/users.json"
CASES_PATH = "data/court_cases.json"

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=4)

def load_cases():
    if not os.path.exists(CASES_PATH):
        return {}
    with open(CASES_PATH, "r") as f:
        return json.load(f)

def save_cases(cases):
    with open(CASES_PATH, "w") as f:
        json.dump(cases, f, indent=4)

class Justice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sue(self, ctx, member: discord.Member, *, reason="Нарушение закона"):
        cases = load_cases()
        case_id = str(len(cases) + 1)

        cases[case_id] = {
            "plaintiff": ctx.author.id,
            "defendant": member.id,
            "reason": reason,
            "status": "pending"
        }
        save_cases(cases)

        await ctx.send(f"Дело №{case_id} подано против {member.mention}. Причина: {reason}")

    @commands.command()
    async def cases(self, ctx):
        cases = load_cases()
        if not cases:
            await ctx.send("Нет активных дел.")
            return

        embed = discord.Embed(title="Судебные дела")
        for cid, case in cases.items():
            status = case["status"]
            embed.add_field(
                name=f"Дело №{cid}",
                value=f"Истец: <@{case['plaintiff']}>
Ответчик: <@{case['defendant']}>
Причина: {case['reason']}
Статус: {status}",
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def judge(self, ctx, case_id: str, decision: str):
        cases = load_cases()

        if case_id not in cases:
            await ctx.send("Такого дела нет.")
            return

        if decision.lower() not in ["виновен", "невиновен"]:
            await ctx.send("Решение должно быть: 'виновен' или 'невиновен'.")
            return

        cases[case_id]["status"] = decision.lower()
        save_cases(cases)

        await ctx.send(f"Дело №{case_id} решено: {decision.capitalize()}.")

    @commands.command()
    async def lawyer(self, ctx):
        fee = 500
        users = load_users()
        user_id = str(ctx.author.id)

        if user_id not in users:
            await ctx.send("Ты ещё не начал игру.")
            return

        if users[user_id]["balance"] < fee:
            await ctx.send("У тебя недостаточно денег на услуги адвоката.")
            return

        users[user_id]["balance"] -= fee
        save_users(users)

        await ctx.send(f"{ctx.author.mention}, ты нанял адвоката за ${fee}. Удачи в суде!")

async def setup(bot):
    await bot.add_cog(Justice(bot))
