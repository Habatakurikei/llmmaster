# Data type of LLMMaster.results

Brief summary of what type to be stored in LLMMaster.results for each model.

**Important Note:** since v0.6.0, results are stored as either one of the following types.

- `str`:
  1. Most of text-output models return str, which seems easiest to handle for next process in your program.
  2. In case of any error, the result will be stored as str. Print it to see problem details.
- `dict`:
  1. Native or converted object of JSON, including url of generated media and other important information. Save in text file with "w" option.
  2. `requests.models.Response`, including both text and binary data of generated media. Save media and other information separately.
- `bytes`: binary data of generated media. Follow the provider instruction to save.

Remarks:

- For general REST API calls using `requests` library, return value is `requests.models.Response`. Check `Response.status_code == 200` first if response is successful. If response includes binary output, save `Response.content` in file with "wb" option for generated media. If response contains only text,  possible to convert into dict by `Response.json()`, which seems convenient for many cases.
- For OpenAI text-to-image and image-to-image, return type is `openai.types.images_response.ImagesResponse`. This object can be converted into dict using `model_dump()`.
- For ElevenLabs models, return type is proprietary binary. Use `elevenlabs.save(object, "output.mp3")` to save output. Only mp3 format might be supported for the moment.
- For Luma Dream Machine models, return type is `LumaAI.Generation` class. This class is possible to convert to `dict` using `json.loads()`.

## Text-To-Text
- AnthropicLLM: str = response.content[0].text.strip()
- CerebrasLLM: str = response.choices[0].message.content.strip()
- GoogleLLM: str = response.text.strip()
- GroqLLM: str = response.choices[0].message.content.strip()
- MistralLLM: str = response.choices[0].message.content.strip()
- OpenAILLM: str = response.choices[0].message.content.strip()
- PerplexityLLM: str = response.choices[0].message.content.strip()

## Text-To-Image
- Flux1FalTextToImage: dict = SyncRequestHandle
- OpenAITextToImage: dict = openai.types.images_response.ImagesResponse
- StableDiffusionTextToImage: dict = requests.models.Response with binary content

## Text-To-Audio
- ElevenLabsTextToSpeech: bytes = TextToSpeechClient.convert.generator
- ElevenLabsTextToSoundEffect: bytes = TextToSpeechClient.convert.generator
- OpenAITextToSpeech: bytes = openai._legacy_response.HttpxBinaryResponseContent
- VoicevoxTextToSpeech: dict = requests.models.Response with binary content

## Image-To-Text
- GoogleImageToText: str = response.text.strip()
- OpenAIImageToText: str = response.choices[0].message.content.strip()

## Image-To-Image
- Flux1FalImageToImage: dict = SyncRequestHandle
- OpenAIImageToImage: dict = openai.types.images_response.ImagesResponse
- StableDiffusionImageToImage: dict = requests.models.Response with binary content

## Image-To-Video
- StableDiffusionImageToVideo: dict = requests.models.Response with binary content

## Audio-To-Text
- GoogleSpeechToText: str = response.text.strip()
- OpenAISpeechToText: dependent on response_format
  - str = client.audio.transcriptions
  - dict = Translation or Transcription class

## Audio-To-Audio
- ElevenLabsAudioIsolation: bytes = AudioIsolationClient.audio_isolation

## Video-To-Text
- GoogleVideoToText: str = response.text.strip()

## Meshy
- MeshyTextToTexture: dict = requests.models.Response with text content
- MeshyTextTo3D: dict = requests.models.Response with text content
- MeshyTextTo3DRefine: dict = requests.models.Response with text content
- MeshyTextToVoxel: dict = requests.models.Response with text content
- MeshyImageTo3D: dict = requests.models.Response with text content

## Tripo
- TripoTextTo3D: dict = requests.models.Response with text content
- TripoImageTo3D: dict = requests.models.Response with text content
- TripoMultiviewTo3D: dict = requests.models.Response with text content
- TripoRefineModel: dict = requests.models.Response with text content
- TripoAnimationPreRigCheck: dict = requests.models.Response with text content
- TripoAnimationRig: dict = requests.models.Response with text content
- TripoAnimationRetarget: dict = requests.models.Response with text content
- TripoStylization: dict = requests.models.Response with text content
- TripoConversion: dict = requests.models.Response with text content

## Pika
- PikaPikaPikaGeneration: dict = requests.models.Response with text content

## Luma Dream Machine
- LumaDreamMachineTextToVideo: dict = LumaAI.Generation
- LumaDreamMachineImageToVideo: dict = LumaAI.Generation
- LumaDreamMachineVideoToVideo: dict = LumaAI.Generation

## Skybox
- SkyboxTextToPanorama: dict = requests.models.Response with text content
- SkyboxPanoramaToImageVideo: dict = requests.models.Response with text content
