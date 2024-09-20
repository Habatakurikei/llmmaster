import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest
import requests
from requests.models import Response

from llmmaster.config import REQUEST_OK
from llmmaster.image_to_image_models import OpenAIImageToImage
from llmmaster.image_to_image_models import StableDiffusionImageToImage
from llmmaster.image_to_image_models import Flux1FalImageToImage
from llmmaster import LLMMaster


API_KEY = '''
'''


TEST_IMAGE = 'test-inputs/test_image.png'
TEST_MASK = 'test-inputs/test_mask.png'
TEST_OUTPUT_PATH = 'test-outputs'


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_openai_image_to_image_instances(run_api):
    judgment = True
    master = LLMMaster()

    edit_prompt = 'Add a white cat to the center of the image'

    test_cases = [
        {'name': 'case_1_edits', 'params': {'provider': 'openai_iti', 'mode': 'edits', 'image': TEST_IMAGE, 'prompt': edit_prompt}},
        {'name': 'case_2_variations', 'params': {'provider': 'openai_iti', 'mode': 'variations', 'image': TEST_IMAGE, 'n': 2}},
        {'name': 'case_3_edits_with_mask', 'params': {'provider': 'openai_iti', 'mode': 'edits', 'image': TEST_IMAGE, 'mask': TEST_MASK, 'prompt': edit_prompt, 'size': '512x512', 'n': 2}},
    ]

    master.set_api_keys(API_KEY)
    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        print(f'{name} = {instance}, {instance.parameters}')
        if not isinstance(instance, OpenAIImageToImage):
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
        for name, response in master.results.items():
            if hasattr(response, 'data'):
                for i in range(len(response.data)):
                    image_response = requests.get(response.data[i].url)
                    if image_response.status_code == REQUEST_OK:
                        filename = f"{name}_{i+1:02}.png"
                        filepath = os.path.join(TEST_OUTPUT_PATH, filename)
                        with open(filepath, 'wb') as f:
                            f.write(image_response.content)
                        print(f'{name} = Image saved to {filepath}')
                    else:
                        pytest.fail(f'{name} = Failed to download image from {response}')
            else:
                pytest.fail(f'{name} = Unexpected response type for {name}: {type(response)}')

    print(f'Elapsed time (sec): {master.elapsed_time}')
    master.dismiss()

    assert judgment is True


def test_stable_diffusion_image_to_image_instances(run_api):
    judgment = True
    master = LLMMaster()

    upscale_image = 'test-inputs/frieren.png'

    upscale_prompt = 'An anime elf girl.'
    inpaint_prompt = 'A white cat.'
    outpaint_prompt = 'A white cat.'
    search_prompt = 'An animal playing the viorin.'

    test_cases = [
        {'name': 'case_1_upscale_conservative', 'params': {'provider': 'stable_diffusion_iti', 'mode': 'upscale_conservative', 'image': upscale_image, 'prompt': upscale_prompt}},
        {'name': 'case_2_upscale_creative', 'params': {'provider': 'stable_diffusion_iti', 'mode': 'upscale_creative', 'image': upscale_image, 'prompt': upscale_prompt, 'creativity': 0.3}},
        {'name': 'case_3_erase', 'params': {'provider': 'stable_diffusion_iti', 'mode': 'erase', 'image': TEST_IMAGE, 'mask': TEST_MASK}},
        {'name': 'case_4_inpaint', 'params': {'provider': 'stable_diffusion_iti', 'mode': 'inpaint', 'image': TEST_IMAGE, 'prompt': inpaint_prompt}},
        {'name': 'case_5_outpaint', 'params': {'provider': 'stable_diffusion_iti', 'mode': 'outpaint', 'image': TEST_IMAGE, 'prompt': outpaint_prompt, 'left': 64, 'right': 64}},
        {'name': 'case_6_search_and_replace', 'params': {'provider': 'stable_diffusion_iti', 'mode': 'search_and_replace', 'image': TEST_IMAGE, 'prompt': inpaint_prompt, 'search_prompt': search_prompt}},
        {'name': 'case_7_remove_background', 'params': {'provider': 'stable_diffusion_iti', 'mode': 'remove_background', 'image': TEST_IMAGE}},
    ]

    master.set_api_keys(API_KEY)
    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        print(f'{name} = {instance}, {instance.parameters}')
        if not isinstance(instance, StableDiffusionImageToImage):
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
        for name, response in master.results.items():
            if isinstance(response, Response):
                if 'output_format' in master.instances[name].parameters:
                    save_as = f'{name}.{master.instances[name].parameters["output_format"]}'
                else:
                    save_as = f'{name}.png'

                filepath = os.path.join(TEST_OUTPUT_PATH, save_as)

                with open(filepath, 'wb') as f:
                    if isinstance(response.content, bytes):
                        f.write(response.content)
                        print(f'{name} = {filepath} saved')
                    else:
                        print(f"Unexpected response type for {name}: {type(response)}")

            else:
                print(f'{name} = {response}')
                judgment = False

    print(f'Elapsed time (sec): {master.elapsed_time}')
    master.dismiss()

    assert judgment is True


def test_flux1_image_to_image_instances(run_api):
    judgment = True
    master = LLMMaster()

    prompt = 'The girl smiling with her eyes closed. The words "SHIN monju" are painted in front, in Japanese caligraphy style.'
    url = 'https://monju.ai/app/static/monju-girl.png'

    arguments = master.pack_parameters(
        provider = 'flux1_fal_iti',
        strength = 0.95,
        image_url = url,
        prompt = prompt,
        image_size = 'landscape_16_9',
        num_inference_steps = 40,
        seed = 0,
        guidance_scale = 3.5,
        sync_mode = False,
        num_images = 1,
        enable_safety_checker = True
    )

    master.summon({'flux1_fal_iti': arguments})    
    print(f"Parameters = {master.instances['flux1_fal_iti'].parameters}")

    if not isinstance(master.instances['flux1_fal_iti'], Flux1FalImageToImage):
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
        if isinstance(master.results['flux1_fal_iti'], str):
            pytest.fail(f"Failed to generate: {master.results['flux1_fal_iti']}")
        else:
            print(f"Result = {json.dumps(master.results, indent=2)}")
            filepath = os.path.join(TEST_OUTPUT_PATH, 'flux1_fal_iti.json')
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(master.results, f, indent=2, ensure_ascii=False)
            print(f'Saved as {filepath}')

    print(f"Elapsed time in total (sec): {master.elapsed_time}")
    master.dismiss()

    assert judgment
