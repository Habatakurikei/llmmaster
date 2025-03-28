from pathlib import Path

from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
prompt = "What will happen in the technological singularity?"

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        "openai_o1": master.pack_parameters(
            provider="openai",
            model="o1",
            prompt=prompt,
            reasoning_effort="high",
        ),
        "google_search": master.pack_parameters(
            provider="google",
            model="gemini-1.5-flash",
            prompt=prompt,
            dynamic_threshold=0.0
        ),
        "perplexity_reasoning": master.pack_parameters(
            provider="perplexity",
            model="sonar-reasoning",
            prompt=prompt
        ),
        "deepseek_reasoner": master.pack_parameters(
            provider="deepseek",
            model="deepseek-reasoner",
            prompt=prompt
        )
    }
)
master.run()

print("Responses.")
for instance, response in master.results.items():
    print(f"{instance} responded: {extract_llm_response(response)}")
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
