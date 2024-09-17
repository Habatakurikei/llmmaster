import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from llmmaster.audio_to_text_models import GoogleSpeechToText
from llmmaster.audio_to_text_models import OpenAISpeechToText
from llmmaster import LLMMaster


API_KEY = '''
'''


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_openai_speech_to_text_instances(run_api):
    judgment = True
    master = LLMMaster()

    test_cases = [
        {
            'name': 'openai_stt_case_1',
            'params': {
                'provider': 'openai_stt',
                'mode': 'translations',
                'file': 'test-inputs/test_speech.mp3',
                'response_format': 'json',
                'temperature': 0.0
            }
        },
        {
            'name': 'openai_stt_case_2',
            'params': {
                'provider': 'openai_stt',
                'mode': 'transcriptions',
                'file': 'test-inputs/test_speech.mp3',
                'response_format': 'text'
            }
        },
        {
            'name': 'openai_stt_case_3',
            'params': {
                'provider': 'openai_stt',
                'mode': 'transcriptions',
                'file': 'test-inputs/test_speech.mp3',
                'response_format': 'verbose_json'
            }
        }
    ]

    master.set_api_keys(API_KEY)
    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        print(f'{name} = {instance}, {instance.parameters}')
        if not isinstance(instance, OpenAISpeechToText):
            judgment = False
        if 'file' not in instance.parameters or not instance.parameters['file']:
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


def test_google_speech_to_text_instances(run_api):
    judgment = True
    master = LLMMaster()

    params = master.pack_parameters(provider='google_stt',
                                    prompt='Make a transcript for attached audio file.',
                                    audio_file='test-inputs/enter_the_dragon.mp3')
    master.set_api_keys(API_KEY)
    master.summon({'google_stt': params})

    print(f'{master.instances["google_stt"]} = {master.instances["google_stt"].parameters}')
    if not isinstance(master.instances["google_stt"], GoogleSpeechToText):
        judgment = False

    if run_api:
        # add --run-api option for making actual API calls test, paying API credit
        print('Run API')
        try:
            master.run()
        except Exception as e:
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        if not master.results["google_stt"]:
            judgment = False
        else:
            print(f'Google stt responsed: {master.results["google_stt"]}')

    print(f'Elapsed time: {master.elapsed_time} seconds')
    master.dismiss()

    assert judgment is True
