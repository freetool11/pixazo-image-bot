import requests
import os
import time
from datetime import datetime

API_KEY = os.getenv("PIXAZO_API_KEY")

def generate_image(prompt):
    url = "https://api.pixazo.ai/v1/images/generate"

    payload = {
        "prompt": f"{prompt}, ultra realistic, 4k, cinematic lighting, highly detailed",
        "model": "flux",
        "width": 1024,
        "height": 1024
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        print("❌ Error:", response.text)
        return None

    data = response.json()
    image_url = data["data"][0]["url"]

    img_data = requests.get(image_url).content
    return img_data


today = datetime.now().strftime("%Y-%m-%d")
output_dir = f"images/{today}"
os.makedirs(output_dir, exist_ok=True)

with open("prompts.txt", "r") as f:
    prompts = [p.strip() for p in f if p.strip()]

print(f"Loaded {len(prompts)} prompts")

for i, prompt in enumerate(prompts):
    try:
        print(f"Generating {i+1}: {prompt}")

        image = generate_image(prompt)

        if image:
            with open(f"{output_dir}/img_{i+1}.png", "wb") as f:
                f.write(image)

        time.sleep(3)

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
