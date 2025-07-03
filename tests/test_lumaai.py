from pathlib import Path

import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.lumaai_models import LumaAIImageToImage
from llmmaster.lumaai_models import LumaAIImageToVideo
from llmmaster.lumaai_models import LumaAITextToImage
from llmmaster.lumaai_models import LumaAITextToVideo
from llmmaster.lumaai_models import LumaAIVideoToVideo
from llmmaster.lumaai_models import LumaAIReframeImage
from llmmaster.lumaai_models import LumaAIReframeVideo


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
    key = "lumaai_tti"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # model not included
    entry = master.pack_parameters(
        provider=key,
        prompt=Path(CHARACTER_PROMPT).read_text(encoding="utf-8"),
        aspect_ratio="1:1",
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], LumaAITextToImage)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_iti(run_api: bool, load_api_file: bool) -> None:
    """
    Test image to image generation
    """
    judgment = True
    master = LLMMaster()
    key = "lumaai_iti"

    source = "https://storage.cdn-luma.com/dream_machine"
    source += "/5f843136-45ff-49af-8c97-9b99d6b12c5b"
    source += "/0fcbe733-d464-49ea-86a6-7973f7f26bf8_result.jpg"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    test_cases = [
        {
            "name": f"{key}_01",
            "params": {
                "provider": key,
                "prompt": "smiling",
                "image_ref": [
                    {
                        "url": source,
                        "weight": 0.85
                    }
                ]
            }
        },
        {
            "name": f"{key}_02",
            "params": {
                "provider": key,
                "prompt": "futuristic",
                "style_ref": [
                    {
                        "url": source,
                        "weight": 0.85
                    }
                ]
            }
        },
        {
            "name": f"{key}_03",
            "params": {
                "provider": key,
                "prompt": "a witch girl",
                "character_ref": {
                    "identity0": {
                        "images": [
                            source
                        ]
                    }
                }
            }
        },
        {
            "name": f"{key}_04",
            "params": {
                "provider": key,
                "prompt": "Change the background to a Japanese tea room",
                "modify_image_ref": {
                    "url": source,
                    "weight": 0.85
                }
            }
        }
    ]

    for case in test_cases:
        master.summon({case["name"]: master.pack_parameters(**case["params"])})

    for name, instance in master.instances.items():
        judgment = verify_instance(instance, LumaAIImageToImage)
        if judgment is False:
            pytest.fail(f"{name} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_ttv(run_api: bool, load_api_file: bool) -> None:
    """
    Test text to video generation
    """
    judgment = True
    master = LLMMaster()
    key = "lumaai_ttv"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=key,
        prompt=Path(CHARACTER_PROMPT).read_text(encoding="utf-8"),
        aspect_ratio="16:9",
        loop=True,
        resolution="720p",
        duration="9s",
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], LumaAITextToVideo)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_itv(run_api: bool, load_api_file: bool) -> None:
    """
    Test image to video generation
    """
    judgment = True
    master = LLMMaster()
    key = "lumaai_itv"

    source = "https://storage.cdn-luma.com/dream_machine/"
    source += "7fcb9a89-b765-458b-8822-2c380dc78be3/"
    source += "8a68d18d-f809-4ce8-938d-c3d2396ab9a9_result4095c688106e6a78.jpg"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=key,
        prompt="Let the witch girl dancing",
        aspect_ratio="16:9",
        loop=True,
        keyframes={
            "frame0": {
                "type": "image",
                "url": source
            }
        }
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], LumaAIImageToVideo)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_vtv(run_api: bool, load_api_file: bool) -> None:
    """
    Test video to video generation
    """
    judgment = True
    master = LLMMaster()
    key = "lumaai_vtv"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=key,
        prompt="Let the witch girl dancing",
        aspect_ratio="16:9",
        loop=True,
        keyframes={
            "frame0": {
                "type": "generation",
                "id": "221cd9d7-3aef-423e-b8d2-22799e679d3f"
            }
        }
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], LumaAIVideoToVideo)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_rfi(run_api: bool, load_api_file: bool) -> None:
    """
    Test reframe image generation
    """
    judgment = True
    master = LLMMaster()
    key = "lumaai_rfi"

    media_url = "https://storage.cdn-luma.com/dream_machine"
    media_url += "/8f638692-91ec-4f43-96f6-792328f3c1ad"
    media_url += "/848ad8da-c7f6-42ca-83b7-b9a920ba17f5_result8d4dfb4123e1c2c5.jpg"
    media_input = {"url": media_url}

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=key,
        media=media_input,
        aspect_ratio="3:4",
        grid_position_x=100,
        grid_position_y=100,
        format="png"
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], LumaAIReframeImage)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_rfv(run_api: bool, load_api_file: bool) -> None:
    """
    Test reframe video generation
    """
    judgment = True
    master = LLMMaster()
    key = "lumaai_rfv"

    media_url = "https://storage.cdn-luma.com/dream_machine"
    media_url += "/c3660737-c4d5-4a1f-b4b0-12695bce1f21"
    media_url += "/9d5a9731-b3d9-45a0-af94-0b770d99d6da_resultd5dcad2d8e7936ad.mp4"
    media_input = {"url": media_url}

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=key,
        media=media_input,
        aspect_ratio="3:4",
        grid_position_x=0,
        grid_position_y=0
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], LumaAIReframeVideo)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
