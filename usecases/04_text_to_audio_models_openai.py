from llmmaster import LLMMaster
from llmmaster.config import OPENAI_TTS_VOICE_OPTIONS

master = LLMMaster()

to_say = "Do not concentrate on the finger, or you will miss all that heavenly glory."

# try to generate all the voice patterns for a same saying
entries = []
for voice_pattern in OPENAI_TTS_VOICE_OPTIONS:
    case = {'provider': 'openai_tts',
            'prompt': to_say,
            'voice': voice_pattern,
            'response_format': 'mp3'}
    entries.append({'name': f'openai_tts_{voice_pattern}', 'params': case})

for entry in entries:
    master.summon({entry['name']: master.pack_parameters(**entry['params'])})

# You can check what parameters are set before run
print('Parameters set before run.')
for label, instance in master.instances.items():
    print(f'{label} = {instance.parameters}')

# Run LLM
print('Start running LLMMaster...')
master.run()

# Get results
print('Responses')
for name, response in master.results.items():
    save_as = f"{name}.mp3"
    with open(save_as, 'wb') as f:
        for chunk in response.iter_bytes():
            f.write(chunk)
    print(f'Saved as {save_as} for case {name}')

# Check elapsed time
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
