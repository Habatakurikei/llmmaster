from pathlib import Path

from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
key = "openai"

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
print(f"API key pairs (print for debug purpose): {master.api_key_pairs}")

master.summon(
    {
        key: master.pack_parameters(
            provider=key,
            prompt="Hello, how are you?"
        )
    }
)
master.run()

print(f"Response: {extract_llm_response(master.results[key])}")
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
