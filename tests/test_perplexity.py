import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.perplexity_models import PerplexityLLM
from llmmaster.utils import extract_llm_response


PROVIDER = "perplexity"
PROMPT = "What are the latest news in the world this month?"


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
    key = "perplexity_least"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(provider=PROVIDER, prompt=PROMPT)
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], PerplexityLLM)
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
    Test model with most parameters
    """
    judgment = True
    master = LLMMaster()
    key = "perplexity_more"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # frequency_penalty not tested
    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt=PROMPT,
        system_prompt="Return in a news narration style to read aloud.",
        model="sonar-pro",
        max_tokens=4096,
        presence_penalty=-0.2,
        search_recency_filter="month",
        temperature=0.3,
        top_p=0.6,
        top_k=75
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], PerplexityLLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_reasoning(run_api: bool, load_api_file: bool) -> None:
    """
    Test reasoning
    """
    judgment = True
    master = LLMMaster()
    key = "perplexity_reasoning"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # frequency_penalty not tested
    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt="What is the latest strategy of USA in semiconductor industry?",
        system_prompt="Show your reasoning process.",
        model="sonar-reasoning",
        max_tokens=8192,
        presence_penalty=-0.2,
        search_recency_filter="week",
        temperature=0.3,
        top_p=0.8,
        top_k=100
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], PerplexityLLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
