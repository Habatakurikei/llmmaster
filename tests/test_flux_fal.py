from pathlib import Path

import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.flux1_fal_models import Flux1FalImageToImage
from llmmaster.flux1_fal_models import Flux1FalTextToImage
from llmmaster.utils import flux1_fal_image_input
from llmmaster.utils import flux1_fal_image_save


CHARACTER_PROMPT = "./test-inputs/character_prompt_short.txt"
ITI_SOURCE_IMAGE = "./test-inputs/monju_girl_white_tanpopo.jpg"


@pytest.fixture
def run_api(request) -> bool:
    return request.config.getoption("--run-api")


@pytest.fixture
def load_api_file(request) -> bool:
    return request.config.getoption("--load-api-file")


def test_tti(run_api: bool, load_api_file: bool) -> None:
    """
    Test text to image generation
    """
    judgment = True
    master = LLMMaster()
    key = "flux1_fal_tti"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=key,
        model="dev",
        prompt=Path(CHARACTER_PROMPT).read_text(encoding="utf-8"),
        image_size="square_hd",
        num_inference_steps=28,
        seed=1,
        guidance_scale=3.5,
        num_images=1,
        enable_safety_checker=True
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], Flux1FalTextToImage)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
            flux1_fal_image_save(
                result=master.results[key],
                save_as=f"./test-outputs/{key}"
            )
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_iti(run_api: bool, load_api_file: bool) -> None:
    """
    Test image to image generation
    """
    judgment = True
    master = LLMMaster()
    key = "flux1_fal_iti"

    prompt = "Let the girl make smiling face with her eyes closed."

    if load_api_file:
        master.set_api_keys(load_api_keys())

    test_cases = [
        {
            "name": f"{key}_01",
            "params": {
                "provider": key,
                "model": "dev/image-to-image",
                "prompt": prompt,
                "image_url": flux1_fal_image_input(ITI_SOURCE_IMAGE),
                "strength": 0.95,
                "num_inference_steps": 40,
                "seed": 1,
                "guidance_scale": 3.5,
                "num_images": 3,
                "enable_safety_checker": True
            }
        },
        {
            "name": f"{key}_02",
            "params": {
                "provider": key,
                "model": "dev/redux",
                "image_url": flux1_fal_image_input(ITI_SOURCE_IMAGE),
                "strength": 0.95,
                "num_inference_steps": 40,
                "seed": 1,
                "guidance_scale": 3.5,
                "num_images": 3,
                "enable_safety_checker": True,
                "image_size": {"width": 1024, "height": 1024}
            }
        }
    ]

    for case in test_cases:
        master.summon({case["name"]: master.pack_parameters(**case["params"])})

    for name, instance in master.instances.items():
        judgment = verify_instance(instance, Flux1FalImageToImage)
        if judgment is False:
            pytest.fail(f"{name} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
            for key in master.results:
                flux1_fal_image_save(
                    result=master.results[key],
                    save_as=f"./test-outputs/{key}"
                )
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
