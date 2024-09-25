from llmmaster import LLMMaster

video_file = '/home/user/sample-video.mp4'
key = 'google_vtt'

master = LLMMaster()
master.summon({
    key: master.pack_parameters(
        provider=key,
        prompt='Describe attached video.',
        video_file=video_file
    )
})

print('Start running LLMMaster...')
master.run()

print(f'Response = {master.results[key]}')
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
