from pathlib import Path

import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.tripo_models import TripoAnimationPreRigCheck
from llmmaster.tripo_models import TripoAnimationRetarget
from llmmaster.tripo_models import TripoAnimationRig
from llmmaster.tripo_models import TripoConversion
from llmmaster.tripo_models import TripoImageTo3D
from llmmaster.tripo_models import TripoMultiviewTo3D
from llmmaster.tripo_models import TripoRefineModel
from llmmaster.tripo_models import TripoStylization
from llmmaster.tripo_models import TripoTextTo3D
from llmmaster.tripo_models import TripoTextureModel


CHARACTER_PROMPT = "./test-inputs/character_prompt_short.txt"
IMAGE_PATH = "./test-inputs/monju_girl_white_tanpopo.jpg"
# IMAGE_PATH = "./test-inputs/elf_girl_1.png"


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
    key = "tripo_tt3d"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=key,
        model="v2.0-20240919",
        prompt=Path(CHARACTER_PROMPT).read_text(encoding="utf-8"),
        negative_prompt="ugly, low-quality, upper body only",
        image_seed=1,
        model_seed=1,
        face_limit=10000,
        texture=True,
        pbr=True,
        texture_seed=1,
        texture_quality="detailed",
        auto_size=False,
        style="person:person2cartoon",
        quad=True
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], TripoTextTo3D)
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
    key = "tripo_it3d"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # omit model and style
    entry = master.pack_parameters(
        provider=key,
        model="v2.0-20240919",
        file=IMAGE_PATH,
        model_seed=1,
        face_limit=10000,
        texture=True,
        pbr=True,
        texture_seed=1,
        texture_quality="detailed",
        auto_size=False,
        quad=True,
        texture_alignment="geometry",
        orientation="align_image"
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], TripoImageTo3D)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_mvt3d(run_api: bool, load_api_file: bool) -> None:
    """
    Test multiview to 3D generation
    """
    judgment = True
    master = LLMMaster()
    key = "tripo_mv3d"
    images = [
        "test-inputs/girl_front.png",
        "test-inputs/girl_left.png",
        "test-inputs/girl_back.png",
        "test-inputs/girl_right.png"
    ]

    if load_api_file:
        master.set_api_keys(load_api_keys())

    params = master.pack_parameters(
        provider=key,
        files=images,
        face_limit=10000,
        texture=True,
        pbr=True,
        texture_seed=1,
        texture_alignment="geometry",
        texture_quality="detailed",
        auto_size=False,
        orientation="align_image",
        quad=False
    )
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], TripoMultiviewTo3D)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_texture_model(run_api: bool, load_api_file: bool) -> None:
    """
    Test texture model
    """
    judgment = True
    master = LLMMaster()

    key = "tripo_texture"
    task_id = "664adeae-01e9-4ccd-ae5d-00adb811bc27"
    # model made by multiview v2.5-20250123

    if load_api_file:
        master.set_api_keys(load_api_keys())

    params = master.pack_parameters(
        provider=key, original_model_task_id=task_id
    )
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], TripoTextureModel)
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
    key = "tripo_refine"
    task_id = "391b18ea-d3b9-4a02-90e5-7a4bf49bcc4a"
    # model made by tt3d older than v2.0-20240919

    if load_api_file:
        master.set_api_keys(load_api_keys())

    params = master.pack_parameters(provider=key, draft_model_task_id=task_id)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], TripoRefineModel)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_aprc(run_api: bool, load_api_file: bool) -> None:
    """
    Test animation pre-rig check
    """
    judgment = True
    master = LLMMaster()
    key = "tripo_aprc"
    task_id = "f90c1f18-3c55-4e9c-b3f2-1e84ba270f8b"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    params = master.pack_parameters(
        provider=key, original_model_task_id=task_id
    )
    master.summon({key: params})

    judgment = verify_instance(
        master.instances[key], TripoAnimationPreRigCheck
    )
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_arig(run_api: bool, load_api_file: bool) -> None:
    """
    Test animation rig
    """
    judgment = True
    master = LLMMaster()
    key = "tripo_arig"
    task_id = "f90c1f18-3c55-4e9c-b3f2-1e84ba270f8b"
    # model of tt3d kimono girl

    if load_api_file:
        master.set_api_keys(load_api_keys())

    params = master.pack_parameters(
        provider=key,
        original_model_task_id=task_id,
        out_format="glb"
    )
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], TripoAnimationRig)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_aretarget(run_api: bool, load_api_file: bool) -> None:
    """
    Test animation retarget
    """
    judgment = True
    master = LLMMaster()
    key = "tripo_aretarget"
    task_id = "98481d31-e63a-4e8a-9143-fd0db8ec2f74"
    # model of rigged kimono girl

    if load_api_file:
        master.set_api_keys(load_api_keys())

    params = master.pack_parameters(
        provider=key,
        original_model_task_id=task_id,
        out_format="fbx",
        bake_animation=True,
        animation="preset:jump"
    )
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], TripoAnimationRetarget)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_stylization(run_api: bool, load_api_file: bool) -> None:
    """
    Test stylization
    """
    judgment = True
    master = LLMMaster()
    key = "tripo_stylization"
    task_id = "1ea91c2b-3dcd-4985-92f9-b52460d8f311"
    # model of tt3d kimono girl

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # failed to make minecraft with block_size=40
    params = master.pack_parameters(
        provider=key,
        original_model_task_id=task_id,
        style="lego"
    )
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], TripoStylization)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_conversion(run_api: bool, load_api_file: bool) -> None:
    """
    Test conversion
    """
    judgment = True
    master = LLMMaster()
    key = "tripo_conversion"
    task_id = "1ea91c2b-3dcd-4985-92f9-b52460d8f311"
    # model of tt3d kimono girl

    if load_api_file:
        master.set_api_keys(load_api_keys())

    params = master.pack_parameters(
        provider=key,
        original_model_task_id=task_id,
        format="OBJ",
        quad=True,
        force_symmetry=True,
        face_limit=10000,
        flatten_bottom=True,
        flatten_bottom_threshold=0.01,
        texture_size=4096,
        texture_format="png",
        pivot_to_center_bottom=True,
        scale_factor=1
    )
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], TripoConversion)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
