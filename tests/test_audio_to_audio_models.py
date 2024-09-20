import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest
import elevenlabs
from requests.models import Response

from llmmaster.audio_to_audio_models import ElevenLabsAudioIsolation
from llmmaster import LLMMaster


API_KEY = '''
'''


TEST_OUTPUT_PATH = 'test-outputs'


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_elevenlabs_audio_isolation(run_api):
    judgment = True
    master = LLMMaster()

    audio_path = 'test-inputs/pe.m4a'
    test_case = master.pack_parameters(provider='elevenlabs_aiso',
                                       audio=audio_path)

    master.set_api_keys(API_KEY)
    master.summon({'elevenlabs_aiso': test_case})

    print(f'elevenlabs_aiso = {master.instances["elevenlabs_aiso"]}, {master.instances["elevenlabs_aiso"].parameters}')
    if not isinstance(master.instances["elevenlabs_aiso"], ElevenLabsAudioIsolation):
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
        if not master.results['elevenlabs_aiso']:
            judgment = False
        else:
            filepath = os.path.join(TEST_OUTPUT_PATH, 'elevenlabs_aiso.mp3')
            elevenlabs.save(master.results['elevenlabs_aiso'], filepath)
            print(f'Saved as {filepath} for elevenlabs_aiso')

    print(f'Elapsed time: {master.elapsed_time} seconds')
    master.dismiss()

    assert judgment is True
