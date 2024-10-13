import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from conftest import execute_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.skybox_models import SkyboxTextToPanorama
from llmmaster.skybox_models import SkyboxPanoramaToImageVideo

API_KEY = Path('api_key_pairs.txt').read_text(encoding='utf-8')
# API_KEY = ''

NEGATIVE_PROMPT = 'ugly, dirty, low-resolution'
PROMPT = """
A Japanese temple, surrounded by mountains, with cherry blossoms, in spring.
"""


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_skybox_text_to_panorama(run_api):
    judgment = True
    master = LLMMaster()

    key = 'skybox_ttp'
    params = master.pack_parameters(provider=key,
                                    prompt=PROMPT,
                                    skybox_style_id=138,
                                    negative_text=NEGATIVE_PROMPT,
                                    enhance_prompt=True,
                                    seed=12345)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], SkyboxTextToPanorama)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_skybox_export(run_api):
    judgment = True
    master = LLMMaster()

    skybox_id = 'ccbf3ed68c6e556c033b641b616ee830'

    key = 'skybox_ptiv'
    params = master.pack_parameters(provider=key,
                                    skybox_id=skybox_id,
                                    type_id=7)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key],
                               SkyboxPanoramaToImageVideo)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
