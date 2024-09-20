import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from llmmaster.lumaai_models import LumaDreamMachineTextToVideo
from llmmaster.lumaai_models import LumaDreamMachineImageToVideo
from llmmaster.lumaai_models import LumaDreamMachineVideoToVideo
from llmmaster import LLMMaster


API_KEY = '''
'''


TEST_OUTPUT_PATH = 'test-outputs'


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_luma_text_to_video_instances(run_api):
    judgment = True
    master = LLMMaster()

    prompt = 'A serene Japanese garden with a koi pond, cherry blossoms, and a traditional wooden bridge.'
    params = master.pack_parameters(provider='lumaai_ttv',
                                    prompt=prompt,
                                    aspect_ratio='4:3',
                                    loop=True)
    master.set_api_keys(API_KEY)
    master.summon({'luma_ttv': params})

    print(f"Parameters = {master.instances['luma_ttv'].parameters}")
    print(f"API Key = {master.instances['luma_ttv'].api_key}")

    if not isinstance(master.instances['luma_ttv'], LumaDreamMachineTextToVideo):
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
        if isinstance(master.results['luma_ttv'], str):
            pytest.fail(f"Failed to generate: {master.results['luma_ttv']}")
        else:
            print(f"Result = {json.dumps(master.results, indent=2)}")
            filepath = os.path.join(TEST_OUTPUT_PATH, 'lumaai_ttv.json')
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(master.results, f, indent=2, ensure_ascii=False)
            print(f'Saved as {filepath}')

    print(f"Elapsed time in total (sec): {master.elapsed_time}")
    master.dismiss()

    assert judgment


def test_luma_image_to_video_instances(run_api):
    judgment = True
    master = LLMMaster()

    prompt = 'The merlion spouts water to the sky.'
    image_path = 'https://habatakurikei.com/wp-content/uploads/2018/06/cover-singapore-opt.jpg'

    params = master.pack_parameters(provider='lumaai_itv',
                                    prompt=prompt,
                                    frame0=image_path)
    master.set_api_keys(API_KEY)
    master.summon({'luma_itv': params})

    print(f"Parameters = {master.instances['luma_itv'].parameters}")
    print(f"API Key = {master.instances['luma_itv'].api_key}")

    if not isinstance(master.instances['luma_itv'], LumaDreamMachineImageToVideo):
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
        if isinstance(master.results['luma_itv'], str):
            pytest.fail(f"Failed to generate: {master.results['luma_itv']}")
        else:
            print(f"Result = {json.dumps(master.results, indent=2)}")
            filepath = os.path.join(TEST_OUTPUT_PATH, 'lumaai_itv.json')
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(master.results, f, indent=2, ensure_ascii=False)
            print(f'Saved as {filepath}')

    print(f"Elapsed time in total (sec): {master.elapsed_time}")
    master.dismiss()

    assert judgment


def test_luma_video_to_video_instances(run_api):
    judgment = True
    master = LLMMaster()

    prompt = 'The Kung Fu boy is playing with other characters. Japanese anime style, suitable for children.'
    keyframes={
      "frame0": {
        "type": "generation",
        "id": "91cc1505-e362-4d17-8122-4e3e58ff85dc"
      }
    }
    params = master.pack_parameters(provider='lumaai_vtv',
                                    prompt=prompt,
                                    keyframes=keyframes)
    master.set_api_keys(API_KEY)
    master.summon({'luma_vtv': params})

    print(f"Parameters = {master.instances['luma_vtv'].parameters}")
    print(f"API Key = {master.instances['luma_vtv'].api_key}")

    if not isinstance(master.instances['luma_vtv'], LumaDreamMachineVideoToVideo):
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
        if isinstance(master.results['luma_vtv'], str):
            pytest.fail(f"Failed to generate: {master.results['luma_vtv']}")
        else:
            print(f"Result = {json.dumps(master.results, indent=2)}")
            filepath = os.path.join(TEST_OUTPUT_PATH, 'lumaai_vtv.json')
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(master.results, f, indent=2, ensure_ascii=False)
            print(f'Saved as {filepath}')

    print(f"Elapsed time in total (sec): {master.elapsed_time}")
    master.dismiss()

    assert judgment
