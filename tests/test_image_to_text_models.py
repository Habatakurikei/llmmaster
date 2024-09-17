import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from llmmaster.image_to_text_models import GoogleImageToText
from llmmaster.image_to_text_models import OpenAIImageToText
from llmmaster import LLMMaster


API_KEY = '''
'''


INSTANCE_CLASSES = {
    'google': GoogleImageToText,
    'openai': OpenAIImageToText,
}


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_openai_image_to_text_instances(run_api):
    judgment = True
    master = LLMMaster()

    test_cases = [
        {
            'name': 'openai_case_1',
            'params': {
                'provider': 'openai_itt',
                'model': 'gpt-4o-mini',
                'prompt': 'Describe this image.',
                'image_url': ['https://assets.st-note.com/img/1725449361-rjBEAFQSfC6oecXxh718RndG.png']
            }
        },
        {
            'name': 'openai_case_2',
            'params': {
                'provider': 'openai_itt',
                'model': 'gpt-4o-mini',
                'prompt': 'What are different between these two images?',
                'image_url': ['https://assets.st-note.com/production/uploads/images/152744645/rectangle_large_type_2_8bd3dd8828595922135ec877661d9cbe.png',
                              'https://assets.st-note.com/production/uploads/images/152744949/rectangle_large_type_2_7a85229175b92366e4059afe7927d811.png']
            }
        }
    ]

    master.set_api_keys(API_KEY)
    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        print(f'{name} = {instance}, {instance.parameters}')
        if not isinstance(instance, OpenAIImageToText):
            judgment = False
        if 'image_url' not in instance.parameters or not instance.parameters['image_url']:
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

    print(f'Elapsed time: {master.elapsed_time} seconds')
    master.dismiss()

    assert judgment is True


def test_google_image_to_text_instances(run_api):
    judgment = True
    master = LLMMaster()

    test_cases = [
        {
            'name': 'google_case_1',
            'params': {
                'provider': 'google_itt',
                'model': 'gemini-1.5-flash',
                'prompt': 'Describe this image.',
                'image_url': ['test-inputs/def_dragon_girl_2.png']
            }
        },
        {
            'name': 'google_case_2',
            'params': {
                'provider': 'google_itt',
                'model': 'gemini-1.5-flash',
                'prompt': 'What are different between these two images?',
                'image_url': ['https://assets.st-note.com/production/uploads/images/152744645/rectangle_large_type_2_8bd3dd8828595922135ec877661d9cbe.png',
                              'https://assets.st-note.com/production/uploads/images/152744949/rectangle_large_type_2_7a85229175b92366e4059afe7927d811.png']
            }
        }
    ]

    master.set_api_keys(API_KEY)
    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        print(f'{name} = {instance}, {instance.parameters}')
        if not isinstance(instance, GoogleImageToText):
            judgment = False
        if 'image_url' not in instance.parameters or not instance.parameters['image_url']:
            judgment = False

    if run_api:
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

    print(f'Elapsed time: {master.elapsed_time} seconds')
    master.dismiss()

    assert judgment is True
