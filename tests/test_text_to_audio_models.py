import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from conftest import TEST_OUTPUT_PATH
from conftest import execute_elevenlabs
from conftest import execute_restapi
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.text_to_audio_models import ElevenLabsTextToSoundEffect
from llmmaster.text_to_audio_models import ElevenLabsTextToSpeech
from llmmaster.text_to_audio_models import OpenAITextToSpeech
from llmmaster.text_to_audio_models import VoicevoxTextToSpeech


# API_KEY = Path('api_key_pairs.txt').read_text(encoding='utf-8')
API_KEY = ''

PROMPT_EN = "Do not concentrate on the finger, or you will miss all that heavenly glory."
PROMPT_JA = "こんにちは。今日もいい天気ですね！"


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_openai_text_to_speech(run_api):
    judgment = True
    master = LLMMaster()

    key = 'openai_tts'
    test_cases = [
        {
            'name': f'{key}_1',
            'params': {
                'provider': key,
                'prompt': PROMPT_EN,
                'voice': 'echo',
                'speed': 0.5
            }
        },
        {
            'name': f'{key}_2',
            'params': {
                'provider': key,
                'prompt': PROMPT_EN,
                'voice': 'fable',
                'speed': 1.5,
                'response_format': 'opus'
            }
        },
        {
            'name': f'{key}_3',
            'params': {
                'provider': key,
                'prompt': PROMPT_EN,
                'voice': 'onyx',
                'model': 'tts-1',
                'response_format': 'aac'
            }
        },
        {
            'name': f'{key}_4',
            'params': {
                'provider': key,
                'prompt': PROMPT_EN,
                'voice': 'nova',
                'model': 'tts-1-hd'
            }
        },
        {
            'name': f'{key}_5',
            'params': {
                'provider': key,
                'prompt': PROMPT_EN,
                'voice': 'shimmer',
                'response_format': 'opus'
            }
        },
    ]

    master.set_api_keys(API_KEY)
    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        judgment = verify_instance(instance, OpenAITextToSpeech)
        if judgment is False:
            pytest.fail(f'{name} is not an expected instance.')

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
                pytest.fail(f'Response for {name} is not binary: {response}')

            ext = master.instances[name].parameters.get('response_format',
                                                        'mp3')
            save_as = os.path.join(TEST_OUTPUT_PATH, f"{name}.{ext}")
            with open(save_as, 'wb') as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
            print(f'Saved as {save_as} for {name}')

    print(f'Elapsed time: {master.elapsed_time} seconds')
    master.dismiss()

    assert judgment


def test_elevenlabs_text_to_speech(run_api):
    judgment = True
    master = LLMMaster()

    key = 'elevenlabs_tts'
    params = master.pack_parameters(provider=key, prompt=PROMPT_JA)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key],
                               ElevenLabsTextToSpeech)

    if run_api:
        try:
            execute_elevenlabs(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_elevenlabs_text_to_sound(run_api):
    judgment = True
    master = LLMMaster()

    key = 'elevenlabs_ttse'
    prompt = 'Drinking a glass of water.'
    params = master.pack_parameters(provider=key, prompt=prompt)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key],
                               ElevenLabsTextToSoundEffect)

    if run_api:
        try:
            execute_elevenlabs(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_voicevox_text_to_speech(run_api):
    judgment = True
    master = LLMMaster()

    key = 'voicevox_tts'
    # master.set_api_keys(API_KEY) is not necessary
    for speaker in range(1, 3):
        case = master.pack_parameters(provider=key,
                                      prompt=PROMPT_JA,
                                      speaker=speaker)
        master.summon({f'{key}_{speaker}': case})

    for name, instance in master.instances.items():
        judgment = verify_instance(instance, VoicevoxTextToSpeech)
        if judgment is False:
            pytest.fail(f'{name} is not an expected instance.')

    if run_api:
        try:
            execute_restapi(master, format='wav')
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
