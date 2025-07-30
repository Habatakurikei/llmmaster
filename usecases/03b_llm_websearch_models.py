from pathlib import Path

from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
prompt = "What are most popular pokemon characters in 2025? Look for rankings."

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        "anthropic": {
            "provider": "anthropic",
            "model": "claude-sonnet-4-20250514",
            "prompt": prompt,
            "tools": [
                {
                    "type": "web_search_20250305",
                    "name": "web_search",
                    "max_uses": 3
                }
            ],
        },
        "google": {
            "provider": "google",
            "model": "gemini-2.5-flash",
            "prompt": prompt,
            "tools": [{
                "googleSearch": {}
            }]
        },
        "openai": {
            "provider": "openai",
            "model": "gpt-4o-search-preview",
            "prompt": prompt,
            "web_search_options": {
                "search_context_size": "low"
            },
        },
        "perplexity": {
            "provider": "perplexity",
            "model": "sonar",
            "prompt": prompt,
            "web_search_options": {
                "search_context_size": "low"
            },
        },
        "xai": {
            "provider": "xai",
            "model": "grok-3",
            "prompt": prompt,
            "search_parameters": {
                "mode": "on",
                "return_citations": True
            },
        }
    }
)
master.run()

print("Responses.")
for instance, response in master.results.items():
    print(f"{instance} responded: {extract_llm_response(response)}")
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
