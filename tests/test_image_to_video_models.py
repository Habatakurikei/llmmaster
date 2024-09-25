import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from conftest import execute_restapi
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.image_to_video_models import StableDiffusionImageToVideo


# API_KEY = Path('api_key_pairs.txt').read_text(encoding='utf-8')
API_KEY = ''


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_stable_diffusion_image_to_video(run_api):
    judgment = True
    master = LLMMaster()

    key = 'stable_diffusion_itv'
    file_path = 'test-inputs/elf_girl_1.png'
    params = master.pack_parameters(provider=key,
                                    image=file_path,
                                    cfg_scale=5.0,
                                    motion_bucket_id=50)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key],
                               StableDiffusionImageToVideo)

    if run_api:
        try:
            execute_restapi(master, format='mp4')
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
