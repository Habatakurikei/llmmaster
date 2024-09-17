from llmmaster import LLMMaster

# Create an instance of LLMMaster
llmmaster = LLMMaster()

# Configure LLM instance
llmmaster.summon({
    "openai_instance": llmmaster.pack_parameters(
        provider="openai",
        model="gpt-4o-mini",
        prompt="Hello, how are you?",
        max_tokens=100,
        temperature=0.7
    )
})

# Run LLM
print('Start running LLMMaster...')
llmmaster.run()

# Get results
results = llmmaster.results
print(f'OpenAI responded: {results["openai_instance"]}')

# Check elapsed time
print(f"Elapsed time: {llmmaster.elapsed_time} seconds")

# Clear instances
llmmaster.dismiss()
