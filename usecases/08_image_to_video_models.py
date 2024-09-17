from llmmaster import LLMMaster

master = LLMMaster()

# Set a path of local image file
# Change "image" for your case
entry = master.pack_parameters(
    provider='stable_diffusion_itv',
    image='/home/user/test-image.png')

master.summon({'sd_itv': entry})

print('Start running LLMMaster...')
master.run()

print('Results')
response = master.results["sd_itv"]
if isinstance(response, bytes):
    with open("sd_itv.mp4", 'wb') as f:
        f.write(response)
    print("sd_itv.mp4 saved")

print(f"Elapsed time: {master.elapsed_time} seconds")

master.dismiss()
