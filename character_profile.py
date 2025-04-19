
from discord.ext import commands
import discord
from PIL import Image
import os
import json

USERS_PATH = "data/users.json"
BASE_CHAR_PATH = "assets/base_character.png"
CLOTHES_DIR = "assets/clothes"

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_PATH, "w") as f:
        json.dump(data, f, indent=4)

def generate_character_image(user_id):
    users = load_users()
    user_data = users.get(str(user_id), {})
    outfit = user_data.get("outfit", [])

    base = Image.open(BASE_CHAR_PATH).convert("RGBA")

    for clothing in outfit:
        clothing_path = os.path.join(CLOTHES_DIR, f"{clothing}.png")
        if os.path.exists(clothing_path):
            clothes_layer = Image.open(clothing_path).convert("RGBA")
            base.paste(clothes_layer, (0, 0), clothes_layer)

    output_path = f"data/rendered_characters/{user_id}.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    base.save(output_path)
    return output_path

class CharacterProfile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx):
        user_id = ctx.author.id
        image_path = generate_character_image(user_id)

        embed = discord.Embed(title=f"Профиль {ctx.author.name}")
        file = discord.File(image_path, filename="character.png")
        embed.set_image(url="attachment://character.png")
        await ctx.send(file=file, embed=embed)

    @commands.command()
    async def wear(self, ctx, item):
        user_id = str(ctx.author.id)
        users = load_users()
        if user_id not in users:
            users[user_id] = {"outfit": []}

        if "outfit" not in users[user_id]:
            users[user_id]["outfit"] = []

        if item not in users[user_id]["outfit"]:
            users[user_id]["outfit"].append(item)
            save_users(users)
            await ctx.send(f"Ты надел {item}.")
        else:
            await ctx.send("Ты уже носишь это.")

    @commands.command()
    async def remove(self, ctx, item):
        user_id = str(ctx.author.id)
        users = load_users()
        if item in users.get(user_id, {}).get("outfit", []):
            users[user_id]["outfit"].remove(item)
            save_users(users)
            await ctx.send(f"Ты снял {item}.")
        else:
            await ctx.send("Этот предмет не надет.")

async def setup(bot):
    await bot.add_cog(CharacterProfile(bot))
