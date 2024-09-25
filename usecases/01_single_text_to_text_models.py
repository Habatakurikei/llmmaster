from llmmaster import LLMMaster

# Create an instance of LLMMaster
master = LLMMaster()

# Configure LLM instance
master.summon({
    "openai_instance": master.pack_parameters(
        provider="openai",
        model="gpt-4o-mini",
        prompt="Hello, how are you?",
        max_tokens=100,
        temperature=0.7
    )
})

# Run LLM
print('Start running LLMMaster...')
master.run()

# Get results
results = master.results
print(f'OpenAI responded: {results["openai_instance"]}')

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

# Clear instances
master.dismiss()
