from llmmaster import LLMMaster

master = LLMMaster()

# Set a path of local video file
# Change "video_file" for your case
params = master.pack_parameters(
    provider='google_vtt',
    prompt='Describe attached video.',
    video_file='/home/user/sample-video.mp4')

master.summon({'video_to_text': params})

print('Start running LLMMaster...')
master.run()

print(f'Answer = {master.results["video_to_text"]}')
print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
