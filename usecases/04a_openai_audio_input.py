from pathlib import Path

from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response
from llmmaster.utils import openai_audio_prompt

key = "openai"
api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
audio_prompt = openai_audio_prompt(
    prompt="What does he want to say?",
    audio_path="./audio_input.wav"
)

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        key: master.pack_parameters(
            provider=key,
            model="gpt-4o-audio-preview",
            prompt=audio_prompt
        )
    }
)
master.run()

print(f"Response: {extract_llm_response(master.results[key])}")
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
