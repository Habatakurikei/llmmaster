from pathlib import Path

import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import save_response
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.openai_models import OpenAIImageToImage
from llmmaster.openai_models import OpenAILLM
from llmmaster.openai_models import OpenAISpeechToText
from llmmaster.openai_models import OpenAITextToImage
from llmmaster.openai_models import OpenAITextToSpeech
from llmmaster.utils import decode_base64
from llmmaster.utils import extract_llm_response
from llmmaster.utils import openai_audio_prompt
from llmmaster.utils import openai_vision_prompt


PROVIDER = "openai"
PROMPT = "What is the history of humburger?"
SITE = "https://cdn-ak.f.st-hatena.com/images/fotolife/d/daichan0204/20241002"
IMAGE_PATH = [SITE+"/20241002041631.png",
              SITE+"/20241002041635.png"]
AUDIO_PATH = "./test-inputs/jobs.wav"
SPEECH_PATH = "./test-inputs/test_speech.mp3"
CHARACTER_PROMPT = "./test-inputs/character_prompt_short.txt"
TEST_IMAGE = "test-inputs/test_image_rgba.png"
TEST_MASK = "test-inputs/test_mask_rgba.png"


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
    key = "openai_least"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(provider=PROVIDER, prompt=PROMPT)
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], OpenAILLM)
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
    key = "openai_more"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    system_prompt = (
        "Order the output by country name in JSON, starting with the USA."
    )

    # not testing store, metadata, and some more parameters
    entry = master.pack_parameters(
        provider=PROVIDER,
        prompt="What are the capital cities of the G20 countries?",
        model="gpt-4o",
        system_prompt=system_prompt,
        frequency_penalty=0.2,
        logprobs=True,
        logit_bias={},
        top_logprobs=3,
        max_tokens=8192,
        modalities=["text"],
        presence_penalty=0.2,
        response_format={"type": "json_object"},
        seed=1234567890,
        service_tier="auto",
        stop=["QED"],
        temperature=0.3,
        top_p=0.6,
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], OpenAILLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_o1(run_api: bool, load_api_file: bool) -> None:
    """
    Test the reasoning model
    """
    judgment = True
    master = LLMMaster()
    key = "openai_o1"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # test reasoning_effort='high' later with o1
    entry = master.pack_parameters(
        provider=PROVIDER,
        model="o1",
        prompt="What will happen in the technological singularity?",
        reasoning_effort="high",
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], OpenAILLM)
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
    Test OpenAI image to text
    """
    judgment = True
    master = LLMMaster()
    key = "openai_i2t"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    image_prompt = openai_vision_prompt(
        prompt="What are different things in the attached images?",
        image_path=IMAGE_PATH
    )

    entry = master.pack_parameters(
        provider=PROVIDER,
        model="gpt-4o",
        prompt=image_prompt
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], OpenAILLM)
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


def test_audio_input(run_api: bool, load_api_file: bool) -> None:
    """
    Test audio input: text and audio input, then text output
    """
    judgment = True
    master = LLMMaster()
    key = "openai_audio_input"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    audio_prompt = openai_audio_prompt(
        prompt="What does he want to say?",
        audio_path=AUDIO_PATH
    )

    entry = master.pack_parameters(
        provider=PROVIDER,
        model="gpt-4o-audio-preview",
        prompt=audio_prompt
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], OpenAILLM)
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


def test_audio_output(run_api: bool, load_api_file: bool) -> None:
    """
    Test audio output: no text output
    """
    judgment = True
    master = LLMMaster()
    key = "openai_audio_output"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=PROVIDER,
        model="gpt-4o-audio-preview",
        prompt="Hi, how are you?",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], OpenAILLM)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
            # response = extract_llm_response(master.results[key])
            # print(f'Extracted response: {response}')
            decode_base64(
                master.results[key]["choices"][0]["message"]["audio"]["data"],
                save_as="./test-outputs/openai_audio_output.wav",
            )
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_tts(run_api: bool, load_api_file: bool) -> None:
    """
    Test text-to-speech output
    """
    judgment = True
    master = LLMMaster()
    key = "openai_tts"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # not including model and voice to check default values
    entry = master.pack_parameters(
        provider=key,
        prompt="Hello, this is a test for text-to-speech.",
        response_format="wav",
        speed=1.5,
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], OpenAITextToSpeech)
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


def test_transcription(run_api: bool, load_api_file: bool) -> None:
    """
    Test transcription
    """
    judgment = True
    master = LLMMaster()
    key = "openai_transcription"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider="openai_stt",
        model="whisper-1",
        file=SPEECH_PATH,
        prompt="English only.",
        response_format="verbose_json",
        temperature=0.2,
        language="en",
        timestamp_granularities=["word", "segment"],
        mode="transcriptions",
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], OpenAISpeechToText)
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
    key = "openai_translation"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider="openai_stt",
        model="whisper-1",
        file=SPEECH_PATH,
        prompt="Do not use Chinese characters.",
        response_format="text",
        temperature=0.2,
        mode="translations",
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], OpenAISpeechToText)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_tti(run_api: bool, load_api_file: bool) -> None:
    """
    Test text to image generation
    """
    judgment = True
    master = LLMMaster()
    key = "openai_tti"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider="openai_tti",
        model="dall-e-3",
        prompt=Path(CHARACTER_PROMPT).read_text(encoding="utf-8"),
        n=1,
        quality="hd",
        response_format="url",
        size="1024x1024",
        style="vivid",
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], OpenAITextToImage)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_iti_edit(run_api: bool, load_api_file: bool) -> None:
    """
    Test image to image editing
    """
    judgment = True
    master = LLMMaster()
    key = "openai_iti_edit"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider="openai_iti",
        model="dall-e-2",
        image=TEST_IMAGE,
        prompt="Add a white cat to the center of the attached image",
        mask=TEST_MASK,
        mode="edits",
        n=1,
        size="512x512",
        response_format="url",
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], OpenAIImageToImage)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_iti_variations(run_api: bool, load_api_file: bool) -> None:
    """
    Test image to image variations
    """
    judgment = True
    master = LLMMaster()
    key = "openai_iti_variations"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider="openai_iti",
        model="dall-e",
        image=TEST_IMAGE,
        mode="variations",
        n=1,
        size="512x512",
        response_format="b64_json",
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], OpenAIImageToImage)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_tti_gpt(run_api: bool, load_api_file: bool) -> None:
    """
    Test text to image generation with gpt-4o
    """
    judgment = True
    master = LLMMaster()
    key = "openai_tti"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider="openai_tti",
        model="gpt-image-1",
        prompt=Path(CHARACTER_PROMPT).read_text(encoding="utf-8"),
        background="transparent",
        moderation="auto",
        n=1,
        output_compression=100,
        output_format="png",
        quality="high",
        size="1024x1024",
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], OpenAITextToImage)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment

# TODO: tools and more tests
