import json
from pathlib import Path

from llmmaster import LLMMaster

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
key = "lumaai_vtv"
task_id = "xxxxxxxx-3aef-423e-b8d2-22799e679d3f"

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        key: master.pack_parameters(
            provider=key,
            prompt="Let the girl dancing in the disco.",
            keyframes={
                "frame0": {
                    "type": "generation",
                    "id": task_id
                }
            }
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
