from pathlib import Path
from llmmaster import LLMMaster

api_key_text = Path("api_key_pairs.txt").read_text(encoding="utf-8")

master = LLMMaster()

parameters = master.pack_parameters(provider="openai",
                                    prompt="Hello, how are you?")
master.set_api_keys(api_key_text)
print(f'API key pairs: {master.api_key_pairs}')

master.summon({"openai": parameters})
master.run()

results = master.results
print(f'OpenAI responded: {results["openai"]}')
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
