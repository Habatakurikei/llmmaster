import json
from pathlib import Path

import requests

from llmmaster import LLMMaster
from llmmaster.config import REQUEST_OK

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
prompt = "Japanese ladies in elegant kimono dancing in traditional tea room."
key = "lumaai_ttv"

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        key: master.pack_parameters(
            provider=key,
            prompt=prompt,
            aspect_ratio="16:9",
            loop=True
        )
    }
)
master.run()

print("Response")
response = master.results[key]

if isinstance(response, dict):
    save_as = f"{key}.json"
    with open(save_as, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2, ensure_ascii=False)
    print(f"Saved as {save_as}")

if "assets" in response:
    res = requests.get(response["assets"]["video"])
    if res.status_code == REQUEST_OK:
        save_as = f"{key}.mp4"
        with open(save_as, "wb") as f:
            f.write(res.content)
        print(f"Saved as {save_as}")

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
