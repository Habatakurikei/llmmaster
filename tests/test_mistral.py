import pytest

from conftest import run_llmmaster
from conftest import verify_instance
from conftest import load_api_keys
from llmmaster import LLMMaster
from llmmaster.mistral_models import MistralLLM
from llmmaster.mistral_models import MistralFIM
from llmmaster.mistral_models import MistralAgent
from llmmaster.utils import mistral_vision_prompt
from llmmaster.utils import extract_llm_response


PROVIDER = "mistral"
PROMPT = "What are recommended sweets in France?"
IMAGE_PATH = ["./test-inputs/dragon_girl_1.png",
              "./test-inputs/elf_girl_1.png"]


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
    key = "mistral_least"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(provider=PROVIDER, prompt=PROMPT)
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], MistralLLM)
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
    key = "mistral_more"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    system_prompt = (
        "Order the output by country name in JSON, starting with the USA."
    )

    # not testing deferred parameter due to 500 error
    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt="What are the capital cities of the G20 countries?",
        model="mistral-large-latest",
        system_prompt=system_prompt,
        stop=["QED"],
        random_seed=1234567890,
        response_format={"type": "json_object"},
        frequency_penalty=0.2,
        presence_penalty=0.2,
        safe_prompt=True,
        max_tokens=4096,
        temperature=0.3,
        top_p=0.6,
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], MistralLLM)
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
    Test Mistral image to text
    """
    judgment = True
    master = LLMMaster()
    key = "mistral_i2t"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    image_prompt = mistral_vision_prompt(
        prompt="What are different things in the attached images?",
        image_path=IMAGE_PATH
    )

    entry = master.pack_parameters(
        provider=PROVIDER,
        model="pixtral-12b-2409",
        prompt=image_prompt,
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], MistralLLM)
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


def test_fim(run_api: bool, load_api_file: bool) -> None:
    """
    Test FIM (Fill-In-The-Middle) model
    """
    judgment = True
    master = LLMMaster()
    key = "mistral_fim"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider="mistral_fim",
        model="codestral-2405",
        temperature=1.5,
        stop="string",
        random_seed=0,
        prompt="def",
        suffix="return a+b",
        min_tokens=0,
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], MistralFIM)
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


# TODO: Fix agent test later


def test_agent(run_api: bool, load_api_file: bool) -> None:
    """
    Test Agent model
    """
    judgment = True
    master = LLMMaster()
    key = "mistral_agent"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(provider=PROVIDER, prompt=PROMPT)
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], MistralAgent)
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
