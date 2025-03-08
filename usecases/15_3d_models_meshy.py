import json
from pathlib import Path

from llmmaster import LLMMaster

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
key = "meshy_tt3d"
prompt = "A cute robot boy."

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        key: master.pack_parameters(
            provider=key,
            prompt=prompt,
            art_style="realistic",
            seed=1,
            ai_model="meshy-4",
            topology="quad",
            target_polycount=150000,
            should_remesh=True,
            symmetry_mode="on"
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
