import requests
from llmmaster import LLMMaster

local_image = '/home/user/test_image.png'
image_url = 'https://example.com/image-1.jpg'

master = LLMMaster()
master.summon({
    "openai": master.pack_parameters(
        provider="openai_iti",
        mode='variations',
        image=local_image,
        n=1
    ),
    "stable_diffusion": master.pack_parameters(
        provider='stable_diffusion_iti',
        mode='remove_background',
        image=local_image,
    ),
    "flux1_fal": master.pack_parameters(
        provider="flux1_fal_iti",
        strength=0.95,
        image_url=image_url,
        prompt='Make smiling',
        image_size='landscape_16_9'
    )
})

print('Start running LLMMaster...')
master.run()

print('Results')

response = master.results["openai"]
if 'data' in response:
    image_response = requests.get(response['data'][0]['url'])
    if image_response.status_code == 200:
        with open("openai_iti.png", 'wb') as f:
            f.write(image_response.content)

response = master.results["stable_diffusion"]
if hasattr(response, 'content'):
    with open("stable_diffusion_iti.png", 'wb') as f:
        f.write(response.content)

response = master.results["flux1_fal"]
if 'images' in response:
    image_response = requests.get(response['images'][0]['url'])
    if image_response.status_code == 200:
        with open("flux1_fal_iti.png", 'wb') as f:
            f.write(image_response.content)

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
