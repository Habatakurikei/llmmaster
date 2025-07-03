import pytest

from conftest import load_api_keys
from conftest import run_llmmaster
from conftest import verify_instance
from llmmaster import LLMMaster
from llmmaster.replica_models import ReplicaTextToSpeech


PROMPT_EN = "Hello World!"


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
    key = "replica_tts"

    if load_api_file:
        master.set_api_keys(load_api_keys())

    # not testing all parameters
    case = master.pack_parameters(
        provider=key,
        prompt=PROMPT_EN,
        extensions=["wav"],
        sample_rate=44100,
        bit_rate=128,
        global_pace=0.9,
        language_code="en",
        global_pitch=0,
        auto_pitch=False,
        global_volume=0,
        voice_preset_id="b4c1b709-941d-4501-8a73-4a36a9c169d8",
        effects_preset_id="b4c1b709-941d-4501-8a73-4a36a9c169d8",
        user_metadata={
            "session_id": "greetings"
        },
        user_tags=["greetings"]
    )
    master.summon({f"{key}": case})

    for name, instance in master.instances.items():
        judgment = verify_instance(instance, ReplicaTextToSpeech)
        if judgment is False:
            pytest.fail(f"{name} is not an expected instance.")

    if run_api:
        try:
            run_llmmaster(master)
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    assert judgment
