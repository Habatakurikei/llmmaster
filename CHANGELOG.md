# LLMMaster Changelog

## [Unsupported]
- Realtime API services
- Streaming output by LLM
- Multiple turns in LLM chat thread
- Anthropic Claude prompt cache

## [Unreleased]
- Image models pending to be added
  - Midjourney API through ImaginePro
  - Adobe Firefly not released for personal use
  - Ideogram not released for personal use
  - Leonardo AI
  - Recraft
- Music models pending to be added
  - Mubert for rather enterprise use
  - Suno for rather enterprise use
- Other providers/models to be added
  - Tool calling for LLMs
  - Agent in MistralAI
  - Google VertexAI
  - Rodin 3D
  - Hailuo
  - Niji Voice
  - GPT-Image-1 Edit

## [1.4.3] - 2025-07-29
### Added
- `web_search_options` can be used in `OpenAILLM`

## [1.4.2] - 2025-07-24
### Changed
- Updated `PerplexityLLM`

## [1.4.1] - 2025-07-19
### Added
- `gpt-image-1` can be used in `OpenAITextToImage`

## [1.4.0] - 2025-07-15
### Added
- `Flux1FalKontext`

## [1.3.1] - 2025-07-03
### Changed
- Replaced `setup.py` with `pyproject.toml`

## [1.3.1] - 2025-07-03
### Added
- `anthropic_pdf_prompt()` in `utils.py` for `AnthropicLLM`

## [1.3.0] - 2025-06-01
### Added
- `LumaAIReframeImage`
- `LumaAIReframeVideo`
- Live search option for `XAILLM`

## [1.2.0] - 2025-04-11
### Added
- `XAITextToImage`
- Reasoning model for `XAILLM`

## [1.1.0] - 2025-04-10
### Added
- `ReplicaTextToSpeech`

## [1.0.0] - 2025-03-08
### Changed
- Reviewed all the models to use native REST API
- Reviewed to follow PEP8 style guide
- Renamed `BaseModel` to `RootModel` to avoid pydantic class name conflict
- Python files restructured based on provider, not function-based
- Unified output of Text-To-Text models to `dict`
- Unified test style
- Renamed `LLMInstanceCreator` to `InstanceCreator`
- Simplified dummy prompt verification in `InstanceCreator` class
- Changed `SUMMON_LIMIT` to 150 from 100
### Added
- `utils.py` for commonly used functions
- `LLMBase` class as common Text-To-Text model
- `MultipartFormdataModel` for multipart/form-data payload
- `SpeechToTextBase` inherited from `MultipartFormdataModel` for Speech-To-Text models
- `DeepSeekLLM`
- `SambaNovaLLM`
- `XAILLM` (Grok)
- Image-To-Text for `AnthropicLLM`, `GroqLLM`, `MistralLLM`
- Speech-To-Text for `GroqLLM`
- Audio questioning and answering to `OpenAILLM`
- Reasoning/Thinking models in `OpenAILLM`, `AnthropicLLM` and other providers can be used
- Google Web Search to `GoogleLLM`
- 3D modeling of Stable Diffusion `StableDiffusionImageTo3D`
- Image generation to Luma AI `LumaAITextToImage`, `LumaAIImageToImage`
- Voice models to ElevenLabs `ElevenLabsVoiceDesign`, `ElevenLabsVoiceChanger` and `ElevenLabsDub`
### Removed
- `pikapikapika_models.py`
- `_is_dummy_prompt_required()` in `LLMInstanceCreator` class

## [0.8.0] - 2024-10-13
### Added
- Skybox models
  - `SkyboxTextToPanorama`
  - `SkyboxPanoramaToImageVideo` (export function)

## [0.7.0] - 2024-10-06
### Added
- Runway video models
  - `RunwayImageToVideo`

## [0.6.0] - 2024-09-27
### Added
- Tripo 3D modeling APIs
  - `TripoTextTo3D`
  - `TripoImageTo3D`
  - `TripoMultiviewTo3D`
  - `TripoRefineModel`
  - `TripoAnimationPreRigCheck`
  - `TripoAnimationRig`
  - `TripoAnimationRetarget`
  - `TripoStylization`
  - `TripoConversion`
### Changed
- Changed output type to `dict` for some models, see `RESULTSTYPE.md` for details
- Fully revised the pytest test functions
- Requirement of Python version changed to 3.10 or later, 3.9 or earlier is no longer supported

## [0.5.1] - 2024-09-20
### Added
- Flux.1 image models via fal-ai
  - `Flux1FalImageToImage`
  - `Flux1FalTextToImage`
- ElevenLabs audio models
  - `ElevenLabsTextToSoundEffect`
  - `ElevenLabsAudioIsolation`
### Changed
- Commonized functions from `BaseModel`
  - `_wait()`: waiting response from API provider
  - `_sanitize_url()`: sanitizing URL text

## [0.5.0] - 2024-09-17
### Added
- Luma Dream Machine video generation models
  - `LumaDreamMachineTextToVideo`
  - `LumaDreamMachineImageToVideo`
  - `LumaDreamMachineVideoToVideo`

## [0.4.1] - 2024-09-06
### Added
- `CerebrasLLM` class
- `MistralLLM` class

## [0.4.0] - 2024-09-04
### Added
- `self.api_key_pairs` and `set_api_keys()` added to `LLMMaster` class
- `_load_api_key()` added to `LLMInstanceCreator` class
### Changed
- Revised all the models to set API key from either `os.getenv()` or  `self.api_key_pairs`
- Changed `ACTIVE_MODELS` in llmmaster.py from list to dictionary

## [0.3.4] - 2024-08-13
### Changed
- `SUMMON_LIMIT` changed to 100 as default
- Deleted `wait_for_starting` parameter verification from `LLMMaster` class
### Added
- `summon_limit` parameter added to `LLMMaster` class

## [0.3.3] - 2024-08-12
### Added
- Text-To-Speech model class
  - `VoicevoxTextToSpeech`

## [0.3.2] - 2024-08-07
### Changed
- `WAIT_FOR_SUMMONING` changed to `WAIT_FOR_STARTING`
- For Meshy models, changed to stop polling result when status is `SUCCEEDED` or `FAILED` or `EXPIRED`

## [0.3.1] - 2024-08-04
### Changed
- For Meshy models, changed to stop polling result when status is `SUCCEEDED` or `FAILED`

## [0.3.0] - 2024-08-01
### Added
- Pika.art third-party Text-To-Video model class
  - `PikaPikaPikaGeneration`

## [0.2.3] - 2024-07-30
### Added
- `ElevenLabsTextToSpeech`

## [0.2.2] - 2024-07-29
### Added
- support Meshy 3D modeling APIs
  - `MeshyTextToTexture`
  - `MeshyTextTo3D`
  - `MeshyTextTo3DRefine`
  - `MeshyTextToVoxel`
  - `MeshyImageTo3D`

## [0.2.1] - 2024-07-28
### Changed
- return value changed to `requests.models.Response` class from `response.content` for the following models:
  - `StableDiffusionTextToImage`
  - `StableDiffusionImageToVideo`
  - `StableDiffusionImageToImage`
### Added
- `RESULTSTYPE.md` for brief description how to handle generated contents

## [0.2.0] - 2024-07-27
### Added
- Speech-To-Text model class
  - `GoogleSpeechToText`

## [0.1.7] - 2024-07-21
### Added
- Image-To-Video model class
  - `StableDiffusionImageToVideo`
### Changed
- Renamed `OpenAIAudioToText` to `OpenAISpeechToText`
- Renamed `INSTANCE_CLASSES` to `ACTIVE_MODELS` in `llmmaster.py`
- Changed `MAX_TOKENS` to `DEFAULT_TOKENS` in `config.py`
- LLMMaster no longer checks `max_tokens` and sets default if not given properly

## [0.1.6] - 2024-07-19
### Added
- Image-To-Image model classes
  - `OpenAIImageToImage`
  - `StableDiffusionImageToImage`
- `elapsed_time` attribute to `LLMMaster` class
### Changed
- adding dummpy prompt process to `LLMInstanceCreator.verify()`
- `OpenAITextToImage` returns `ImagesResponses` class, changed from plain text of image URL

## [0.1.5] - 2024-07-18
### Added
- Audio-To-Text model class
  - `OpenAIAudioToText`

## [0.1.4] - 2024-07-17
### Added
- Video-To-Text model class
  - `GoogleVideoToText`

## [0.1.3] - 2024-07-16
### Added
- Image-To-Text model classes
  - `OpenAIImageToText`
  - `GoogleImageToText`

## [0.1.2] - 2024-07-14
### Added
- Text-To-Image model classes
  - `OpenAITextToImage`
  - `StableDiffusionTextToImage`

## [0.1.1] - 2024-07-12
### Changed
- renamed package name from `llm-master` to `llmmaster` because hyphens and underscores were mixed up and made confusion
### Removed
- ver. 0.1.0 from `llm-master` and start 0.1.1 for new PyPI repository `llmmaster`

## [0.1.0] - 2024-07-10
### Added
- `BaseModel` class in `base_model.py`
- `verify()` function to `LLMInstanceCreator` class
- new folders, `llm_master` and `tests`
- test functions using pytest in folder `tests` and tested
- initial PyPI uploaded

## [0.0.4] - 2024-07-09
### Added
- Text-To_Image model
  - `OpenAITTI`
- `config.py`
- `setup.py`
### Changed
- separated files `text_to_text_models.py`, `text_to_image_models.py`

## [0.0.3] - 2024-07-09
### Changed
- `LLMInstanceCreator.create()`, simplified the process of creating LLM instances

## [0.0.2] - 2024-07-08
### Added
- `LLMInstanceCreator` class in `llm_master.py` for creating and verifying LLM instances
- `LLMMaster.pack_parameters()` method to help create entry dictionaries
- `LLMMaster.dismiss()` method to clear instances and results
- set limit to 32 for max instances
- run each thread in each 1 sec of interval due to API provider limitation
### Removed
- `LLMMaster.summon_all()` method
- `LLMMaster.split_llm_information()` method

## [0.0.1] - 2024-07-05
### Added
- uploaded the first version to GitHub
