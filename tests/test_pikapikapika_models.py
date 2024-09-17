import os
import sys
import json
import requests
from requests.models import Response

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from llmmaster.config import REQUEST_OK
from llmmaster.pikapikapika_models import PikaPikaPikaGeneration
from llmmaster import LLMMaster


API_KEY = '''
'''


TEST_OUTPUT_PATH = 'test-outputs'


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_pikapikapika_generation_instances(run_api):
    judgment = True
    master = LLMMaster()

    prompt = 'A Japanese anime girl inspired by Akira Toriyama. Light blue hair, ponytail, pink dress, full body, winking with full smile.'
    camera = {'zoom': 'in'}
    parameters = {"guidanceScale":16,"motion":2,"negativePrompt": "ugly"}

    params = master.pack_parameters(provider='pikapikapika_ttv',
                                    prompt=prompt,
                                    style='Anime',
                                    sfx=True,
                                    frameRate=24,
                                    aspectRatio='16:9',
                                    camera=camera,
                                    parameters=parameters)
    master.set_api_keys(API_KEY)
    master.summon({'pikapikapika_ttv': params})

    print(f"Parameters = {master.instances['pikapikapika_ttv'].parameters}")
    print(f"API Key = {master.instances['pikapikapika_ttv'].api_key}")

    if not isinstance(master.instances['pikapikapika_ttv'], PikaPikaPikaGeneration):
        judgment = False

    if run_api:
        print('Run API')
        try:
            master.run()
        except Exception as e:
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        if not os.path.isdir(TEST_OUTPUT_PATH):
            os.makedirs(TEST_OUTPUT_PATH)

        print('Responses')
        if isinstance(master.results['pikapikapika_ttv'], str):
            pytest.fail(f"Failed to generate: {master.results['pikapikapika_ttv']}")
        elif not isinstance(master.results['pikapikapika_ttv'], Response):
            pytest.fail(f"Wrong type of result, expected Response: {type(master.results['pikapikapika_ttv'])}")

        else:
            json_result = master.results['pikapikapika_ttv'].json()
            print(f"json_result = {json.dumps(json_result, indent=2)}")

            if 'resultUrl' in json_result['videos'][0]:
                res = requests.get(json_result['videos'][0]['resultUrl'])
                if res.status_code == REQUEST_OK:
                    filename = f'pikapikapika_ttv_test_video.mp4'
                    filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                    with open(filepath, 'wb') as f:
                        f.write(res.content)
                    print(f'Saved as {filepath}')

            if 'imageThumb' in json_result['videos'][0]:
                res = requests.get(json_result['videos'][0]['imageThumb'])
                if res.status_code == REQUEST_OK:
                    filename = f'pikapikapika_ttv_test_thumbnail.png'
                    filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                    with open(filepath, 'wb') as f:
                        f.write(res.content)
                    print(f'Saved as {filepath}')

            if 'videoPoster' in json_result['videos'][0]:
                res = requests.get(json_result['videos'][0]['videoPoster'])
                if res.status_code == REQUEST_OK:
                    filename = f'pikapikapika_ttv_test_poster.png'
                    filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                    with open(filepath, 'wb') as f:
                        f.write(res.content)
                    print(f'Saved as {filepath}')

    print(f"Elapsed time in total (sec): {master.elapsed_time}")
    master.dismiss()

    assert judgment
