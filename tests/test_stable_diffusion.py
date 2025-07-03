from pathlib import Path

import pytest

from conftest import execute_restapi
from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.stable_diffusion_models import StableDiffusionImageTo3D
from llmmaster.stable_diffusion_models import StableDiffusionImageToImage
from llmmaster.stable_diffusion_models import StableDiffusionImageToVideo
from llmmaster.stable_diffusion_models import StableDiffusionTextToImage
from llmmaster.utils import decode_base64


CHARACTER_PROMPT = "./test-inputs/character_prompt_short.txt"
NEGATIVE_PROMPT = "ugly, low-resolution, multiple people"
TEST_IMAGE = "test-inputs/test_image_rgba.png"
TEST_MASK = "test-inputs/test_mask_rgba.png"
ITV_SOURCE_IMAGE = "test-inputs/dragon_girl_1.png"
IT3D_SOURCE_IMAGE = "test-inputs/elf_girl_1.png"


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
    key = "stable_diffusion_tti"
    format = "png"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=key,
        model="ultra",
        prompt=Path(CHARACTER_PROMPT).read_text(encoding="utf-8"),
        aspect_ratio="1:1",
        negative_prompt=NEGATIVE_PROMPT,
        seed=1,
        style_preset="anime",
        output_format=format
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key],
                               StableDiffusionTextToImage)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
            decode_base64(
                master.results[key]["image"],
                f"test-outputs/{key}.{format}"
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
    key = "stable_diffusion_iti"
    format = "png"

    upscale_image = "test-inputs/frieren.png"
    upscale_prompt = "An anime elf girl."
    inpaint_prompt = "A white cat."
    outpaint_prompt = "A white cat."
    search_prompt = "An animal playing the viorin."
    select_prompt = "The wodden house to be bright color."
    light_reference = "test-inputs/light_source_1.webp"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    test_cases = [
        {
            "name": f"{key}_01",
            "params": {
                "provider": key,
                "mode": "upscale/conservative",
                "image": upscale_image,
                "prompt": upscale_prompt,
                "negative_prompt": NEGATIVE_PROMPT,
                "seed": 1,
                "output_format": format,
                "creativity": 0.2
            }
        },
        {
            "name": f"{key}_02",
            "params": {
                "provider": key,
                "mode": "upscale/creative",
                "image": upscale_image,
                "prompt": upscale_prompt,
                "negative_prompt": NEGATIVE_PROMPT,
                "seed": 1,
                "output_format": format,
                "creativity": 0.2,
                "style_preset": "anime"
            }
        },
        {
            "name": f"{key}_03",
            "params": {
                "provider": key,
                "mode": "upscale/fast",
                "image": upscale_image,
                "output_format": format
            }
        },
        {
            'name': f'{key}_04',
            'params': {
                'provider': key,
                "mode": "edit/erase",
                "image": TEST_IMAGE,
                "mask": TEST_MASK,
                "grow_mask": 10,
                "seed": 1,
                "output_format": format
            }
        },
        {
            "name": f"{key}_05",
            "params": {
                "provider": key,
                "mode": "edit/inpaint",
                "image": TEST_IMAGE,
                "prompt": inpaint_prompt,
                "negative_prompt": NEGATIVE_PROMPT,
                "mask": TEST_MASK,
                "grow_mask": 10,
                "seed": 1,
                "output_format": format,
                "style_preset": "anime"
            }
        },
        {
            "name": f"{key}_06",
            "params": {
                "provider": key,
                "mode": "edit/outpaint",
                "image": TEST_IMAGE,
                "left": 100,
                "right": 100,
                "up": 100,
                "down": 100,
                "creativity": 0.7,
                "prompt": outpaint_prompt,
                "seed": 1,
                "output_format": format,
                "style_preset": "anime"
            }
        },
        {
            "name": f"{key}_07",
            "params": {
                "provider": key,
                "mode": "edit/search-and-replace",
                "image": TEST_IMAGE,
                "prompt": inpaint_prompt,
                "search_prompt": search_prompt,
                "negative_prompt": NEGATIVE_PROMPT,
                "grow_mask": 10,
                "seed": 1,
                "output_format": format,
                "style_preset": "anime"
            }
        },
        {
            "name": f"{key}_08",
            "params": {
                "provider": key,
                "mode": "edit/search-and-recolor",
                "image": TEST_IMAGE,
                "prompt": inpaint_prompt,
                "select_prompt": select_prompt,
                "negative_prompt": NEGATIVE_PROMPT,
                "grow_mask": 10,
                "seed": 1,
                "output_format": format,
                "style_preset": "anime"
            }
        },
        {
            "name": f"{key}_09",
            "params": {
                "provider": key,
                "mode": "edit/remove-background",
                "image": TEST_IMAGE,
                "output_format": format
            }
        },
        {
            "name": f"{key}_10",
            "params": {
                "provider": key,
                "mode": "edit/replace-background-and-relight",
                "image": IT3D_SOURCE_IMAGE,
                "background_prompt": "A Japanese traditional tea room.",
                "foreground_prompt": "A woman in a kimono.",
                "negative_prompt": NEGATIVE_PROMPT,
                "preserve_original_subject": 0.8,
                "original_background_depth": 0.1,
                "keep_original_background": False,
                "light_reference": light_reference,
                "light_source_strength": 0.7,
                "seed": 1,
                "output_format": format
            }
        }
    ]

    # no model, no prompt
    for case in test_cases:
        master.summon({case["name"]: master.pack_parameters(**case["params"])})

    for name, instance in master.instances.items():
        judgment = verify_instance(instance, StableDiffusionImageToImage)
        if judgment is False:
            pytest.fail(f"{name} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
            for key in master.results:
                if "image" in master.results[key]:
                    decode_base64(
                        master.results[key]["image"],
                        f"test-outputs/{key}.{format}"
                    )
                if "result" in master.results[key]:
                    # For the following modes, not `image` but `result`
                    # upscale/creative
                    # edit/replace-background-and-relight
                    decode_base64(
                        master.results[key]["result"],
                        f"test-outputs/{key}.{format}"
                    )
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_itv(run_api: bool, load_api_file: bool) -> None:
    """
    Test image to video generation
    """
    judgment = True
    master = LLMMaster()
    key = "stable_diffusion_itv"
    format = "mp4"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # no model, no prompt
    entry = master.pack_parameters(
        provider=key,
        model="ultra",
        image=ITV_SOURCE_IMAGE,
        seed=1,
        cfg_scale=7.0,
        motion_bucket_id=125
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key],
                               StableDiffusionImageToVideo)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            execute_restapi(master, format=format)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_it3d(run_api: bool, load_api_file: bool) -> None:
    """
    Test image to 3d generation
    """
    judgment = True
    master = LLMMaster()
    key = "stable_diffusion_it3d"
    format = "glb"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # no model, no prompt
    test_cases = [
        {
            "name": "stable_diffusion_fast_3d",
            "params": {
                "provider": key,
                "mode": "stable-fast-3d",
                "image": IT3D_SOURCE_IMAGE,
                "texture_resolution": "512",
                "foreground_ratio": 0.9,
                "remesh": "quad",
                "vertex_count": 10000
            }
        },
        {
            "name": "stable_diffusion_spar_3d",
            "params": {
                "provider": key,
                "mode": "stable-point-aware-3d",
                "image": IT3D_SOURCE_IMAGE,
                "texture_resolution": "2048",
                "foreground_ratio": 2.0,
                "remesh": "quad",
                "target_type": "face",
                "target_count": 10000,
                "guidance_scale": 10,
                "seed": 1
            }
        }
    ]

    for case in test_cases:
        master.summon({case["name"]: master.pack_parameters(**case["params"])})

    for name, instance in master.instances.items():
        judgment = verify_instance(instance, StableDiffusionImageTo3D)
        if judgment is False:
            pytest.fail(f"{name} is not an expected instance.")

    if run_api:
        try:
            execute_restapi(master, format=format)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
