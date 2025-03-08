from pathlib import Path

from llmmaster import LLMMaster
from llmmaster.utils import decode_base64

key = "openai"
api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        key: master.pack_parameters(
            provider=key,
            model="gpt-4o-audio-preview",
            prompt="Hi, how are you?",
            modalities=["text", "audio"],
            audio={"voice": "alloy", "format": "wav"},
        )
    }
)
master.run()

print("Save output audio.")
decode_base64(
    master.results[key]["choices"][0]["message"]["audio"]["data"],
    save_as="./audio_output.wav",
)

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
