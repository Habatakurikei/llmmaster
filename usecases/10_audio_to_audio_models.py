# this function works to remove sound noise from source
import elevenlabs
from llmmaster import LLMMaster

audio_file = '/home/user/test_audio.m4a'
key = "elevenlabs_aiso"

master = LLMMaster()
master.summon({
    key: master.pack_parameters(
        provider=key,
        audio=audio_file
    )
})

print('Start running LLMMaster...')
master.run()

print('Result')
if master.results[key]:
    save_as = f"{key}.mp3"
    elevenlabs.save(master.results[key], save_as)
    print(f'Saved as {save_as}')

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
