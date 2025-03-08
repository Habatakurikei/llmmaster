from pathlib import Path

from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
prompt = "Who are you?"
provider_list = [
    "anthropic", "cerebras", "deepseek", "google", "groq", "mistral",
    "openai", "perplexity", "sambanova", "xai"
]

# Create an instance of LLMMaster
master = LLMMaster()
master.set_api_keys(api_key_pairs)

# Configure LLM instance
for provider in provider_list:
    master.summon(
        {
            provider: master.pack_parameters(
                provider=provider,
                prompt=prompt
            )
        }
    )

# You can check what parameters are set before run
print("Parameters (print for debug purpose).")
for label, instance in master.instances.items():
    print(f"{label} = {instance.parameters}")

# Run LLM
print("Start running LLMMaster...")
master.run()

# Get results
for instance, response in master.results.items():
    print(f"{instance} responded: {extract_llm_response(response)}")

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

# Clear instances
master.dismiss()
