from PIL import Image
import os

def generate_profile_image(user_data):
    base = Image.open(f"assets/base_characters/{user_data['gender']}.png")
    for item in user_data['clothes']:
        clothing = Image.open(f"assets/clothes/{item}.png")
        base.paste(clothing, (0, 0), clothing)
    if user_data['gang']:
        uniform = Image.open(f"assets/gang_uniforms/{user_data['gang']}.png")
        base.paste(uniform, (0, 0), uniform)
    profile_path = f"profiles/{user_data['id']}.png"
    base.save(profile_path)
    return profile_path
