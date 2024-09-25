import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.video_to_text_models import GoogleVideoToText


# API_KEY = Path('api_key_pairs.txt').read_text(encoding='utf-8')
API_KEY = ''


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_google_vtt(run_api):
    judgment = True
    master = LLMMaster()

    key = 'google_vtt'
    file_path = 'test-inputs/test_video.mp4'
    params = master.pack_parameters(provider=key,
                                    model='gemini-1.5-flash',
                                    prompt='Describe attached video.',
                                    video_file=file_path)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], GoogleVideoToText)

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
