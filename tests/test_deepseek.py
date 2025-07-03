import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.deepseek_models import DeepSeekLLM
from llmmaster.utils import extract_llm_response


PROVIDER = "deepseek"
PROMPT = "What is Mermaid format?"


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
    key = "deepseek_least"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(provider=PROVIDER, prompt=PROMPT)
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], DeepSeekLLM)
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
    key = "deepseek_more"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    system_prompt = (
        "Order the output by country name in JSON, starting with the USA."
    )

    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt="What are the capital cities of the G20 countries?",
        model="deepseek-chat",
        system_prompt=system_prompt,
        response_format={"type": "json_object"},
        presence_penalty=0.2,
        frequency_penalty=0.2,
        max_tokens=4096,
        temperature=0.3,
        top_p=0.6,
        logprobs=True,
        top_logprobs=10
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], DeepSeekLLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_reasoner(run_api: bool, load_api_file: bool) -> None:
    """
    Test reasoner model
    """
    judgment = True
    master = LLMMaster()
    key = "deepseek-reasoner"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt="Where does today come before yesterday?",
        model="deepseek-reasoner"
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], DeepSeekLLM)
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


# TODO: Add test for tool calling
