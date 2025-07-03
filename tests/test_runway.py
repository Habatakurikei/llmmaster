import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.runway_models import RunwayImageToVideo
from llmmaster.utils import runway_image_input


IMAGE_PATH = "./test-inputs/monju_logo.png"
IMAGE_URL = runway_image_input(IMAGE_PATH)


@pytest.fixture
def run_api(request) -> bool:
    return request.config.getoption("--run-api")


@pytest.fixture
def load_api_file(request) -> bool:
    return request.config.getoption("--load-api-file")


def test_itv(run_api: bool, load_api_file: bool) -> None:
    """
    Test image to video generation
    """
    judgment = True
    master = LLMMaster()
    key = "runway_itv"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    prompt = "Let the girl make smiling face with her eyes closed."
    images = [
        {"uri": IMAGE_URL, "position": "first"},
        {"uri": IMAGE_URL, "position": "last"}
    ]

    entry = master.pack_parameters(
        provider=key,
        promptImage=images,
        prompt=prompt,
        seed=1,
        watermark=False,
        duration=5,
        ratio="1280:768"
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], RunwayImageToVideo)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
