from pathlib import Path

import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.skybox_models import SkyboxPanoramaToImageVideo
from llmmaster.skybox_models import SkyboxTextToPanorama


NEGATIVE_PROMPT = "ugly, dirty, low-resolution"
PANORAMA_PROMPT = "./test-inputs/tearoom_image_prompt.txt"


@pytest.fixture
def run_api(request) -> bool:
    return request.config.getoption("--run-api")


@pytest.fixture
def load_api_file(request) -> bool:
    return request.config.getoption("--load-api-file")


def test_skybox_text_to_panorama(run_api: bool, load_api_file: bool) -> None:
    """
    Test text to panorama generation
    """
    judgment = True
    master = LLMMaster()
    key = "skybox_ttp"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    params = master.pack_parameters(
        provider=key,
        prompt=Path(PANORAMA_PROMPT).read_text(encoding="utf-8"),
        skybox_style_id=138,
        negative_text=NEGATIVE_PROMPT,
        enhance_prompt=True,
        seed=1
    )
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], SkyboxTextToPanorama)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_skybox_export(run_api: bool, load_api_file: bool) -> None:
    """
    Test panorama to image video generation
    """
    judgment = True
    master = LLMMaster()
    key = "skybox_ptiv"

    skybox_id = "15f544cd48f90e317c2f4308e6c617ff"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    params = master.pack_parameters(
        provider=key,
        skybox_id=skybox_id,
        type_id=7
    )
    master.summon({key: params})

    judgment = verify_instance(
        master.instances[key], SkyboxPanoramaToImageVideo
    )
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
