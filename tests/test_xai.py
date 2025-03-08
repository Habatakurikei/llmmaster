import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response
from llmmaster.utils import xai_vision_prompt
from llmmaster.xai_models import XAILLM


PROVIDER = "xai"
PROMPT = "What is the future implementation of Grok 2 from XAI?"
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


# TODO: Add test for tool calling
