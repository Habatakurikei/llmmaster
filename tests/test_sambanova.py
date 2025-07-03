import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.sambanova_models import SambaNovaLLM
from llmmaster.utils import extract_llm_response
from llmmaster.utils import sambanova_vision_prompt


PROVIDER = "sambanova"
PROMPT = "What is RDU (Reconfigurable Dataflow Unit)?"
IMAGE_PATH = ["./test-inputs/frieren.png"]


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
    key = "sambanova_least"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(provider=PROVIDER, prompt=PROMPT)
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], SambaNovaLLM)
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
    key = "sambanova_more"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    system_prompt = (
        "Order the output by country name in JSON, starting with the USA."
    )

    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt="What are the capital cities of the G20 countries?",
        model="Meta-Llama-3.1-405B-Instruct",
        system_prompt=system_prompt,
        max_tokens=4096,
        temperature=0.3,
        top_p=0.6,
        top_k=50,
        stop=["QED"],
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], SambaNovaLLM)
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
    key = "sambanova"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    image_prompt = sambanova_vision_prompt(
        prompt="Describe the image.",
        image_path=IMAGE_PATH,
    )

    entry = master.pack_parameters(
        provider=PROVIDER,
        model="Llama-3.2-11B-Vision-Instruct",
        prompt=image_prompt,
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], SambaNovaLLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
