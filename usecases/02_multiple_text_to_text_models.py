from llmmaster import LLMMaster

# Create an instance of LLMMaster
llmmaster = LLMMaster()

# Configure LLM instance
llmmaster.summon({
    "openai_instance": llmmaster.pack_parameters(
        provider="openai",
        prompt="Summarize the main ideas of quantum computing."
    ),
    "anthropic_instance": llmmaster.pack_parameters(
        provider="anthropic",
        prompt="Explain the concept of artificial general intelligence."
    )
})

# You can check what parameters are set before run
print('Parameters set before run.')
for label, instance in llmmaster.instances.items():
    print(f'{label} = {instance.parameters}')

# Run LLM
print('Start running LLMMaster...')
llmmaster.run()

# Get results
for instance, response in llmmaster.results.items():
    print(f'{instance} responded: {response}')

# Check elapsed time
print(f"Elapsed time: {llmmaster.elapsed_time} seconds")

# Clear instances
llmmaster.dismiss()
