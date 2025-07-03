import pytest

from conftest import run_llmmaster
from conftest import verify_instance
from conftest import load_api_keys
from llmmaster import LLMMaster
from llmmaster.inceptionlabs_models import InceptionLabsLLM
from llmmaster.inceptionlabs_models import InceptionLabsFIM
from llmmaster.utils import extract_llm_response


PROVIDER = "inceptionlabs"
PROMPT_LEAST = "Write a function to calculate the factorial of a number"
PROMPT_MORE = (
    "Write a Python function to find the longest palindrome in a string"
)
FIM_PROMPT = "def factorial(n):"
FIM_SUFFIX = "return result"


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
    key = "inceptionlabs_least"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(provider=PROVIDER, prompt=PROMPT_LEAST)
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], InceptionLabsLLM)
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
    key = "inceptionlabs_more"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt=PROMPT_MORE,
        model="mercury-coder-small",
        stop=["QED"],
        frequency_penalty=0.2,
        presence_penalty=0.2,
        diffusing=False,
        max_tokens=8192,
        temperature=0.0,
        top_p=0.6,
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], InceptionLabsLLM)
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
    key = "inceptionlabs_fim"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider="inceptionlabs_fim",
        model="mercury-coder-small",
        temperature=0.7,
        stop=["QED"],
        prompt=FIM_PROMPT,
        suffix=FIM_SUFFIX,
        max_tokens=8192,
        top_p=0.9,
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], InceptionLabsFIM)
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
