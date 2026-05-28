import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import save_response
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.groq_models import GroqLLM
from llmmaster.groq_models import GroqSpeechToText
from llmmaster.groq_models import GroqTextToSpeech
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
        model="openai/gpt-oss-20b",
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
        user=None,
        citation_options="disabled",
        compound_custom=None,
        disable_tool_validation=False,
        documents=None,
        reasoning_effort="low",
        search_settings=None
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
        model="meta-llama/llama-4-scout-17b-16e-instruct",
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


def test_tts(run_api: bool, load_api_file: bool) -> None:
    """
    2025-05-28 added: Test text-to-speech output
    """
    judgment = True
    master = LLMMaster()
    key = "groq_tts"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # not including model and voice to check default values
    entry = master.pack_parameters(
        provider=key,
        prompt="Hello, this is a test for text-to-speech.",
        response_format="wav",
        sample_rate=44100,
        speed=1.5,
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], GroqTextToSpeech)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            master.run()
            if isinstance(master.results[key], str):
                pytest.fail(f"Test failed with error: {master.results[key]}")
            save_response(master.results[key], key, "wav")
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment

# TODO: Add test for tool calling
