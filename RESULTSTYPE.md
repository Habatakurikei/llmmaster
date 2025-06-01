# Data type of LLMMaster.results

Brief summary of what type to be stored in LLMMaster.results for each model.

## History:

- fully revised since v1.0.0.
- revised at v0.6.0.

## Remarks:

- For most models, the return value is `requests.models.Response`. Check `Response.status_code == 200` first if request is successful. If response includes binary output, save `Response.content` in file with "wb" option for generated media. If response contains only text, possible to convert into dict by `Response.json()`, which seems convenient for many cases. Follow the general rules of `requests` library for handling the response.
- For Text-To-Text (LLM) models: dict = requests.models.Response with text content. Extract message by calling `llmmaster.utils.extract_llm_response(response)` or utilize a full response object. Changed from v1.0.0.
- There are also supporting functions to save binary data returned from some models. See each use case or `llmmaster.utils.py` for technical details.

## Result Type of Each Model:

### Anthropic
- AnthropicLLM (text-to-text): requests.models.Response with text content.
- AnthropicLLM (vision input): requests.models.Response with text content.

### Cerebras
- CerebrasLLM (text-to-text): requests.models.Response with text content.

### DeepSeek
- DeepSeekLLM (text-to-text): requests.models.Response with text content.

### ElevenLabs
- ElevenLabsTextToSpeech: requests.models.Response with binary content.
- ElevenLabsTextToSoundEffect: requests.models.Response with binary content.
- ElevenLabsVoiceDesign: requests.models.Response with base64 encoded audio.
- ElevenLabsAudioIsolation: requests.models.Response with binary content.
- ElevenLabsVoiceChanger: requests.models.Response with binary content.
- ElevenLabsDub: requests.models.Response with binary content.

### Flux.1 via Fal
- Flux1FalTextToImage: requests.models.Response with base64 content.
- Flux1FalImageToImage: requests.models.Response with base64 content.

### Google
- GoogleLLM (text-to-text): requests.models.Response with text content.
- GoogleLLM (vision input): requests.models.Response with text content.
- GoogleSpeechVideoToText (speech-to-text): requests.models.Response with text content.
- GoogleSpeechVideoToText (video-to-text): requests.models.Response with text content.

### Groq
- GroqLLM (text-to-text): requests.models.Response with text content.
- GroqLLM (vision input): requests.models.Response with text content.
- GroqSpeechToText:
    - requests.models.Response with text content if `response_format` is `json` or `verbose_json`
    - str = Response.text if `response_format` is `text`

### Luma Dream Machine
- LumaAITextToImage: requests.models.Response with URL of generation
- LumaAIImageToImage: requests.models.Response with URL of generation
- LumaAITextToVideo: requests.models.Response with URL of generation
- LumaAIImageToVideo: requests.models.Response with URL of generation
- LumaAIVideoToVideo: requests.models.Response with URL of generation
- LumaAIReframeImage: requests.models.Response with URL of generation
- LumaAIReframeVideo: requests.models.Response with URL of generation

### Meshy
- MeshyTextTo3D: requests.models.Response with URL of 3D model
- MeshyTextTo3DRefine: requests.models.Response with URL of 3D model
- MeshyImageTo3D: requests.models.Response with URL of 3D model
- MeshyRemeshModel: requests.models.Response with URL of 3D model
- MeshyTextToTexture: requests.models.Response with URL of 3D model

### MistralAI
- MistralLLM (text-to-text): requests.models.Response with text content.
- MistralLLM (vision input): requests.models.Response with text content.
- MistralFIM (fill-in-the-middle): requests.models.Response with text content.
- MistralAgent: pending for implementation.

### OpenAI
- OpenAILLM (text-to-text): requests.models.Response with text content.
- OpenAILLM (vision input): requests.models.Response with text content.
- OpenAILLM (audio output): requests.models.Response with base64 content `dict['choices'][0]['message']['audio']['data']`.
- OpenAITextToImage:
    - requests.models.Response with URL of generated image if `response_format` is `url`
    - requests.models.Response with base64 content if `response_format` is `b64_json`
- OpenAITextToSpeech: ~~bytes = openai._legacy_response.HttpxBinaryResponseContent~~ requests.models.Response with binary content
- OpenAIImageToImage:
    - requests.models.Response with URL of generated image if `response_format` is `url`
    - requests.models.Response with base64 content if `response_format` is `b64_json`
- OpenAISpeechToText:
    - dict converted from requests.models.Response with text content if `response_format` is `json` or `verbose_json`
    - str = Response.text if `response_format` is `text`

### Perplexity
- PerplexityLLM: requests.models.Response with text content.

### Pika
- ~~PikaPikaPikaGeneration: dict = requests.models.Response with text content~~ DEPRECATED from v1.0.0

### Replica
- ReplicaTextToSpeech: requests.models.Response with URL of generated speech

### Runway
- RunwayImageToVideo: requests.models.Response with URL of generated video

### SambaNova
- SambaNovaLLM (text-to-text): requests.models.Response with text content.
- SambaNovaLLM (vision input): requests.models.Response with text content.

### Skybox
- SkyboxTextToPanorama: requests.models.Response with text content
- SkyboxPanoramaToImageVideo: requests.models.Response with text content

### Stable Diffusion
- StableDiffusionTextToImage: requests.models.Response with base64 encoded image
- StableDiffusionImageToImage: requests.models.Response with base64 encoded image
- StableDiffusionImageToVideo: requests.models.Response with binary content
- StableDiffusionImageTo3D: requests.models.Response with binary content

### Tripo
- TripoTextTo3D: requests.models.Response with URL of 3D model
- TripoImageTo3D: requests.models.Response with URL of 3D model
- TripoMultiviewTo3D: requests.models.Response with URL of 3D model
- TripoTextureModel: requests.models.Response with URL of 3D model
- TripoRefineModel: requests.models.Response with URL of 3D model
- TripoAnimationPreRigCheck: requests.models.Response with text content
- TripoAnimationRig: requests.models.Response with URL of 3D model
- TripoAnimationRetarget: requests.models.Response with URL of 3D model
- TripoStylization: requests.models.Response with URL of 3D model
- TripoConversion: requests.models.Response with URL of 3D model

### VoiceVox
- VoicevoxTextToSpeech: requests.models.Response with binary content

### XAI
- XAILLM (text-to-text): requests.models.Response with text content.
- XAILLM (vision input): requests.models.Response with text content.
- XAITextToImage: requests.models.Response with base64 encoded image
