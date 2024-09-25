from llmmaster import LLMMaster

master = LLMMaster()

speech_file = '/home/user/sample-speech.mp3'

entries = [
    {
        'name': 'openai_stt_1',
        'params': {
            'provider': 'openai_stt',
            'mode': 'translations',
            'file': speech_file,
            'response_format': 'json',
            'temperature': 0.0
        }
    },
    {
        'name': 'openai_stt_2',
        'params': {
            'provider': 'openai_stt',
            'mode': 'transcriptions',
            'file': speech_file,
            'response_format': 'text'
        }
    },
    {
        'name': 'openai_stt_3',
        'params': {
            'provider': 'openai_stt',
            'mode': 'transcriptions',
            'file': speech_file,
            'response_format': 'verbose_json'
        }
    },
    {
        'name': 'google_stt',
        'params': {
            'provider': 'google_stt',
            'prompt': 'What does the speaker imply?',
            'audio_file': speech_file
        }
    }
]

for entry in entries:
    master.summon({entry['name']: master.pack_parameters(**entry['params'])})

print('Start running LLMMaster...')
master.run()

# Different type of response given by different
# `response_format`, `transcriptions` or `translations` mode
# Handle with care for output
print('Results')
for name, response in master.results.items():
    print(f'{name}: {response}')

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
