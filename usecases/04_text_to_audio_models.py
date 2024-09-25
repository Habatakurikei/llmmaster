import elevenlabs
from llmmaster import LLMMaster

to_say = "Hello World!"

master = LLMMaster()

# Configure instances
master.summon({
    "openai": master.pack_parameters(
        provider='openai_tts',
        prompt=to_say,
        voice='echo',
        speed=0.5,
        response_format='mp3'
    ),
    "elevenlabs_speech": master.pack_parameters(
        provider='elevenlabs_tts',
        prompt=to_say
    ),
    "elevenlabs_sound": master.pack_parameters(
        provider='elevenlabs_ttse',
        prompt='Drinking a glass of water.'
    ),
    "voicevox": master.pack_parameters(
        provider='voicevox_tts',
        prompt=to_say,
        speaker=0
    )
})

# You can check what parameters are set before run
print('Parameters set before run.')
for label, instance in master.instances.items():
    print(f'{label} = {instance.parameters}')

# Run master
print('Start running LLMMaster...')
master.run()

# Get results
print('Responses')

response = master.results['openai']
if response:
    save_as = "openai.mp3"
    with open(save_as, 'wb') as f:
        for chunk in response.iter_bytes():
            f.write(chunk)
    print(f'Saved as {save_as}')

if master.results['elevenlabs_speech']:
    save_as = "elevenlabs_speech.mp3"
    elevenlabs.save(master.results['elevenlabs_speech'], save_as)
    print(f'Saved as {save_as}')

if master.results['elevenlabs_sound']:
    save_as = "elevenlabs_sound.mp3"
    elevenlabs.save(master.results['elevenlabs_sound'], save_as)
    print(f'Saved as {save_as}')

response = master.results['voicevox']
if response.content:
    save_as = "voicevox.wav"
    with open(save_as, 'wb') as f:
        f.write(response.content)
    print(f'Saved as {save_as}')

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
