import pytest

from conftest import run_llmmaster
from conftest import verify_instance
from conftest import load_api_keys
from llmmaster import LLMMaster
from llmmaster.inceptionlabs_models import InceptionLabsEdit
from llmmaster.inceptionlabs_models import InceptionLabsFIM
from llmmaster.inceptionlabs_models import InceptionLabsLLM
from llmmaster.utils import extract_llm_response


PROVIDER = "inceptionlabs"
PROMPT_LEAST = "Write a function to calculate the factorial of a number"
PROMPT_MORE = (
    "Write a Python function to find the longest palindrome in a string"
)
PROMPT_EDIT = (
    "<|recently_viewed_code_snippets|>\n<|/recently_viewed_code_snippets|>\n"
    "<|edit_diff_history|>\n<|/edit_diff_history|>\n<|current_file_content|>\n"
    "def greet(name):\n    print(\"hi\")\n<|/current_file_content|>\n"
    "<|code_to_edit|>\ndef greet(name):\n    print(\"hi\")<|cursor|>\n"
    "<|/code_to_edit|>"
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
        max_tokens=8192,
        temperature=0.2,
        stop=["QED"],
        diffusing=False,
        response_format={"type": "text"},
        reasoning_summary=True,
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


def test_edit(run_api: bool, load_api_file: bool) -> None:
    """
    Test Edit model
    """
    judgment = True
    master = LLMMaster()
    key = "inceptionlabs_edit"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider="inceptionlabs_edit",
        model="mercury-edit-2",
        prompt=PROMPT_EDIT,
        max_tokens=8192,
        temperature=0.7,
        top_p=0.6,
        presence_penalty=0.2
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], InceptionLabsEdit)
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
