import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from llmmaster.text_to_image_models import OpenAITextToImage
from llmmaster.text_to_image_models import StableDiffusionTextToImage
from llmmaster import LLMMaster


INSTANCE_CLASSES = {
    'openai_tti': OpenAITextToImage,
    'stable_diffusion_tti': StableDiffusionTextToImage
}


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

        print('Responses')
        for name, response in master.results.items():
            print(f'{name} = {response}')
            if not response:
                judgment = False

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

        print('Responses')
        for name, response in master.results.items():
            if isinstance(response, str):
                print(f'{name} = {response}')
            else:
                if 'output_format' in master.instances[name].parameters:
                    save_as = f'{name}.{master.instances[name].parameters["output_format"]}'
                else:
                    save_as = f'{name}.png'

                with open(save_as, 'wb') as f:
                    if isinstance(response, bytes):
                        f.write(response)
                        print(f'{name} = {save_as} saved')
                    else:
                        print(f"Unexpected response type for {name}: {type(response)}")

    master.dismiss()

    assert judgment is True
