import requests
from llmmaster import LLMMaster

task_id = 'uuid-generated-by-lumaai'

master = LLMMaster()

# Use generated video in Luma or public image in web.
# This is a case to extend video with generated frame.
key = 'lumaai_vtv'
params = master.pack_parameters(
    provider=key,
    prompt='The boy exploring the space finds Mars.',
    keyframes={
        "frame0": {
            "type": "generation",
            "id": task_id
        }
    }
)

master.summon({key: params})
master.run()

response = master.results[key]
if 'assets' in response:
    res = requests.get(response['assets']['video'])
    if res.status_code == 200:
        with open(f"{key}.mp4", "wb") as f:
            f.write(res.content)

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
