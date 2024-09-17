import requests
from llmmaster import LLMMaster

master = LLMMaster()

test_image = '/home/user/test_image.png'

entries = [
    {
        'name': 'openai',
        'params': {
            'provider': 'openai_iti',
            'mode': 'variations',
            'image': test_image,
            'n': 2
        }
    },
    {
        'name': 'stable_diffusion',
        'params': {
            'provider': 'stable_diffusion_iti',
            'mode': 'remove_background',
            'image': test_image,
        }
    }]

for entry in entries:
    master.summon({entry['name']: master.pack_parameters(**entry['params'])})

print('Start running LLMMaster...')
master.run()

print('Results')

# Get results
response = master.results["openai"]
if hasattr(response, 'data'):
    for i in range(len(response.data)):
        image_response = requests.get(response.data[i].url)
        if image_response.status_code == 200:
            filename = f"openai_{i+1:02}.png"
            with open(filename, 'wb') as f:
                f.write(image_response.content)
            print(f'Image No. {i+1:2} saved as {filename}')
        else:
            print(f'Image No. {i+1:2} failed to download')

response = master.results["stable_diffusion"]
if isinstance(response, bytes):
    with open("stable_diffusion_result.png", 'wb') as f:
        f.write(response)
    print("stable_diffusion_result.png saved")

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
