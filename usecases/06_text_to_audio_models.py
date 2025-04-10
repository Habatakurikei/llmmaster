import json
from pathlib import Path

from llmmaster import LLMMaster

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
speech_text = Path("speech_text.txt").read_text(encoding="utf-8")
to_say = "Hello World!"

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        "openai": master.pack_parameters(
            provider="openai_tts",
            prompt=to_say,
            voice="echo",
            speed=0.5,
            response_format="mp3"
        ),
        "elevenlabs_speech": master.pack_parameters(
            provider="elevenlabs_tts",
            prompt=to_say
        ),
        "elevenlabs_sound": master.pack_parameters(
            provider="elevenlabs_tts",
            prompt="Drinking a glass of water."
        ),
        "elevenlabs_voicedesign": master.pack_parameters(
            provider="elevenlabs_voicedesign",
            output_format="mp3_44100_32",
            text=speech_text, # min 100 words required
            voice_description="A female voice with a soft and friendly tone.",
            auto_generate_text=False
        ),
        "voicevox": master.pack_parameters(
            provider="voicevox_tts",
            prompt=to_say,
            speaker=0
        ),
        "replica": master.pack_parameters(
            provider="replica_tts",
            prompt=to_say,
        )
    }
)
master.run()

print("Response")
for instance, response in master.results.items():
    if hasattr(response, "content"):
        save_as = f"{instance}.mp3"
        with open(save_as, "wb") as f:
            f.write(response.content)
        print(f"Saved as {save_as}")
    elif isinstance(response, dict):
        save_as = f"{instance}.json"
        with open(save_as, "w", encoding="utf-8") as f:
            json.dump(response, f, indent=4, ensure_ascii=False)
        print(f"Saved as {save_as}")
    else:
        save_as = f"{instance}.txt"
        with open(save_as, "w", encoding="utf-8") as f:
            f.write(str(response))
        print(f"Saved as {save_as}")

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
