
from discord.ext import commands
import discord
from PIL import Image, ImageDraw, ImageFont
import os
import json

BASE_IMAGE = "assets/base_character.png"
CLOTHES_FOLDER = "assets/clothes/"
BANDANA_IMAGE = "assets/bandana.png"
USERS_PATH = "data/users.json"

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="profile")
    async def profile(self, ctx):
        uid = str(ctx.author.id)
        users = load_users()

        if uid not in users:
            return await ctx.send("Сначала зарегистрируйтесь.")

        base = Image.open(BASE_IMAGE).convert("RGBA")
        clothes_name = users[uid].get("wearing", None)
        if clothes_name:
            clothes_path = os.path.join(CLOTHES_FOLDER, f"{clothes_name}.png")
            if os.path.exists(clothes_path):
                clothes_img = Image.open(clothes_path).convert("RGBA")
                base.paste(clothes_img, (0, 0), clothes_img)

        if users[uid].get("gang") == "Backwoods":
            if os.path.exists(BANDANA_IMAGE):
                bandana = Image.open(BANDANA_IMAGE).convert("RGBA")
                base.paste(bandana, (0, 0), bandana)

        output_path = f"temp/{uid}_profile.png"
        os.makedirs("temp", exist_ok=True)
        base.save(output_path)

        await ctx.send(file=discord.File(output_path))

async def setup(bot):
    await bot.add_cog(Profile(bot))
