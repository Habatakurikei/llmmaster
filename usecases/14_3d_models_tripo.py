import requests
from llmmaster import LLMMaster

key = 'tripo_tt3d'
negative_prompt = 'ugly, low resolution'
prompt = 'A cute robot boy.'

master = LLMMaster()
master.summon({
    key: master.pack_parameters(
        provider=key,
        prompt=prompt,
        negative_prompt=negative_prompt
    )
})

print('Run master')
master.run()

print('Responses')
response = master.results[key]

if 'data' in response:
    # Download model
    ext = response['data']['result']['model']['type']
    res = requests.get(response['data']['result']['model']['url'])
    if res.status_code == 200:
        with open(f"{key}.{ext}", "wb") as f:
            f.write(res.content)

    # Download model
    ext = response['data']['result']['rendered_image']['type']
    res = requests.get(response['data']['result']['rendered_image']['url'])
    if res.status_code == 200:
        with open(f"{key}.{ext}", "wb") as f:
            f.write(res.content)

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
