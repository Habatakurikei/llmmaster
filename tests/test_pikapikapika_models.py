import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from conftest import execute_llmmaster
from conftest import verify_instance
from llmmaster.pikapikapika_models import PikaPikaPikaGeneration
from llmmaster import LLMMaster


# API_KEY = Path('api_key_pairs.txt').read_text(encoding='utf-8')
API_KEY = ''


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_pikapikapika_text_to_video(run_api):
    judgment = True
    master = LLMMaster()

    key = 'pikapikapika_ttv'
    prompt = 'A Japanese anime girl inspired by Akira Toriyama. Light blue hair, ponytail, pink dress, full body, winking with full smile.'
    camera = {'zoom': 'in'}
    parameters = {"guidanceScale": 16, "motion": 2, "negativePrompt": "ugly"}

    params = master.pack_parameters(provider=key,
                                    prompt=prompt,
                                    style='Anime',
                                    sfx=True,
                                    frameRate=24,
                                    aspectRatio='16:9',
                                    camera=camera,
                                    parameters=parameters)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key],
                               PikaPikaPikaGeneration)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
