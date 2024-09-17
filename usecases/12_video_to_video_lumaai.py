import requests
from llmmaster import LLMMaster

master = LLMMaster()

prompt = 'The boy exploring the space finds Mars.'

# Use generated video in Luma or public image in web.
# This is a case to extend video with generated frame.
keyframes={
    "frame0": {
    "type": "generation",
    "id": "uuid-generated-by-lumaai"
    }
}

params = master.pack_parameters(provider='lumaai_vtv',
                                prompt=prompt,
                                keyframes=keyframes)
master.set_api_keys(API_KEY)
master.summon({'lumaai_vtv': params})

print('Start running LLMMaster...')
master.run()

print('Results')
response = master.results["lumaai_vtv"]
res = requests.get(response['assets']['video'])
if res.status_code == 200:
    with open("lumaai_vtv.mp4", 'wb') as f:
        f.write(res.content)
    print("lumaai_vtv.mp4 saved")

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
