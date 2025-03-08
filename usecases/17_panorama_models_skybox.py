import json
from pathlib import Path

from llmmaster import LLMMaster

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
key = "skybox_ttp"
prompt = "A futuristic cityscape with flying cars in the clear sky"
negative_prompt = "ugly, dirty, low resolution"

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        key: master.pack_parameters(
            provider=key,
            prompt=prompt,
            skybox_style_id=112,
            negative_text=negative_prompt,
            enhance_prompt=True,
            seed=1
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
