import requests
from llmmaster import LLMMaster

# Create an instance of LLMMaster
master = LLMMaster()

# Configure instances
master.summon({
    "openai_image": master.pack_parameters(
        provider="openai_tti",
        model="dall-e-3",
        prompt="A futuristic cityscape with flying cars in the clear sky",
        size="1792x1024",
        quality="hd"
    ),
    "stable_diffusion_image": master.pack_parameters(
        provider="stable_diffusion_tti",
        model="core",
        prompt="A serene landscape with a mountain lake at sunset",
        aspect_ratio="16:9",
        style_preset="cinematic"
    ),
    "flux1_fal_image": master.pack_parameters(
        provider="flux1_fal_tti",
        model="fal-ai/flux/schnell",
        prompt="A spaceship heading to Mars in the space",
        image_size="landscape_16_9",
        num_inference_steps=4
    )
})

# You can check what parameters are set before run
print('Parameters set before run.')
for label, instance in master.instances.items():
    print(f'{label} = {instance.parameters}')

# Run master
print('Start running LLMMaster...')
master.run()

# Get results
response = master.results["openai_image"]
if 'data' in response:
    image_response = requests.get(response['data'][0]['url'])
    if image_response.status_code == 200:
        with open("openai_image.png", 'wb') as f:
            f.write(image_response.content)
        print("openai_image.png saved")

response = master.results["stable_diffusion_image"]
if hasattr(response, 'content'):
    with open("stable_diffusion_image.png", 'wb') as f:
        f.write(response.content)
    print("stable_diffusion_image.png saved")

response = master.results["flux1_fal_image"]
if 'images' in response:
    image_response = requests.get(response['images'][0]['url'])
    if image_response.status_code == 200:
        with open("flux1_fal_image.png", 'wb') as f:
            f.write(image_response.content)
    print("flux1_fal_image.png saved")

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

# Clear instances
master.dismiss()
