import elevenlabs
from llmmaster import LLMMaster

master = LLMMaster()

to_say = "Do not concentrate on the finger, or you will miss all that heavenly glory."

test_case = master.pack_parameters(provider='elevenlabs_tts', prompt=to_say)

master.summon({'elevenlabs_tts': test_case})

# Run LLM
print('Start running LLMMaster...')
master.run()

# Get results
print('Responses')
if master.results['elevenlabs_tts']:
    save_as = f"elevenlabs_tts.mp3"
    elevenlabs.save(master.results['elevenlabs_tts'], save_as)
    print(f'Saved as {save_as} for case {name}')

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
