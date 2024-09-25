from pathlib import Path
from llmmaster import LLMMaster

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")

# Create an instance of LLMMaster
master = LLMMaster()
master.set_api_keys(api_key_pairs)
print(f'API key pairs: {master.api_key_pairs}')

# Configure LLM instance
master.summon({
    "openai_instance": master.pack_parameters(
        provider="openai",
        prompt="Summarize the main ideas of quantum computing."
    ),
    "anthropic_instance": master.pack_parameters(
        provider="anthropic",
        prompt="Explain the concept of artificial general intelligence."
    )
})

# You can check what parameters are set before run
print('Parameters set before run.')
for label, instance in master.instances.items():
    print(f'{label} = {instance.parameters}')

# Run LLM
print('Start running LLMMaster...')
master.run()

# Get results
for instance, response in master.results.items():
    print(f'{instance} responded: {response}')

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

# Clear instances
master.dismiss()
