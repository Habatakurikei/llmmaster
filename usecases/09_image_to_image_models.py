import json
from pathlib import Path

from llmmaster import LLMMaster
from llmmaster.utils import flux1_fal_image_input
from llmmaster.utils import flux1_fal_image_save

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
local_image = "./test_image_rgb.png"
web_image = "https://assets.st-note.com/production/uploads/images/153833605/rectangle_large_type_2_96493844e69c64098b27ff953b7b37b3.png"

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        "openai": master.pack_parameters(
            provider="openai_iti",
            mode="variations",
            image=local_image,
            n=1
        ),
        "stable_diffusion": master.pack_parameters(
            provider="stable_diffusion_iti",
            mode="edit/search-and-replace",
            image=local_image,
            prompt="Make happy",
            search_prompt="Cat",
            negative_prompt="ugly"
        ),
        "flux1_fal": master.pack_parameters(
            provider="flux1_fal_iti",
            model="dev/image-to-image",
            prompt="Make smiling",
            image_url=flux1_fal_image_input(local_image),
        ),
        "lumaai": master.pack_parameters(
            provider="lumaai_iti",
            prompt="Pop art style",
            style_ref=[
                {
                    "url": web_image,
                    "weight": 0.5,
                }
            ]
        )
    }
)
master.run()

print("Results")
for instance, response in master.results.items():
    save_as = f"{instance}.json"
    with open(save_as, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2)
    print(f"Saved {instance}: {save_as}")

save_as = "flux_fal_iti.png"
flux1_fal_image_save(result=master.results["flux1_fal"], save_as=save_as)
print(f"Saved binary image as {save_as}")

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
