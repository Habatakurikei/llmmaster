import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from conftest import execute_elevenlabs
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.audio_to_audio_models import ElevenLabsAudioIsolation


# API_KEY = Path('api_key_pairs.txt').read_text(encoding='utf-8')
API_KEY = ''


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_elevenlabs_audio_isolation(run_api):
    judgment = True
    master = LLMMaster()

    key = 'elevenlabs_aiso'
    audio_path = 'test-inputs/pe.m4a'
    params = master.pack_parameters(provider=key,
                                    audio=audio_path)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], ElevenLabsAudioIsolation)

    if run_api:
        try:
            execute_elevenlabs(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
