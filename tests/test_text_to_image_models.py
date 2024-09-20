import json
import os
import requests
import sys
from requests.models import Response

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from llmmaster.config import REQUEST_OK
from llmmaster.text_to_image_models import OpenAITextToImage
from llmmaster.text_to_image_models import StableDiffusionTextToImage
from llmmaster.text_to_image_models import Flux1FalTextToImage
from llmmaster import LLMMaster


API_KEY = '''
'''


TEST_OUTPUT_PATH = 'test-outputs'


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_openai_text_to_image_instances(run_api):
    judgment = True
    master = LLMMaster()
    prompt = 'An anime girl saying Hello, smiling.'

    test_cases = [
        {'name': 'case_1_min_params', 'params': {'provider': 'openai_tti', 'prompt': prompt}},
        {'name': 'case_2_dall_e_3_standard', 'params': {'provider': 'openai_tti', 'model': 'dall-e-3', 'prompt': prompt, 'size': '1024x1024', 'quality': 'standard', 'n': 1}},
        {'name': 'case_3_dall_e_3_hd', 'params': {'provider': 'openai_tti', 'model': 'dall-e-3', 'prompt': prompt, 'size': '1024x1792', 'quality': 'hd', 'n': 1}},
        {'name': 'case_4_dall_e_2', 'params': {'provider': 'openai_tti', 'model': 'dall-e-2', 'prompt': prompt, 'size': '256x256', 'n': 1}},
        {'name': 'case_5_dall_e_2_max_n', 'params': {'provider': 'openai_tti', 'model': 'dall-e-2', 'prompt': prompt, 'size': '256x256', 'quality': 'standard', 'n': 3}},
        {'name': 'case_6_invalid_size', 'params': {'provider': 'openai_tti', 'prompt': prompt, 'size': '1000x1000'}},
        {'name': 'case_7_invalid_quality', 'params': {'provider': 'openai_tti', 'prompt': prompt, 'quality': 'ultra'}},
        {'name': 'case_8_invalid_n', 'params': {'provider': 'openai_tti', 'prompt': prompt, 'n': 5}},
    ]
    master.set_api_keys(API_KEY)
    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        print(f'{name} = {instance}, {instance.parameters}')
        if not isinstance(instance, OpenAITextToImage):
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


def test_stable_diffusion_text_to_image_instances(run_api):
    judgment = True
    master = LLMMaster()
    prompt = 'An anime girl saying Hello, smiling.'

    test_cases = [
        {'name': 'case_1_min_params', 'params': {'provider': 'stable_diffusion_tti', 'prompt': prompt}},
        {'name': 'case_2_core_model', 'params': {'provider': 'stable_diffusion_tti', 'model': 'core', 'prompt': prompt, 'aspect_ratio': '1:1', 'style_preset': 'photographic'}},
        {'name': 'case_3_ultra_model', 'params': {'provider': 'stable_diffusion_tti', 'model': 'ultra', 'prompt': prompt, 'aspect_ratio': '3:2', 'output_format': 'png'}},
        {'name': 'case_4_with_negative_prompt', 'params': {'provider': 'stable_diffusion_tti', 'prompt': prompt, 'negative_prompt': 'blurry, low quality'}},
        {'name': 'case_5_with_seed', 'params': {'provider': 'stable_diffusion_tti', 'prompt': prompt, 'seed': 12345}},
        {'name': 'case_6_invalid_model', 'params': {'provider': 'stable_diffusion_tti', 'model': 'invalid_model', 'prompt': prompt}},
        {'name': 'case_7_invalid_aspect_ratio', 'params': {'provider': 'stable_diffusion_tti', 'prompt': prompt, 'aspect_ratio': '5:5'}},
        {'name': 'case_8_invalid_style_preset', 'params': {'provider': 'stable_diffusion_tti', 'model': 'core', 'prompt': prompt, 'style_preset': 'invalid_style'}},
    ]
    master.set_api_keys(API_KEY)
    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        print(f'{name} = {instance}, {instance.parameters}')
        if not isinstance(instance, StableDiffusionTextToImage):
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
            if isinstance(response, str):
                print(f'{name} = {response}')

            elif isinstance(response, Response):
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
                        print(f"Unexpected response type for response.content of {name}: {type(response.content)}")

            else:
                pytest.fail(f'Unexpected response type for {name}: {type(response)}')

    print(f'Elapsed time (sec): {master.elapsed_time}')
    master.dismiss()

    assert judgment is True


def test_flux1fal_text_to_image_instances(run_api):
    judgment = True
    master = LLMMaster()

    prompt = 'A Japanese anime girl inspired by Akira Toriyama. Light blue hair, ponytail, pink dress, smiling at the camera. High resolution.'

    arguments = master.pack_parameters(
        provider = 'flux1_fal_tti',
        model = 'fal-ai/flux/schnell',
        prompt = prompt,
        image_size = 'landscape_16_9',
        num_inference_steps = 4,
        seed = 0,
        guidance_scale = 3.5,
        sync_mode = False,
        num_images = 1,
        enable_safety_checker = True
    )

    master.summon({'flux1_fal_tti': arguments})    
    print(f"Parameters = {master.instances['flux1_fal_tti'].parameters}")

    if not isinstance(master.instances['flux1_fal_tti'], Flux1FalTextToImage):
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
        if isinstance(master.results['flux1_fal_tti'], str):
            pytest.fail(f"Failed to generate: {master.results['flux1_fal_tti']}")
        else:
            print(f"Result = {json.dumps(master.results, indent=2)}")
            filepath = os.path.join(TEST_OUTPUT_PATH, 'flux1_fal_tti.json')
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(master.results, f, indent=2, ensure_ascii=False)
            print(f'Saved as {filepath}')

    print(f"Elapsed time in total (sec): {master.elapsed_time}")
    master.dismiss()

    assert judgment
