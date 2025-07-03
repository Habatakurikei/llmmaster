import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.cerebras_models import CerebrasLLM
from llmmaster.utils import extract_llm_response


PROVIDER = "cerebras"
PROMPT = "What is the capital of the USA?"


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
    key = "cerebras_least"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(provider=PROVIDER, prompt=PROMPT)
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], CerebrasLLM)
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
    key = "cerebras_more"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    system_prompt = (
        "Order the output by country name in JSON, starting with the USA."
    )

    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt="What are the capital cities of the G20 countries?",
        model="llama3.3-70b",
        system_prompt=system_prompt,
        max_completion_tokens=4096,
        response_format={"type": "json_object"},
        seed=1234567890,
        temperature=0.3,
        top_p=0.6,
        stop=["QED"],
        user=None,
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], CerebrasLLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment

# TODO: Add test for tool calling
