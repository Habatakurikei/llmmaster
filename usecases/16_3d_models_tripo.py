import json
from pathlib import Path

from llmmaster import LLMMaster

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
key = "tripo_tt3d"
prompt = "A cute robot boy."
negative_prompt = "ugly, low resolution"

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        key: master.pack_parameters(
            provider=key,
            model="v2.0-20240919",
            prompt=prompt,
            negative_prompt=negative_prompt,
            image_seed=1,
            model_seed=1,
            face_limit=10000,
            texture=True,
            pbr=True,
            texture_seed=1,
            texture_quality="detailed",
            auto_size=False,
            style="person:person2cartoon",
            quad=True
        )
    }
)
master.run()

print("Response")
save_as = f"{key}.json"
with open(save_as, "w", encoding="utf-8") as f:
    json.dump(master.results[key], f, indent=2)

print(f"Saved as {save_as}")
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
