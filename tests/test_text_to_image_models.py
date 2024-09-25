import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest

from conftest import execute_llmmaster
from conftest import execute_restapi
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.text_to_image_models import Flux1FalTextToImage
from llmmaster.text_to_image_models import OpenAITextToImage
from llmmaster.text_to_image_models import StableDiffusionTextToImage


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


def test_openai_text_to_image(run_api):
    judgment = True
    master = LLMMaster()

    key = 'openai_tti'
    params = master.pack_parameters(provider=key,
                                    model='dall-e-3',
                                    prompt=PROMPT,
                                    size='1024x1792',
                                    quality='hd',
                                    n=1)
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key], OpenAITextToImage)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_stable_diffusion_text_to_image(run_api):
    judgment = True
    master = LLMMaster()

    key = 'stable_diffusion_tti'
    format = 'png'
    params = master.pack_parameters(provider=key,
                                    model='core',
                                    prompt=PROMPT,
                                    output_format=format,
                                    aspect_ratio='1:1',
                                    negative_prompt=NEGATIVE_PROMPT,
                                    see=12345,
                                    style_preset='photographic')
    master.set_api_keys(API_KEY)
    master.summon({key: params})

    judgment = verify_instance(master.instances[key],
                               StableDiffusionTextToImage)

    if run_api:
        try:
            execute_restapi(master, format=format)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_flux1fal_text_to_image(run_api):
    judgment = True
    master = LLMMaster()

    key = 'flux1_fal_tti'
    params = master.pack_parameters(provider=key,
                                    model='fal-ai/flux/schnell',
                                    prompt=PROMPT,
                                    image_size='landscape_16_9',
                                    num_inference_steps=4,
                                    seed=0,
                                    guidance_scale=3.5,
                                    sync_mode=False,
                                    num_images=1,
                                    enable_safety_checker=True)
    # master.set_api_keys(API_KEY) is not applicable but os.getenv() only
    master.summon({key: params})
    judgment = verify_instance(master.instances[key], Flux1FalTextToImage)

    if run_api:
        try:
            execute_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
