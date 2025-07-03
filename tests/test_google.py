import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.google_models import GoogleLLM
from llmmaster.google_models import GoogleSpeechVideoToText
from llmmaster.utils import extract_llm_response
from llmmaster.utils import google_vision_prompt


PROVIDER = "google"
IMAGE_PATH = ["./test-inputs/dragon_girl_1.png",
              "./test-inputs/elf_girl_1.png"]
SPEECH_PATH = "./test-inputs/test_speech.mp3"
VIDEO_PATH = "./test-inputs/test_video_org.mp4"


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
    key = "google_least"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt="Who are you?"
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], GoogleLLM)
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
    key = "google_more"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    system_prompt = (
        "Order the output by country name in JSON, starting with the USA."
    )

    # some parameters are not tested
    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt="What are the capital cities of the G20 countries?",
        model="gemini-2.0-flash",
        system_prompt=system_prompt,
        stopSequences=["QED"],
        responseMimeType="application/json",
        responseModalities=["TEXT"],
        candidateCount=1,
        maxOutputTokens=8000,
        temperature=0.5,
        topP=0.95,
        topK=40,
        seed=1,
        presencePenalty=0.2,
        frequencyPenalty=0.2,
        enableEnhancedCivicAnswers=True
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], GoogleLLM)
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


def test_llm_reasoning(run_api: bool, load_api_file: bool) -> None:
    """
    Test reasoning model
    """
    judgment = True
    master = LLMMaster()
    key = "google_reasoning"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider="google",
        model="gemini-2.5-pro-preview-05-06",
        prompt="Is the basic income a good idea?",
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], GoogleLLM)
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


def test_llm_search(run_api: bool, load_api_file: bool) -> None:
    """
    Test web search model
    """
    judgment = True
    master = LLMMaster()
    key = "google_search"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=PROVIDER,
        model="gemini-1.5-flash",
        prompt="What was happening in the world last week?",
        dynamic_threshold=0.1
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], GoogleLLM)
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
    Test image to text model
    """
    judgment = True
    master = LLMMaster()
    key = "google_i2t"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    image_prompt = google_vision_prompt(
        prompt="What are different characters in the image?",
        image_path=IMAGE_PATH
    )

    entry = master.pack_parameters(
        provider=PROVIDER,
        model="gemini-2.0-flash",
        prompt=image_prompt
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], GoogleLLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
            extracted_response = extract_llm_response(master.results[key])
            print(f"Extracted response: {extracted_response}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_stt(run_api: bool, load_api_file: bool) -> None:
    """
    Test speech to text model
    """
    judgment = True
    master = LLMMaster()
    key = "google_stt"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=key,
        model="gemini-1.5-flash",
        prompt="What is the attached audio about?",
        file=SPEECH_PATH
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], GoogleSpeechVideoToText)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
            extracted_response = extract_llm_response(master.results[key])
            print(f"Extracted response: {extracted_response}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_vtt(run_api: bool, load_api_file: bool) -> None:
    """
    Test video to text model
    """
    judgment = True
    master = LLMMaster()
    key = "google_vtt"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=key,
        model="gemini-1.5-flash",
        prompt="What is the attached video about?",
        file=VIDEO_PATH
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], GoogleSpeechVideoToText)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
            extracted_response = extract_llm_response(master.results[key])
            print(f"Extracted response: {extracted_response}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
