import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.image_to_text_models import GoogleImageToText
from llmmaster.image_to_text_models import OpenAIImageToText


# API_KEY = Path('api_key_pairs.txt').read_text(encoding='utf-8')
API_KEY = ''

IMAGE_URL_1 = 'https://assets.st-note.com/production/uploads/images/152744645/rectangle_large_type_2_8bd3dd8828595922135ec877661d9cbe.png'
IMAGE_URL_2 = 'https://assets.st-note.com/production/uploads/images/152744949/rectangle_large_type_2_7a85229175b92366e4059afe7927d811.png'
IMAGE_URL_3 = 'https://assets.st-note.com/img/1725449361-rjBEAFQSfC6oecXxh718RndG.png'


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_openai_image_to_text(run_api):
    judgment = True
    master = LLMMaster()

    key = 'openai_itt'
    model = 'gpt-4o-mini'
    test_cases = [
        {
            'name': f'{key}_1',
            'params': {
                'provider': key,
                'model': model,
                'prompt': 'Describe this image.',
                'image_url': [IMAGE_URL_3]
            }
        },
        {
            'name': f'{key}_2',
            'params': {
                'provider': key,
                'model': model,
                'prompt': 'What are different between these two images?',
                'image_url': [IMAGE_URL_1, IMAGE_URL_2]
            }
        }
    ]

    master.set_api_keys(API_KEY)
    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        judgment = verify_instance(instance, OpenAIImageToText)
        if judgment is False:
            pytest.fail(f'{name} is not an expected instance.')

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_google_image_to_text(run_api):
    judgment = True
    master = LLMMaster()

    key = 'google_itt'
    model = 'gemini-1.5-flash'
    test_cases = [
        {
            'name': f'{key}_1',
            'params': {
                'provider': key,
                'model': model,
                'prompt': 'Describe this image.',
                'image_url': ['test-inputs/dragon_girl_1.png']
            }
        },
        {
            'name': f'{key}_2',
            'params': {
                'provider': key,
                'model': 'gemini-1.5-flash',
                'prompt': 'What are different between these two images?',
                'image_url': [IMAGE_URL_1, IMAGE_URL_2]
            }
        }
    ]

    master.set_api_keys(API_KEY)
    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        judgment = verify_instance(instance, GoogleImageToText)
        if judgment is False:
            pytest.fail(f'{name} is not an expected instance.')

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
