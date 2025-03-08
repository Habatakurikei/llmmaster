import json

from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response

# Create an instance of LLMMaster
key = "openai_instance"
master = LLMMaster()

# Configure LLM instance
master.summon(
    {
        key: master.pack_parameters(
            provider="openai",
            model="gpt-4o-mini",
            prompt="Hello, how are you?",
            max_tokens=100,
            temperature=0.7
        )
    }
)

# Run LLM
print("Start running LLMMaster...")
master.run()

# Show results
result_text = extract_llm_response(master.results[key])
print(f"Response: {result_text}")

# Save results to a JSON file
save_as = "results.json"
with open(save_as, "w", encoding="utf-8") as f:
    json.dump(master.results[key], f, indent=4, ensure_ascii=False)
print(f"Results saved to {save_as}")

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

# Clear instance
master.dismiss()
