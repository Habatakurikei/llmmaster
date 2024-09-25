import requests
from llmmaster import LLMMaster

master = LLMMaster()

prompt = 'Japanese ladies in elegant kimono dancing in traditional tea room.'

pika_parameters = {
    "guidanceScale": 16,
    "motion": 2,
    "negativePrompt": "ugly"
}

# Configure instances
master.summon({
    "pikapikapika_ttv": master.pack_parameters(
        provider='pikapikapika_ttv',
        prompt=prompt,
        style='Anime',
        sfx=True,
        frameRate=24,
        aspectRatio='16:9',
        camera={'zoom': 'out'},
        parameters=pika_parameters
    ),
    "lumaai_ttv": master.pack_parameters(
        provider='lumaai_ttv',
        prompt=prompt,
        aspect_ratio='16:9',
        loop=True
    )
})

print('Parameters set before run.')
for label, instance in master.instances.items():
    print(f'{label} = {instance.parameters}')

print('Start running LLMMaster...')
master.run()

print('Responses')

response = master.results['pikapikapika_ttv']
if 'videos' in response:
    res = requests.get(response['videos'][0]['resultUrl'])
    if res.status_code == 200:
        save_as = "pikapikapika_ttv.mp4"
        with open(save_as, "wb") as f:
            f.write(res.content)
        print(f'Saved as {save_as}')

response = master.results['lumaai_ttv']
if 'assets' in response:
    res = requests.get(response['assets']['video'])
    if res.status_code == 200:
        save_as = "lumaai_ttv.mp4"
        with open(save_as, "wb") as f:
            f.write(res.content)
        print(f'Saved as {save_as}')

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
