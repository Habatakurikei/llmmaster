import requests
from llmmaster import LLMMaster

# Create an instance of LLMMaster
master = LLMMaster()

# Configure LLM instance
prompt = 'A cute robot boy flying high to the space.'
camera = {'zoom': 'out'}
parameters = {"guidanceScale":16,"motion":2,"negativePrompt": "ugly"}

params = master.pack_parameters(provider='pikapikapika_ttv',
                                prompt=prompt,
                                style='Anime',
                                sfx=True,
                                frameRate=24,
                                aspectRatio='16:9',
                                camera=camera,
                                parameters=parameters)

master.summon({'pikapikapika_ttv': params})

# You can check what parameters are set before run
print('Parameters set before run.')
for label, instance in master.instances.items():
    print(f'{label} = {instance.parameters}')

# Run LLM
print('Start running LLMMaster...')
master.run()

# Get results
print('Responses')
response = master.results['pikapikapika_ttv'].json()

if 'resultUrl' in response['videos'][0] and response['videos'][0]:
    res = requests.get(response['videos'][0]['resultUrl'])
    if res.status_code == 200:
        filename = f'pikapikapika_ttv_test_video.mp4'
        with open(filepath, 'wb') as f:
            f.write(res.content)
            print(f'Saved as {filepath}')

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
