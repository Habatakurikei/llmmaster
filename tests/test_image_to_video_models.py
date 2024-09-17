import os
import sys
from requests.models import Response

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from llmmaster.image_to_video_models import StableDiffusionImageToVideo
from llmmaster import LLMMaster

API_KEY = '''
'''


TEST_OUTPUT_PATH = 'test-outputs'


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_stable_diffusion_image_to_video_instances(run_api):
    judgment = True
    master = LLMMaster()

    sd_itv_test = master.pack_parameters(provider='stable_diffusion_itv',
                                         image='test-inputs/elf_girl_1.png')
    master.set_api_keys(API_KEY)
    master.summon({'sd_itv_test': sd_itv_test})

    for name, instance in master.instances.items():
        msg = f"{name} = {instance}, {instance.parameters.keys()}, "
        msg += f"{instance.parameters['url']}, {instance.parameters['url_result']}, {instance.parameters['data']}"
        print(msg)
        if not isinstance(instance, StableDiffusionImageToVideo):
            judgment = False

    if run_api:
        # add --run-api option for making actual API calls test, paying API credit
        print('Run API')
        try:
            master.run()
        except Exception as e:
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        if not os.path.isdir(TEST_OUTPUT_PATH):
            os.makedirs(TEST_OUTPUT_PATH)

        print('Responses')
        for name, response in master.results.items():
            if isinstance(response, Response):
                filename = f'{name}.mp4'
                filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f'Saved as {filepath} for {name}')
            else:
                print(f'{name} = {response}')
                judgment = False

    print(f"Elapsed time (sec): {master.elapsed_time}")
    master.dismiss()

    assert judgment is True
