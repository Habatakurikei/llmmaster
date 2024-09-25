import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from conftest import execute_llmmaster
from conftest import execute_restapi
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.image_to_image_models import OpenAIImageToImage
from llmmaster.image_to_image_models import StableDiffusionImageToImage
from llmmaster.image_to_image_models import Flux1FalImageToImage


# API_KEY = Path('api_key_pairs.txt').read_text(encoding='utf-8')
API_KEY = ''

PROMPT_FLUX1FAL_EDIT = """
The girl in the picture makes smiling with her eyes closed.
The words "SHIN monju" are painted in front, in Japanese caligraphy style.
"""

TEST_IMAGE = 'test-inputs/test_image.png'
TEST_MASK = 'test-inputs/test_mask.png'


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_openai_image_to_image(run_api):
    judgment = True
    master = LLMMaster()

    key = 'openai_iti'
    edit_prompt = 'Add a white cat to the center of the attached image'

    test_cases = [
        {
            'name': f'{key}_1',
            'params': {
                'provider': key,
                'mode': 'variations',
                'image': TEST_IMAGE,
                'n': 2
            }
        },
        {
            'name': f'{key}_2',
            'params': {
                'provider': key,
                'mode': 'edits',
                'image': TEST_IMAGE,
                'mask': TEST_MASK,
                'prompt': edit_prompt,
                'size': '512x512',
                'n': 2
            }
        }
    ]
    master.set_api_keys(API_KEY)
    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        judgment = verify_instance(instance, OpenAIImageToImage)
        if judgment is False:
            pytest.fail(f'{name} is not an expected instance.')

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_stable_diffusion_image_to_image(run_api):
    judgment = True
    master = LLMMaster()

    key = 'stable_diffusion_iti'

    upscale_image = 'test-inputs/frieren.png'

    upscale_prompt = 'An anime elf girl.'
    inpaint_prompt = 'A white cat.'
    outpaint_prompt = 'A white cat.'
    search_prompt = 'An animal playing the viorin.'

    test_cases = [
        {
            'name': f'{key}_1',
            'params': {
                'provider': key,
                'mode': 'upscale_conservative',
                'image': upscale_image,
                'prompt': upscale_prompt
            }
        },
        {
            'name': f'{key}_2',
            'params': {
                'provider': key,
                'mode': 'upscale_creative',
                'image': upscale_image,
                'prompt': upscale_prompt,
                'creativity': 0.7
            }
        },
        {
            'name': f'{key}_3',
            'params': {
                'provider': key,
                'mode': 'erase',
                'image': TEST_IMAGE,
                'mask': TEST_MASK
            }
        },
        {
            'name': f'{key}_4',
            'params': {
                'provider': key,
                'mode': 'inpaint',
                'image': TEST_IMAGE,
                'prompt': inpaint_prompt
            }
        },
        {
            'name': f'{key}_5',
            'params': {
                'provider': key,
                'mode': 'outpaint',
                'image': TEST_IMAGE,
                'prompt': outpaint_prompt,
                'left': 64,
                'right': 64}
            },
        {
            'name': f'{key}_6',
            'params': {
                'provider': key,
                'mode': 'search_and_replace',
                'image': TEST_IMAGE,
                'prompt': inpaint_prompt,
                'search_prompt': search_prompt
            }
        },
        {
            'name': f'{key}_7',
            'params': {
                'provider': key,
                'mode': 'remove_background',
                'image': TEST_IMAGE
            }
        }
    ]
    master.set_api_keys(API_KEY)
    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        judgment = verify_instance(instance, StableDiffusionImageToImage)
        if judgment is False:
            pytest.fail(f'{name} is not an expected instance.')

    if run_api:
        try:
            execute_restapi(master, format='png')
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_flux1_image_to_image_instances(run_api):
    judgment = True
    master = LLMMaster()

    key = 'flux1_fal_iti'
    url = 'https://monju.ai/app/static/monju-girl.png'

    arguments = master.pack_parameters(
        provider=key,
        strength=0.95,
        image_url=url,
        prompt=PROMPT_FLUX1FAL_EDIT,
        image_size='landscape_16_9',
        num_inference_steps=40,
        seed=0,
        guidance_scale=3.5,
        sync_mode=False,
        num_images=1,
        enable_safety_checker=True
    )
    master.summon({key: arguments})
    judgment = verify_instance(master.instances[key], Flux1FalImageToImage)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
