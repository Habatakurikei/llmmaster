import requests
from llmmaster import LLMMaster

local_image = '/home/user/test_image.png'
image_url = 'https://example.com/image-1.jpg'

master = LLMMaster()
master.summon({
    "stable_diffusion": master.pack_parameters(
        provider='stable_diffusion_itv',
        image=local_image
    ),
    "lumaai": master.pack_parameters(
        provider='lumaai_itv',
        prompt='Make smiling',
        frame0=image_url
    )
})

print('Start running LLMMaster...')
master.run()

print('Results')

response = master.results["stable_diffusion"]
if hasattr(response, 'content'):
    with open("stable_diffusion_itv.mp4", 'wb') as f:
        f.write(response.content)

response = master.results["lumaai"]
if 'assets' in response:
    res = requests.get(response['assets']['video'])
    if res.status_code == 200:
        with open("lumaai_itv.mp4", "wb") as f:
            f.write(res.content)

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
