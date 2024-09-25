import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from conftest import execute_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.meshy_models import MeshyImageTo3D
from llmmaster.meshy_models import MeshyTextTo3D
from llmmaster.meshy_models import MeshyTextTo3DRefine
from llmmaster.meshy_models import MeshyTextToTexture
from llmmaster.meshy_models import MeshyTextToVoxel


# API_KEY = Path('api_key_pairs.txt').read_text(encoding='utf-8')
API_KEY = ''

NEGATIVE_PROMPT = 'ugly, low-resolution, multiple people'
PROMPT = """
age: 16;
gender: female;
height: 165cm;
figure: slim build;
hairstyle: light blue hair, ponytail;
eye color: blue;
cloths: pink dress; short sox; sneakers;
accesories: hair band with pink ribbon, leather gloves;
appearance features: nothing special;
Japanese anime style; Single Person; Full body; Face Front; White background;
"""


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_meshy_text_to_3d(run_api):
    judgment = True
    master = LLMMaster()

    id = ''
    key = 'meshy_tt3d'
    params = master.pack_parameters(provider=key,
                                    prompt=PROMPT,
                                    model='meshy-3-turbo',
                                    art_style='cartoon',
                                    negative_prompt=NEGATIVE_PROMPT,
                                    seed=10)
    # params = master.pack_parameters(provider=key,
    #                                 prompt=PROMPT,
    #                                 model='meshy-4',
    #                                 art_style='realistic',
    #                                 negative_prompt=NEGATIVE_PROMPT,
    #                                 seed=10,
    #                                 topology='quad',
    #                                 target_polycount=100000)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], MeshyTextTo3D)

    print('Step 1: Make text-to-3d model')
    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

        if 'id' in master.results[key]:
            id = master.results[key]['id']
            print(f"id = {id}")

    if run_api and id:

        print('Step 2: Refine the model')

        master.dismiss()
        key = 'meshy_tt3d_refine'
        params = master.pack_parameters(provider=key,
                                        preview_task_id=id,
                                        texture_richness='high')
        master.set_api_keys(API_KEY)
        master.summon({key: params})

        judgment = verify_instance(master.instances[key], MeshyTextTo3DRefine)

        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_meshy_text_to_texture(run_api):
    judgment = True
    master = LLMMaster()

    key = 'meshy_tttx'
    model_url = 'https://habatakurikei.com/dlfiles/zoltraak/model.glb'
    object_prompt = 'A girl in a pink dress with ponytail hair.'
    style_prompt = 'cherry blossum like kimono style outfit'

    params = master.pack_parameters(provider=key,
                                    model_url=model_url,
                                    object_prompt=object_prompt,
                                    style_prompt=style_prompt,
                                    enable_original_uv=True,
                                    enable_pbr=True,
                                    art_style='japanese-anime',
                                    negative_prompt=NEGATIVE_PROMPT,
                                    resolution='1024')
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], MeshyTextToTexture)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_meshy_text_to_voxel(run_api):
    judgment = True
    master = LLMMaster()

    key = 'meshy_ttvx'
    params = master.pack_parameters(provider=key,
                                    prompt=PROMPT,
                                    voxel_size_shrink_factor=8,
                                    negative_prompt=NEGATIVE_PROMPT,
                                    seed=10)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], MeshyTextToVoxel)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_meshy_image_to_3d(run_api):
    judgment = True
    master = LLMMaster()

    key = 'meshy_it3d'
    # image_url = 'https://assets.st-note.com/img/1725449361-rjBEAFQSfC6oecXxh718RndG.png'
    image_url = 'https://monju.ai/app/static/dragon_girl_2.png'
    params = master.pack_parameters(provider=key,
                                    image_url=image_url,
                                    enable_pbr=True)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], MeshyImageTo3D)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
