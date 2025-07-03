from pathlib import Path

from llmmaster import LLMMaster
from llmmaster.config import ELEVENLABS_DEFAULT_VOICE_ID

api_key_pairs = Path("api_key_pairs.txt").read_text(encoding="utf-8")
audio_file = "./audio_input.wav"

print("Start generation...")
master = LLMMaster()
master.set_api_keys(api_key_pairs)
master.summon(
    {
        "elevenlabs_aiso": master.pack_parameters(
            provider="elevenlabs_aiso",
            audio=audio_file
        ),
        "elevenlabs_voicechange": master.pack_parameters(
            provider="elevenlabs_voicechange",
            voice_id=ELEVENLABS_DEFAULT_VOICE_ID,
            audio=audio_file,
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
    }
)
master.run()

print("Response")
for instance, response in master.results.items():
    if response:
        save_as = f"{instance}.mp3"
        with open(save_as, "wb") as f:
            f.write(response.content)
        print(f"Saved as {save_as}")

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
