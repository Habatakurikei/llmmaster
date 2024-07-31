import requests
from requests.models import Response
from llmmaster import LLMMaster

REQUEST_OK = 200
TEST_OUTPUT_PATH = 'test-outputs'

master = LLMMaster()

prompt = 'A cute robot boy.'

# This is a case of generating Voxel model from text prompt
params = master.pack_parameters(provider='meshy_ttvx',
                                prompt=prompt,
                                negative_prompt='ugly, low resolution')

master.summon({'meshy_ttvx_test': params})

# Run LLM
print('Start running LLMMaster...')
master.run()

# Get results
print('Responses')

if isinstance(master.results['meshy_ttvx_test'], Response):

    json_result = master.results['meshy_ttvx_test'].json()

    # Meshy returns several different model formats
    for key, value in json_result['model_urls'].items():
        if value:
            res = requests.get(value)
            if res.status_code == REQUEST_OK:
                filename = f'meshy_ttvx_test.{key}'
                filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                with open(filepath, 'wb') as f:
                    f.write(res.content)
                print(f'Saved as {filepath}')

    # Meshy also returns thumbnail png for preview
    if 'thumbnail_url' in json_result:
        res = requests.get(json_result['thumbnail_url'])
        if res.status_code == REQUEST_OK:
            filename = f'meshy_ttvx_test_thumbnail.png'
            filepath = os.path.join(TEST_OUTPUT_PATH, filename)
            with open(filepath, 'wb') as f:
                f.write(res.content)
            print(f'Saved as {filepath}')

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
