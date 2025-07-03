from pathlib import Path

from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
speech_file = "./audio_input.wav"

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)

entries = [
    {
        "name": "openai",
        "params": {
            "provider": "openai_stt",
            "model": "whisper-1",
            "file": speech_file,
            "mode": "transcriptions",
            "response_format": "json",
        }
    },
    {
        "name": "google",
        "params": {
            "provider": "google_stt",
            "prompt": "Make a summary of the speech.",
            "file": speech_file
        }
    },
    {
        "name": "groq",
        "params": {
            "provider": "groq_stt",
            "model": "whisper-large-v3",
            "file": speech_file,
            "mode": "transcriptions",
            "response_format": "json"
        }
    }
]

for entry in entries:
    master.summon({entry["name"]: master.pack_parameters(**entry["params"])})

master.run()

print("Results")
# extract_llm_response can be used if response_format is json (OpenAI and Groq)
for instance, response in master.results.items():
    print(f"{instance} responded: {extract_llm_response(response)}")

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
