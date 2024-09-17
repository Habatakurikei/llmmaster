from llmmaster import LLMMaster

master = LLMMaster()

# Online images are preferred for OpenAI.
# Online images and local image paths are both supported for Google.
# Change "image_url" for your case
entries = [
    {
        'name': 'openai_itt_case',
        'params': {
            'provider': 'openai_itt',
            'model': 'gpt-4o',
            'prompt': 'Describe each image.',
            'image_url': ['https://example.com/image-1.jpg',
                          'https://example.com/image-2.jpg']
        }
    },
    {
        'name': 'google_itt_case',
        'params': {
            'provider': 'google_itt',
            'model': 'gemini-1.5-flash',
            'prompt': 'What might be differences between these pictures?',
            'image_url': ['https://example.com/image.png',
                          '/home/user/my_image.png']
        }
    }
]

for entry in entries:
    master.summon({entry['name']: master.pack_parameters(**entry['params'])})

print('Start running LLMMaster...')
master.run()

for entry, result in master.results.items():
    print(f'{entry} responded: {result}')

print(f'Elapsed time: {master.elapsed_time} seconds')

master.dismiss()
