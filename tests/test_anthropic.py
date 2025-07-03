import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.anthropic_models import AnthropicLLM
from llmmaster.utils import anthropic_vision_prompt
from llmmaster.utils import anthropic_pdf_prompt
from llmmaster.utils import extract_llm_response


PROVIDER = "anthropic"
PROMPT = "Hello, how are you?"
IMAGE_PATH = ["./test-inputs/dragon_girl_1.png",
              "./test-inputs/elf_girl_1.png"]
PDF_PATH = "./test-inputs/Manus-api-presentation-EN.pdf"


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
    key = "anthropic_least"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(provider=PROVIDER, prompt=PROMPT)
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], AnthropicLLM)
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
    key = "anthropic_more"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt="Could you tell me the story of Hamlet?",
        model="claude-3-5-sonnet-20240620",
        system_prompt="You are a good storyteller.",
        max_tokens=8192,
        temperature=0.3,
        top_p=0.6,
        top_k=75,
        metadata=None,
        stop_sequences=["QED"],
        system="Output in 150 words.",
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], AnthropicLLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_thinking(run_api: bool, load_api_file: bool) -> None:
    """
    Test thinking prompt
    """
    judgment = True
    master = LLMMaster()
    key = "anthropic_thinking"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt="What are the most 3 serious problems in the world?",
        thinking={"type": "enabled", "budget_tokens": 10000},
        model="claude-3-7-sonnet-20250219",
        max_tokens=128000
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], AnthropicLLM)
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


def test_i2t(run_api: bool, load_api_file: bool) -> None:
    """
    Test image to text
    """
    judgment = True
    master = LLMMaster()
    key = "anthropic_i2t"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    image_prompt = anthropic_vision_prompt(
        prompt="What are different things in the attached images?",
        image_path=IMAGE_PATH
    )

    entry = master.pack_parameters(provider=PROVIDER, prompt=image_prompt)
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], AnthropicLLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_pdf(run_api: bool, load_api_file: bool) -> None:
    """
    Test pdf to text
    """
    judgment = True
    master = LLMMaster()
    key = "anthropic_pdf"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    pdf_prompt = anthropic_pdf_prompt(
        prompt="Summarize information in 150 words.",
        pdf_path=PDF_PATH
    )

    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt=pdf_prompt,
        model="claude-3-5-sonnet-20241022"
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], AnthropicLLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


# tool calling

def test_websearch(run_api: bool, load_api_file: bool) -> None:
    """
    Test web search
    """
    judgment = True
    master = LLMMaster()
    key = "anthropic_websearch"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=PROVIDER,
        model="claude-3-7-sonnet-latest",
        prompt="Who is the new pope elected?",
        tools=[
            {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 5
            }
        ]
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], AnthropicLLM)
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
