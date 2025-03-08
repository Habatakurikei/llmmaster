import json
from pathlib import Path

from llmmaster import LLMMaster

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
local_image = "./test_image_sq.png"
web_image = "https://assets.st-note.com/production/uploads/images/153833605/rectangle_large_type_2_96493844e69c64098b27ff953b7b37b3.png"
prompt = "The girl makes smiling with her eyes closed."

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        "stable_diffusion": master.pack_parameters(
            provider="stable_diffusion_itv",
            image=local_image
        ),
        "lumaai": master.pack_parameters(
            provider="lumaai_itv",
            prompt=prompt,
            keyframes={
                "frame0": {
                    "type": "image",
                    "url": web_image
                }
            }
        ),
        "runway": master.pack_parameters(
            provider="runway_itv",
            prompt=prompt,
            promptImage=web_image
        )
    }
)
master.run()

print("Results")

response = master.results["stable_diffusion"]
if hasattr(response, "content"):
    with open("stable_diffusion_itv.mp4", "wb") as f:
        f.write(response.content)
print("Saved stable_diffusion_itv.mp4")

with open("lumaai_itv.json", "w", encoding="utf-8") as f:
    json.dump(master.results["lumaai"], f, indent=2)
print("Saved lumaai_itv.json")

with open("runway_itv.json", "w", encoding="utf-8") as f:
    json.dump(master.results["runway"], f, indent=2)
print("Saved runway_itv.json")

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
