import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from conftest import execute_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.tripo_models import TripoTextTo3D
from llmmaster.tripo_models import TripoImageTo3D
from llmmaster.tripo_models import TripoMultiviewTo3D
from llmmaster.tripo_models import TripoRefineModel
from llmmaster.tripo_models import TripoAnimationPreRigCheck
from llmmaster.tripo_models import TripoAnimationRig
from llmmaster.tripo_models import TripoAnimationRetarget
from llmmaster.tripo_models import TripoStylization
from llmmaster.tripo_models import TripoConversion

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


def test_tripo_text_to_3d(run_api):
    judgment = True
    master = LLMMaster()

    key = 'tripo_tt3d'
    params = master.pack_parameters(provider=key,
                                    prompt=PROMPT,
                                    negative_prompt=NEGATIVE_PROMPT)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], TripoTextTo3D)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_tripo_image_to_3d(run_api):
    judgment = True
    master = LLMMaster()

    key = 'tripo_it3d'
    image_url = 'test-inputs/dragon_girl_2.png'
    params = master.pack_parameters(provider=key,
                                    file=image_url)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], TripoImageTo3D)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_tripo_multiview_to_3d(run_api):
    judgment = True
    master = LLMMaster()

    key = 'tripo_mv3d'
    image_urls = ['test-inputs/girl_front.png',
                  'test-inputs/girl_right.png',
                  'test-inputs/girl_back.png']
    params = master.pack_parameters(provider=key,
                                    files=image_urls,
                                    mode='RIGHT')
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], TripoMultiviewTo3D)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_tripo_refine_model(run_api):
    judgment = True
    master = LLMMaster()

    key = 'tripo_refine'
    task_id = '4dda7824-8375-4ab1-8b04-2ae7c891897c'
    params = master.pack_parameters(provider=key,
                                    draft_model_task_id=task_id)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], TripoRefineModel)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_tripo_aprc(run_api):
    judgment = True
    master = LLMMaster()

    key = 'tripo_aprc'
    task_id = '391b18ea-d3b9-4a02-90e5-7a4bf49bcc4a'
    params = master.pack_parameters(provider=key,
                                    original_model_task_id=task_id)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key],
                               TripoAnimationPreRigCheck)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_tripo_animation_rig(run_api):
    judgment = True
    master = LLMMaster()

    key = 'tripo_arig'
    task_id = '391b18ea-d3b9-4a02-90e5-7a4bf49bcc4a'
    params = master.pack_parameters(provider=key,
                                    original_model_task_id=task_id,
                                    out_format='glb')
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], TripoAnimationRig)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_tripo_animation_retarget(run_api):
    judgment = True
    master = LLMMaster()

    key = 'tripo_aretarget'
    task_id = 'bdd21870-6ab5-4a27-8cf3-dc2e77c808ad'
    params = master.pack_parameters(provider=key,
                                    original_model_task_id=task_id,
                                    out_format='fbx',
                                    bake_animation=True,
                                    animation='preset:walk')
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], TripoAnimationRetarget)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_tripo_stylization(run_api):
    judgment = True
    master = LLMMaster()

    key = 'tripo_stylize'
    task_id = '391b18ea-d3b9-4a02-90e5-7a4bf49bcc4a'
    params = master.pack_parameters(provider=key,
                                    original_model_task_id=task_id,
                                    style='lego')
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], TripoStylization)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_tripo_conversion(run_api):
    judgment = True
    master = LLMMaster()

    key = 'tripo_conversion'
    task_id = '391b18ea-d3b9-4a02-90e5-7a4bf49bcc4a'
    params = master.pack_parameters(provider=key,
                                    original_model_task_id=task_id,
                                    format='USDZ')
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], TripoConversion)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
