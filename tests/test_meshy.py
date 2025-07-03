from pathlib import Path

import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.meshy_models import MeshyImageTo3D
from llmmaster.meshy_models import MeshyRemeshModel
from llmmaster.meshy_models import MeshyTextTo3D
from llmmaster.meshy_models import MeshyTextTo3DRefine
from llmmaster.meshy_models import MeshyTextToTexture


CHARACTER_PROMPT = "./test-inputs/character_prompt_short.txt"
IMAGE_PATH = "./test-inputs/monju_girl_white_tanpopo.jpg"
NEGATIVE_PROMPT = "ugly, low-resolution, upper body only"
TT3D_TEST_MODEL = ""


@pytest.fixture
def run_api(request) -> bool:
    return request.config.getoption("--run-api")


@pytest.fixture
def load_api_file(request) -> bool:
    return request.config.getoption("--load-api-file")


def test_tt3d(run_api: bool, load_api_file: bool) -> None:
    """
    Test text to 3D generation
    """
    judgment = True
    master = LLMMaster()
    key = "meshy_tt3d"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=key,
        prompt=Path(CHARACTER_PROMPT).read_text(encoding="utf-8"),
        art_style="realistic",
        seed=1,
        ai_model="meshy-4",
        topology="quad",
        target_polycount=150000,
        should_remesh=True,
        symmetry_mode="on"
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], MeshyTextTo3D)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_refine_model(run_api: bool, load_api_file: bool) -> None:
    """
    Test refine model
    """
    judgment = True
    master = LLMMaster()
    key = "meshy_tt3d_refine"
    task_id = "01953d39-e052-770e-8e6f-604e8e4e9934"
    # model made by tt3d

    if load_api_file:
        master.set_api_keys(load_api_keys())

    params = master.pack_parameters(
        provider=key,
        preview_task_id=task_id,
        enable_pbr=True
    )
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], MeshyTextTo3DRefine)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_it3d(run_api: bool, load_api_file: bool) -> None:
    """
    Test image to 3D generation
    """
    judgment = True
    master = LLMMaster()
    key = "meshy_it3d"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # omit ai_model
    entry = master.pack_parameters(
        provider=key,
        image_url=IMAGE_PATH,
        topology="triangle",
        target_polycount=300000,
        should_remesh=True,
        enable_pbr=True,
        should_texture=True,
        symmetry_mode="auto"
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], MeshyImageTo3D)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_remesh_model(run_api: bool, load_api_file: bool) -> None:
    """
    Test remesh model
    """
    judgment = True
    master = LLMMaster()
    key = "meshy_remesh"
    task_id = "01953d3c-8c44-770e-920f-555bf69bb6c0"
    # model made by tt3d and refined

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # omit ai_model
    entry = master.pack_parameters(
        provider=key,
        input_task_id=task_id,
        target_formats=["obj", "blend"],
        topology="quad",
        target_polycount=300000,
        resize_height=1.0,
        origin_at="bottom"
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], MeshyRemeshModel)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_tttx(run_api: bool, load_api_file: bool) -> None:
    """
    Test texture model
    """
    judgment = True
    master = LLMMaster()

    key = "meshy_tttx"
    model_url = TT3D_TEST_MODEL

    if load_api_file:
        master.set_api_keys(load_api_keys())

    params = master.pack_parameters(
        provider=key,
        model_url=model_url,
        object_prompt=Path(CHARACTER_PROMPT).read_text(encoding='utf-8'),
        style_prompt="outfit that fused with japanese batik style",
        enable_original_uv=True,
        enable_pbr=True,
        resolution="4096",
        negative_prompt=NEGATIVE_PROMPT,
        art_style="japanese-anime"
    )
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], MeshyTextToTexture)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
