import pytest

from conftest import execute_restapi
from conftest import load_api_keys
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.voicevox_models import VoicevoxTextToSpeech


PROMPT_JA = "こんにちは。今日もいい天気ですね！"


@pytest.fixture
def run_api(request) -> bool:
    return request.config.getoption("--run-api")


@pytest.fixture
def load_api_file(request) -> bool:
    return request.config.getoption("--load-api-file")


def test_tts(run_api: bool, load_api_file: bool) -> None:
    """
    Test text-to-speech output
    """
    judgment = True
    master = LLMMaster()
    key = "voicevox_tts"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    for speaker in range(1, 3):
        case = master.pack_parameters(provider=key,
                                      prompt=PROMPT_JA,
                                      speaker=speaker)
        master.summon({f"{key}_{speaker}": case})

    for name, instance in master.instances.items():
        judgment = verify_instance(instance, VoicevoxTextToSpeech)
        if judgment is False:
            pytest.fail(f"{name} is not an expected instance.")

    if run_api:
        try:
            execute_restapi(master, format="wav")
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
