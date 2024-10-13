import requests
from llmmaster import LLMMaster

key = 'skybox_ttp'
negative_prompt = 'ugly, dirty, low resolution'
prompt = 'A Japanese temple, surrounded by mountains, with cherry blossoms.'

master = LLMMaster()
master.summon({
    key: master.pack_parameters(
        provider=key,
        prompt=prompt,
        skybox_style_id=138,
        negative_text=negative_prompt
    )
})

print('Run master')
master.run()

print('Responses')
response = master.results[key]

# Download images generated
if 'request' in response:
    res = requests.get(response['request']['file_url'])
    if res.status_code == 200:
        with open(f"{key}_view.jpg", 'wb') as f:
            f.write(res.content)

    res = requests.get(response['request']['thumb_url'])
    if res.status_code == 200:
        with open(f"{key}_thumb.jpg", 'wb') as f:
            f.write(res.content)

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
