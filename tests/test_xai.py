from pathlib import Path

import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response
from llmmaster.utils import xai_vision_prompt
from llmmaster.xai_models import XAILLM
from llmmaster.xai_models import XAITextToImage


PROVIDER = "xai"
PROMPT = "What is the future implementation of Grok 2 from XAI?"
CHARACTER_PROMPT = "./test-inputs/character_prompt_short.txt"

IMAGE_PATH = [
    "./test-inputs/dragon_girl_1.png",
    "./test-inputs/elf_girl_1.png",
]


@pytest.fixture
def run_api(request) -> bool:
    return request.config.getoption("--run-api")


@pytest.fixture
def load_api_file(request) -> bool:
    return request.config.getoption("--load-api-file")


def test_llm_least(run_api: bool, load_api_file: bool) -> None:
    """
    Test model with least parameters
    """
    judgment = True
    master = LLMMaster()
    key = "xai_least"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(provider=PROVIDER, prompt=PROMPT)
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], XAILLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
            response = extract_llm_response(master.results[key])
            print(f"Extracted response: {response}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_llm_more(run_api: bool, load_api_file: bool) -> None:
    """
    Test model with more parameters
    """
    judgment = True
    master = LLMMaster()
    key = "xai_more"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    system_prompt = (
        "Order the output by country name in JSON, starting with the USA."
    )

    # not testing deferred parameter due to 500 error
    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt="What are the capital cities of the G20 countries?",
        model="grok-2-latest",
        system_prompt=system_prompt,
        frequency_penalty=0.2,
        presence_penalty=0.2,
        max_tokens=4096,
        response_format={"type": "json_object"},
        seed=1234567890,
        temperature=0.3,
        top_p=0.6,
        stop=["QED"],
        logprobs=True,
        top_logprobs=6,
        logit_bias=None,
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], XAILLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_llm_reasoning(run_api: bool, load_api_file: bool) -> None:
    """
    Test model with more parameters
    """
    judgment = True
    master = LLMMaster()
    key = "xai_reasoning"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # not testing deferred parameter due to 500 error
    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt="What will happen after the second Trump presidency?",
        model="grok-3-mini-beta",
        reasoning_effort="high",
        temperature=0.3
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], XAILLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_llm_livesearch(run_api: bool, load_api_file: bool) -> None:
    """
    Test model with more parameters
    """
    judgment = True
    master = LLMMaster()
    key = "xai_livesearch"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt="Provide news about Trump administration in the last 24 hours.",
        model="grok-3-latest",
        search_parameters={
            "mode": "auto"
        }
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], XAILLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_i2t(run_api: bool, load_api_file: bool) -> None:
    """
    Test image to text
    """
    judgment = True
    master = LLMMaster()
    key = "xai_i2t"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    image_prompt = xai_vision_prompt(
        prompt="What are different things in the attached images?",
        image_path=IMAGE_PATH,
    )

    entry = master.pack_parameters(
        provider=PROVIDER,
        model="grok-2-vision-latest",
        prompt=image_prompt,
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], XAILLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_tti(run_api: bool, load_api_file: bool) -> None:
    """
    Test text to image generation
    """
    judgment = True
    master = LLMMaster()
    key = "xai_tti"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=key,
        model="grok-2-image-latest",
        prompt=Path(CHARACTER_PROMPT).read_text(encoding="utf-8"),
        n=1,
        response_format="url",
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], XAITextToImage)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


# TODO: Add test for tool calling
