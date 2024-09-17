import requests
from llmmaster import LLMMaster

# Create an instance of LLMMaster
llmmaster = LLMMaster()

# Configure LLM instance
llmmaster.summon({
    "openai_image": llmmaster.pack_parameters(
        provider="openai_tti",
        model="dall-e-3",
        prompt="A futuristic cityscape with flying cars and holographic billboards",
        size="1792x1024",
        quality="hd"
    ),
    "stable_diffusion_image": llmmaster.pack_parameters(
        provider="stable_diffusion_tti",
        model="core",
        prompt="A serene landscape with a mountain lake at sunset",
        aspect_ratio="16:9",
        style_preset="cinematic"
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
response = llmmaster.results["openai_image"]
if hasattr(response, 'data'):
    image_response = requests.get(response.data[0].url)
    if image_response.status_code == 200:
        with open("openai_image.png", 'wb') as f:
            f.write(image_response.content)
        print("openai_image.png saved")

response = llmmaster.results["stable_diffusion_image"]
if isinstance(response, bytes):
    with open("stable_diffusion_image.png", 'wb') as f:
        f.write(response)
    print("stable_diffusion_image.png saved")

# Check elapsed time
print(f"Elapsed time: {llmmaster.elapsed_time} seconds")

# Clear instances
llmmaster.dismiss()
