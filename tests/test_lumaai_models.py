import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from conftest import execute_llmmaster
from conftest import verify_instance
from llmmaster.lumaai_models import LumaDreamMachineTextToVideo
from llmmaster.lumaai_models import LumaDreamMachineImageToVideo
from llmmaster.lumaai_models import LumaDreamMachineVideoToVideo
from llmmaster import LLMMaster


# API_KEY = Path('api_key_pairs.txt').read_text(encoding='utf-8')
API_KEY = ''


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_luma_text_to_video(run_api):
    judgment = True
    master = LLMMaster()

    key = 'lumaai_ttv'
    prompt = 'A teenager beast master, in a robe and crown hat, '
    prompt += 'smiling, swinging his wand, 3 cute monsters around, '
    prompt += 'dancing, rainbow background, japanese cartoon style'
    params = master.pack_parameters(provider=key,
                                    prompt=prompt,
                                    aspect_ratio='16:9',
                                    loop=True)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key],
                               LumaDreamMachineTextToVideo)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_luma_image_to_video(run_api):
    judgment = True
    master = LLMMaster()

    key = 'lumaai_itv'
    prompt = 'The girl in the picture makes smile with her eyes closed.'
    image_path = 'https://monju.ai/app/static/monju-logo.jpg'

    params = master.pack_parameters(provider=key,
                                    prompt=prompt,
                                    frame0=image_path)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key],
                               LumaDreamMachineImageToVideo)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_luma_video_to_video(run_api):
    judgment = True
    master = LLMMaster()

    key = 'lumaai_vtv'
    prompt = 'The Kung Fu boy is playing with other characters. '
    prompt += 'Japanese anime style, suitable for children.'
    keyframes = {
      "frame0": {
        "type": "generation",
        "id": "91cc1505-e362-4d17-8122-4e3e58ff85dc"
      }
    }
    params = master.pack_parameters(provider=key,
                                    prompt=prompt,
                                    keyframes=keyframes)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key],
                               LumaDreamMachineVideoToVideo)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
