import json
from pathlib import Path

from llmmaster import LLMMaster

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
prompt = "A futuristic cityscape with flying cars in the clear sky"

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        "dall_e": master.pack_parameters(
            provider="openai_tti",
            model="dall-e-3",
            prompt=prompt,
            response_format="url",
            size="1792x1024",
            quality="hd"
        ),
        "stable_diffusion": master.pack_parameters(
            provider="stable_diffusion_tti",
            model="core",
            prompt=prompt,
            aspect_ratio="16:9",
            style_preset="cinematic"
        ),
        "flux1_fal": master.pack_parameters(
            provider="flux1_fal_tti",
            model="schnell",
            prompt=prompt,
            image_size="landscape_16_9",
            num_inference_steps=4
        ),
        "luma_dream_machine": master.pack_parameters(
            provider="lumaai_tti",
            prompt=prompt,
            aspect_ratio="16:9"
        ),
        "xai": master.pack_parameters(
            provider="xai_tti",
            prompt=prompt
        )
    }
)
master.run()

print("Response")
for key, result in master.results.items():
    to_show = f"Result for {key}: "
    if isinstance(result, dict):
        with open(f"{key}.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        to_show += f"Saved to {key}.json"
    else:
        to_show += f"type ({type(result)}) = {result}"
    print(to_show)

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
