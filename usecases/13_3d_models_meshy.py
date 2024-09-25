import requests
from llmmaster import LLMMaster

key = 'meshy_tt3d'
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

# Meshy returns several different model formats
for format, url in response['model_urls'].items():
    if url:
        res = requests.get(url)
        if res.status_code == 200:
            with open(f"{key}.{format}", 'wb') as f:
                f.write(res.content)

# Meshy also returns thumbnail png for preview
if 'thumbnail_url' in response:
    res = requests.get(response['thumbnail_url'])
    if res.status_code == 200:
        with open(f"{key}.png", 'wb') as f:
            f.write(res.content)

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
