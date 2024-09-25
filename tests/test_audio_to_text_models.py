import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.audio_to_text_models import GoogleSpeechToText
from llmmaster.audio_to_text_models import OpenAISpeechToText


# API_KEY = Path('api_key_pairs.txt').read_text(encoding='utf-8')
API_KEY = ''


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_openai_speech_to_text(run_api):
    judgment = True
    master = LLMMaster()

    key = 'openai_stt'
    file_path = 'test-inputs/test_speech.mp3'
    test_cases = [
        {
            'name': f'{key}_1',
            'params': {
                'provider': key,
                'mode': 'translations',
                'file': file_path,
                'response_format': 'json',
                'temperature': 0.0
            }
        },
        {
            'name': f'{key}_2',
            'params': {
                'provider': key,
                'mode': 'transcriptions',
                'file': file_path,
                'response_format': 'text'
            }
        },
        {
            'name': f'{key}_3',
            'params': {
                'provider': key,
                'mode': 'transcriptions',
                'file': file_path,
                'response_format': 'verbose_json'
            }
        }
    ]

    master.set_api_keys(API_KEY)
    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        judgment = verify_instance(instance, OpenAISpeechToText)
        if judgment is False:
            pytest.fail(f'{name} is not an expected instance.')

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_google_speech_to_text(run_api):
    judgment = True
    master = LLMMaster()

    key = 'google_stt'
    file_path = 'test-inputs/enter_the_dragon.mp3'
    prompt = 'Make a transcript for attached audio file.'
    params = master.pack_parameters(provider=key,
                                    prompt=prompt,
                                    audio_file=file_path)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], GoogleSpeechToText)

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
