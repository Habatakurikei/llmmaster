import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.groq_models import GroqLLM
from llmmaster.groq_models import GroqSpeechToText
from llmmaster.utils import extract_llm_response
from llmmaster.utils import groq_vision_prompt


PROVIDER = "groq"
PROMPT = "What is the capital of France?"
IMAGE_PATH = ["./test-inputs/frieren.png"]
SPEECH_PATH = "./test-inputs/test_speech.mp3"


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
    key = "groq_least"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(provider=PROVIDER, prompt=PROMPT)
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], GroqLLM)
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
    key = "groq_more"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    system_prompt = (
        "Order the output by country name in JSON, starting with the USA."
    )

    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt="What are the capital cities of the G20 countries?",
        model="llama-3.3-70b-versatile",
        system_prompt=system_prompt,
        frequency_penalty=0.2,
        presence_penalty=-0.2,
        max_completion_tokens=4096,
        response_format={"type": "json_object"},
        seed=1234567890,
        service_tier="on_demand",
        temperature=0.3,
        top_p=0.6,
        stop=["QED"],
        user=None
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], GroqLLM)
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
    key = "groq_i2t"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    image_prompt = groq_vision_prompt(
        prompt="Describe the image.",
        image_path=IMAGE_PATH
    )

    entry = master.pack_parameters(
        provider=PROVIDER,
        model="llama-3.2-11b-vision-preview",
        prompt=image_prompt
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], GroqLLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_transcription(run_api: bool, load_api_file: bool) -> None:
    """
    Test transcription
    """
    judgment = True
    master = LLMMaster()
    key = "groq_transcription"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider="groq_stt",
        model="whisper-large-v3",
        file=SPEECH_PATH,
        response_format="verbose_json",
        temperature=0.2,
        language="en",
        mode="transcriptions",
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], GroqSpeechToText)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_translation(run_api: bool, load_api_file: bool) -> None:
    """
    Test translation
    """
    judgment = True
    master = LLMMaster()
    key = "groq_translation"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider="groq_stt",
        model="whisper-large-v3",
        file=SPEECH_PATH,
        prompt="Do not use Chaniese characters.",
        response_format="text",
        temperature=0.2,
        mode="translations",
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], GroqSpeechToText)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


# TODO: Add test for tool calling
