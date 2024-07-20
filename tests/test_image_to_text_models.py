import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from llmmaster.image_to_text_models import GoogleImageToText
from llmmaster.image_to_text_models import OpenAIImageToText
from llmmaster import LLMMaster


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
                'model': 'gpt-4o',
                'prompt': 'Describe this image.',
                'image_url': ['https://habatakurikei.com/wp-content/uploads/2022/03/sleep-tracker-collection-202203.jpg']
            }
        },
        {
            'name': 'openai_case_2',
            'params': {
                'provider': 'openai_itt',
                'model': 'gpt-4o',
                'prompt': 'Which photo is more described Europe and why?',
                'image_url': ['https://habatakurikei.com/wp-content/uploads/2018/06/cover-singapore-opt.jpg',
                              'https://habatakurikei.com/wp-content/uploads/2018/05/cover-gent-old-town-opt.jpg']
            }
        }
    ]

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
                'image_url': ['test-inputs/test_image.png']
            }
        },
        {
            'name': 'google_case_2',
            'params': {
                'provider': 'google_itt',
                'model': 'gemini-1.5-flash',
                'prompt': 'Which brand of sleep tracker does seem more beneficial for users?',
                'image_url': ['https://habatakurikei.com/wp-content/uploads/2022/11/sleep-tracker-applewatch-sample.png',
                              'https://habatakurikei.com/wp-content/uploads/2020/02/sleep-tracker-fitbit-sample.png']
            }
        }
    ]

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
