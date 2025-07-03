from pathlib import Path

import pytest

from conftest import execute_restapi
from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.elevenlabs_models import ElevenLabsAudioIsolation
from llmmaster.elevenlabs_models import ElevenLabsDub
from llmmaster.elevenlabs_models import ElevenLabsTextToSoundEffect
from llmmaster.elevenlabs_models import ElevenLabsTextToSpeech
from llmmaster.elevenlabs_models import ElevenLabsVoiceChanger
from llmmaster.elevenlabs_models import ElevenLabsVoiceDesign


PROMPT = "Hello world!"
AUDIO_PATH = "./test-inputs/jobs.wav"
DESCRIPTION = "./test-inputs/character_prompt_short.txt"
SCRIPT = "./test-inputs/monju_introduction.txt"


@pytest.fixture
def run_api(request) -> bool:
    return request.config.getoption("--run-api")


@pytest.fixture
def load_api_file(request) -> bool:
    return request.config.getoption("--load-api-file")


def test_tts(run_api: bool, load_api_file: bool) -> None:
    """
    Test text-to-speech
    """
    judgment = True
    master = LLMMaster()
    key = "elevenlabs_tts"
    format = "mp3"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # some parameters are not tested here
    entry = master.pack_parameters(
        provider=key,
        prompt=PROMPT,
        output_format="mp3_44100_64",
        seed=1,
        use_pvc_as_ivc=True,
        apply_text_normalization="on",
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], ElevenLabsTextToSpeech)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            execute_restapi(master, format)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_ttse(run_api: bool, load_api_file: bool) -> None:
    """
    Test text-to-sound-effect
    """
    judgment = True
    master = LLMMaster()
    key = "elevenlabs_ttse"
    format = "mp3"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=key,
        prompt="A dog barking in the distance",
        duration_seconds=3.0,
        prompt_influence=0.8
    )
    master.summon({key: entry})

    judgment = verify_instance(
        master.instances[key],
        ElevenLabsTextToSoundEffect
    )
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            execute_restapi(master, format)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_voice_design(run_api: bool, load_api_file: bool) -> None:
    """
    Test voice design
    """
    judgment = True
    master = LLMMaster()
    key = "elevenlabs_voicedesign"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=key,
        output_format="mp3_44100_32",
        text=Path(SCRIPT).read_text(encoding="utf-8"),
        voice_description=Path(DESCRIPTION).read_text(encoding="utf-8"),
        auto_generate_text=False
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], ElevenLabsVoiceDesign)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_aiso(run_api: bool, load_api_file: bool) -> None:
    """
    Test audio isolation
    """
    judgment = True
    master = LLMMaster()
    key = "elevenlabs_aiso"
    format = "mp3"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(provider=key, audio=AUDIO_PATH)
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], ElevenLabsAudioIsolation)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            execute_restapi(master, format)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_voice_changer(run_api: bool, load_api_file: bool) -> None:
    """
    Test voice changer
    """
    judgment = True
    master = LLMMaster()
    key = "elevenlabs_voicechange"
    format = "mp3"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    entry = master.pack_parameters(
        provider=key,
        audio=AUDIO_PATH,
        output_format="mp3_44100_32",
        voice_settings={
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.5,
            "use_speaker_boost": True
        },
        seed=1,
        remove_background_noise=True
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], ElevenLabsVoiceChanger)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            execute_restapi(master, format)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment


def test_dub(run_api: bool, load_api_file: bool) -> None:
    """
    Test dub
    Note: a conflict of watermark setting, this test is not working.
    """
    judgment = True
    master = LLMMaster()
    key = "elevenlabs_dub"
    format = "mp3"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # some parameters are not tested here
    entry = master.pack_parameters(
        provider=key,
        file=AUDIO_PATH,
        target_lang="ja",
        name="test-dub",
        source_lang="en",
        num_speakers=1,
        watermark=False,
        drop_background_audio=True,
        use_profanity_filter=True
    )
    master.summon({key: entry})

    judgment = verify_instance(master.instances[key], ElevenLabsDub)
    if judgment is False:
        pytest.fail(f"{key} is not an expected instance.")

    if run_api:
        try:
            execute_restapi(master, format)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
