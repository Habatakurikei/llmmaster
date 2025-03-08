import os
import time

from .config import ANTHROPIC_KEY_NAME
from .config import CEREBRAS_KEY_NAME
from .config import CLASS
from .config import DALLE_KEY_NAME
from .config import DEEPSEEK_KEY_NAME
from .config import DEFAULT_MODEL
from .config import DUMMY_KEY_NAME
from .config import ELEVENLABS_KEY_NAME
from .config import FAL_KEY_NAME
from .config import GOOGLE_KEY_NAME
from .config import GROQ_KEY_NAME
from .config import KEY_NAME
from .config import LUMAAI_KEY_NAME
from .config import MESHY_KEY_NAME
from .config import MISTRAL_KEY_NAME
from .config import OPENAI_KEY_NAME
from .config import PERPLEXITY_KEY_NAME
from .config import PROVIDERS_NEED_DUMMY_PROMPT
from .config import RUNWAY_KEY_NAME
from .config import SAMBANOVA_KEY_NAME
from .config import SKYBOX_KEY_NAME
from .config import STABLE_DIFFUSION_KEY_NAME
from .config import SUMMON_LIMIT
from .config import TRIPO_KEY_NAME
from .config import WAIT_FOR_STARTING
from .config import XAI_KEY_NAME

from .anthropic_models import AnthropicLLM
from .cerebras_models import CerebrasLLM
from .deepseek_models import DeepSeekLLM
from .elevenlabs_models import ElevenLabsAudioIsolation
from .elevenlabs_models import ElevenLabsDub
from .elevenlabs_models import ElevenLabsTextToSoundEffect
from .elevenlabs_models import ElevenLabsTextToSpeech
from .elevenlabs_models import ElevenLabsVoiceChanger
from .elevenlabs_models import ElevenLabsVoiceDesign
from .flux1_fal_models import Flux1FalImageToImage
from .flux1_fal_models import Flux1FalTextToImage
from .google_models import GoogleLLM
from .google_models import GoogleSpeechVideoToText
from .groq_models import GroqLLM
from .groq_models import GroqSpeechToText
from .lumaai_models import LumaAIImageToImage
from .lumaai_models import LumaAIImageToVideo
from .lumaai_models import LumaAITextToImage
from .lumaai_models import LumaAITextToVideo
from .lumaai_models import LumaAIVideoToVideo
from .meshy_models import MeshyImageTo3D
from .meshy_models import MeshyRemeshModel
from .meshy_models import MeshyTextTo3D
from .meshy_models import MeshyTextTo3DRefine
from .meshy_models import MeshyTextToTexture
from .mistral_models import MistralAgent
from .mistral_models import MistralFIM
from .mistral_models import MistralLLM
from .openai_models import OpenAIImageToImage
from .openai_models import OpenAILLM
from .openai_models import OpenAISpeechToText
from .openai_models import OpenAITextToImage
from .openai_models import OpenAITextToSpeech
from .perplexity_models import PerplexityLLM
from .runway_models import RunwayImageToVideo
from .sambanova_models import SambaNovaLLM
from .skybox_models import SkyboxPanoramaToImageVideo
from .skybox_models import SkyboxTextToPanorama
from .stable_diffusion_models import StableDiffusionImageTo3D
from .stable_diffusion_models import StableDiffusionImageToImage
from .stable_diffusion_models import StableDiffusionImageToVideo
from .stable_diffusion_models import StableDiffusionTextToImage
from .tripo_models import TripoAnimationPreRigCheck
from .tripo_models import TripoAnimationRetarget
from .tripo_models import TripoAnimationRig
from .tripo_models import TripoConversion
from .tripo_models import TripoImageTo3D
from .tripo_models import TripoMultiviewTo3D
from .tripo_models import TripoRefineModel
from .tripo_models import TripoStylization
from .tripo_models import TripoTextTo3D
from .tripo_models import TripoTextureModel
from .voicevox_models import VoicevoxTextToSpeech
from .xai_models import XAILLM


ACTIVE_MODELS = {
    "anthropic": {
        CLASS: AnthropicLLM,
        KEY_NAME: ANTHROPIC_KEY_NAME,
        DEFAULT_MODEL: "claude-3-haiku-20240307"
    },
    "cerebras": {
        CLASS: CerebrasLLM,
        KEY_NAME: CEREBRAS_KEY_NAME,
        DEFAULT_MODEL: "llama3.1-8b"
    },
    "deepseek": {
        CLASS: DeepSeekLLM,
        KEY_NAME: DEEPSEEK_KEY_NAME,
        DEFAULT_MODEL: "deepseek-chat"
    },
    "elevenlabs_aiso": {
        CLASS: ElevenLabsAudioIsolation,
        KEY_NAME: ELEVENLABS_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "elevenlabs_dub": {
        CLASS: ElevenLabsDub,
        KEY_NAME: ELEVENLABS_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "elevenlabs_tts": {
        CLASS: ElevenLabsTextToSpeech,
        KEY_NAME: ELEVENLABS_KEY_NAME,
        DEFAULT_MODEL: "eleven_multilingual_v2"
    },
    "elevenlabs_ttse": {
        CLASS: ElevenLabsTextToSoundEffect,
        KEY_NAME: ELEVENLABS_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "elevenlabs_voicechange": {
        CLASS: ElevenLabsVoiceChanger,
        KEY_NAME: ELEVENLABS_KEY_NAME,
        DEFAULT_MODEL: "eleven_english_sts_v2"
    },
    "elevenlabs_voicedesign": {
        CLASS: ElevenLabsVoiceDesign,
        KEY_NAME: ELEVENLABS_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "flux1_fal_iti": {
        CLASS: Flux1FalImageToImage,
        KEY_NAME: FAL_KEY_NAME,
        DEFAULT_MODEL: "dev/image-to-image"
    },
    "flux1_fal_tti": {
        CLASS: Flux1FalTextToImage,
        KEY_NAME: FAL_KEY_NAME,
        DEFAULT_MODEL: "dev"
    },
    "google": {
        CLASS: GoogleLLM,
        KEY_NAME: GOOGLE_KEY_NAME,
        DEFAULT_MODEL: "gemini-1.5-flash"
    },
    "google_stt": {
        CLASS: GoogleSpeechVideoToText,
        KEY_NAME: GOOGLE_KEY_NAME,
        DEFAULT_MODEL: "gemini-1.5-flash"
    },
    "google_vtt": {
        CLASS: GoogleSpeechVideoToText,
        KEY_NAME: GOOGLE_KEY_NAME,
        DEFAULT_MODEL: "gemini-1.5-flash"
    },
    "groq": {
        CLASS: GroqLLM,
        KEY_NAME: GROQ_KEY_NAME,
        DEFAULT_MODEL: "llama-3.1-8b-instant"
    },
    "groq_stt": {
        CLASS: GroqSpeechToText,
        KEY_NAME: GROQ_KEY_NAME,
        DEFAULT_MODEL: "whisper-large-v3"
    },
    "lumaai_iti": {
        CLASS: LumaAIImageToImage,
        KEY_NAME: LUMAAI_KEY_NAME,
        DEFAULT_MODEL: "photon-1"
    },
    "lumaai_itv": {
        CLASS: LumaAIImageToVideo,
        KEY_NAME: LUMAAI_KEY_NAME,
        DEFAULT_MODEL: "ray-1-6"
    },
    "lumaai_tti": {
        CLASS: LumaAITextToImage,
        KEY_NAME: LUMAAI_KEY_NAME,
        DEFAULT_MODEL: "photon-1"
    },
    "lumaai_ttv": {
        CLASS: LumaAITextToVideo,
        KEY_NAME: LUMAAI_KEY_NAME,
        DEFAULT_MODEL: "ray-2"
    },
    "lumaai_vtv": {
        CLASS: LumaAIVideoToVideo,
        KEY_NAME: LUMAAI_KEY_NAME,
        DEFAULT_MODEL: "ray-1-6"
    },
    "meshy_it3d": {
        CLASS: MeshyImageTo3D,
        KEY_NAME: MESHY_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "meshy_remesh": {
        CLASS: MeshyRemeshModel,
        KEY_NAME: MESHY_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "meshy_tt3d": {
        CLASS: MeshyTextTo3D,
        KEY_NAME: MESHY_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "meshy_tt3d_refine": {
        CLASS: MeshyTextTo3DRefine,
        KEY_NAME: MESHY_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "meshy_tttx": {
        CLASS: MeshyTextToTexture,
        KEY_NAME: MESHY_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "mistral": {
        CLASS: MistralLLM,
        KEY_NAME: MISTRAL_KEY_NAME,
        DEFAULT_MODEL: "mistral-small-latest"
    },
    "mistral_agent": {
        CLASS: MistralAgent,
        KEY_NAME: MISTRAL_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "mistral_fim": {
        CLASS: MistralFIM,
        KEY_NAME: MISTRAL_KEY_NAME,
        DEFAULT_MODEL: "codestral-latest"
    },
    "openai": {
        CLASS: OpenAILLM,
        KEY_NAME: OPENAI_KEY_NAME,
        DEFAULT_MODEL: "gpt-4o-mini"
    },
    "openai_iti": {
        CLASS: OpenAIImageToImage,
        KEY_NAME: DALLE_KEY_NAME,
        DEFAULT_MODEL: "dall-e-2"
    },
    "openai_stt": {
        CLASS: OpenAISpeechToText,
        KEY_NAME: OPENAI_KEY_NAME,
        DEFAULT_MODEL: "whisper-1"
    },
    "openai_tti": {
        CLASS: OpenAITextToImage,
        KEY_NAME: DALLE_KEY_NAME,
        DEFAULT_MODEL: "dall-e-3"
    },
    "openai_tts": {
        CLASS: OpenAITextToSpeech,
        KEY_NAME: OPENAI_KEY_NAME,
        DEFAULT_MODEL: "tts-1"
    },
    "perplexity": {
        CLASS: PerplexityLLM,
        KEY_NAME: PERPLEXITY_KEY_NAME,
        DEFAULT_MODEL: "sonar"
    },
    "runway_itv": {
        CLASS: RunwayImageToVideo,
        KEY_NAME: RUNWAY_KEY_NAME,
        DEFAULT_MODEL: "gen3a_turbo"
    },
    "sambanova": {
        CLASS: SambaNovaLLM,
        KEY_NAME: SAMBANOVA_KEY_NAME,
        DEFAULT_MODEL: "Meta-Llama-3.1-8B-Instruct"
    },
    "skybox_ptiv": {
        CLASS: SkyboxPanoramaToImageVideo,
        KEY_NAME: SKYBOX_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "skybox_ttp": {
        CLASS: SkyboxTextToPanorama,
        KEY_NAME: SKYBOX_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "stable_diffusion_it3d": {
        CLASS: StableDiffusionImageTo3D,
        KEY_NAME: STABLE_DIFFUSION_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "stable_diffusion_iti": {
        CLASS: StableDiffusionImageToImage,
        KEY_NAME: STABLE_DIFFUSION_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "stable_diffusion_itv": {
        CLASS: StableDiffusionImageToVideo,
        KEY_NAME: STABLE_DIFFUSION_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "stable_diffusion_tti": {
        CLASS: StableDiffusionTextToImage,
        KEY_NAME: STABLE_DIFFUSION_KEY_NAME,
        DEFAULT_MODEL: "core"
    },
    "tripo_aprc": {
        CLASS: TripoAnimationPreRigCheck,
        KEY_NAME: TRIPO_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "tripo_aretarget": {
        CLASS: TripoAnimationRetarget,
        KEY_NAME: TRIPO_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "tripo_arig": {
        CLASS: TripoAnimationRig,
        KEY_NAME: TRIPO_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "tripo_conversion": {
        CLASS: TripoConversion,
        KEY_NAME: TRIPO_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "tripo_it3d": {
        CLASS: TripoImageTo3D,
        KEY_NAME: TRIPO_KEY_NAME,
        DEFAULT_MODEL: "v2.5-20250123"
    },
    "tripo_mv3d": {
        CLASS: TripoMultiviewTo3D,
        KEY_NAME: TRIPO_KEY_NAME,
        DEFAULT_MODEL: "v2.5-20250123"
    },
    "tripo_refine": {
        CLASS: TripoRefineModel,
        KEY_NAME: TRIPO_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "tripo_stylization": {
        CLASS: TripoStylization,
        KEY_NAME: TRIPO_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "tripo_texture": {
        CLASS: TripoTextureModel,
        KEY_NAME: TRIPO_KEY_NAME,
        DEFAULT_MODEL: "v2.5-20250123"
    },
    "tripo_tt3d": {
        CLASS: TripoTextTo3D,
        KEY_NAME: TRIPO_KEY_NAME,
        DEFAULT_MODEL: "v2.5-20250123"
    },
    "voicevox_tts": {
        CLASS: VoicevoxTextToSpeech,
        KEY_NAME: DUMMY_KEY_NAME,
        DEFAULT_MODEL: "dummy"
    },
    "xai": {
        CLASS: XAILLM,
        KEY_NAME: XAI_KEY_NAME,
        DEFAULT_MODEL: "grok-2-latest"
    },
}


class LLMMaster:
    """
    Note: prepare your API keys before calling summon().
    Either environment variables or in string from text file.
    See config.py for name defined in each provider.
    Usage:
      1. create this class instance.
         (optional) set summon_limit and wait_for_starting.
         Default of summon_limit is 100 and wait_for_starting is 1 second.
         wait_for_starting must not be shorter than 1 second.
      2. (optional) load API keys with set_api_keys() method from text file.
      3. call summon() to set a new LLM/AI entry with parameters.
         Use pack_parameters() to make parameters into dictionary.
      4. call run() to start working for each entry.
      5. access self.results to get results for each LLM/AI entry.
      6. call dismiss() to clear entries and results, then finish work.
    2024-09-03: added `api_key_pairs` for one-time use.
    """

    def __init__(
        self,
        summon_limit: int = SUMMON_LIMIT,
        wait_for_starting: float = WAIT_FOR_STARTING
    ) -> None:
        self.api_key_pairs = {}
        self.instances = {}
        self.results = {}
        self.elapsed_time = 0
        self.summon_limit = (
            summon_limit if summon_limit > 0 else SUMMON_LIMIT
        )
        self.wait_for_starting = (
            wait_for_starting if wait_for_starting > 0 else WAIT_FOR_STARTING
        )

    def summon(self, entries: dict = None) -> None:
        """
        Set LLM instance. Provide argument in dictionary format such as:
        entries = {
            "label": {
                "provider": "openai",
                "model": "gpt-4o",
                "prompt": "text",
                "max_tokens": 4096,
                "temperature": 0.7
            }
        }
        See InstanceCreator for input rules for each parameter.
        Acceptable for single entry or multiple entries at once.
        Use self.pack_parameters() for batch parameters input.
        """
        if entries is None or not isinstance(entries, dict):
            raise ValueError("No entries provided.")

        num_to_summon = len(entries)

        if num_to_summon < 1 or self.summon_limit < num_to_summon:
            msg = (
                f"LLM entries must be between 1 and {self.summon_limit} "
                f"but {num_to_summon}."
            )
            raise ValueError(msg)

        creator = InstanceCreator()

        for key, value in entries.items():
            if self.summon_limit < len(self.instances):
                msg = (
                    f"LLM entries to summon reached to limit "
                    f"{self.summon_limit} - now attempted to add "
                    f"{len(self.instances)}."
                )
                raise Exception(msg)

            if key in self.instances:
                msg = f"Duplicate label: {key}"
                raise Exception(msg)

            try:
                creator.verify(
                    label=key,
                    api_key_pairs=self.api_key_pairs,
                    **value
                )
                self.instances.update(creator.create())

            except Exception as e:
                msg = "Error occurred while verifying or creating instance."
                raise Exception(f"{msg} - {e}") from e

    def run(self) -> None:
        """
        Run all instances in parallel.
        """
        self.results = {}
        start_time = time.time()

        for instance in self.instances.values():
            time.sleep(self.wait_for_starting)
            instance.start()

        for instance in self.instances.values():
            instance.join()

        end_time = time.time()
        self.elapsed_time = round(end_time - start_time, 3)

        for label, instance in self.instances.items():
            buff = {label: instance.response}
            self.results.update(buff)

    def dismiss(self) -> None:
        self.api_key_pairs = {}
        self.instances = {}
        self.results = {}
        self.elapsed_time = 0

    def pack_parameters(self, **kwargs) -> dict:
        """
        Use this function to arrange entry parameters in dictionary format.
        """
        return kwargs

    def set_api_keys(self, source: str = '') -> None:
        """
        2024-09-03: load API keys from multiple-line text
        Format: API_KEY_NAME = "your_key" or API_KEY_NAME=your_key
        One key-pair per line.
        """
        active_api_keys = [model[KEY_NAME] for model in ACTIVE_MODELS.values()]
        lines = source.splitlines()
        for line in lines:
            buff = line.replace(" ", "").replace('"', "").replace("'", "")
            word_list = buff.split("=")
            if len(word_list) > 1 and word_list[0] in active_api_keys:
                self.api_key_pairs[word_list[0]] = word_list[1]


class InstanceCreator:
    """
    Verify entry parameters and create GenAI instance in dictionary format.
    2025-01-26: removed _is_dummy_prompt_required().
    2025-02-05: renamed from LLMInstanceCreator to InstanceCreator.
    """

    def __init__(self) -> None:
        self.label = ''
        self.parameters = {}
        self.api_key = ''
        self.verified_OK = False

    def verify(
        self,
        label: str = '',
        api_key_pairs: dict = {},
        **kwargs
    ) -> None:
        """
        Check validity of minimum parameters for single entry.

        Arguments:
        - label (required): unique identifier in string for instance
            - empty str not acceptable
        - api_key_pairs (required): dictionary for API keys
        - kwargs (required): entry parameters in dictionary:
            - provider (required): string defined in config.py
            - model: string defined in config.py, default model is available
            - prompt (basically required): string, empty str not acceptable
            - other parameters: optional, see each provider's documentation
        Steps:
          1. verify label
          2. verify provider
          3. verify model
          4. verify prompt
          5. verify api key
        """
        self.verified_OK = False
        self.parameters = kwargs

        if not label or not isinstance(label, str):
            raise Exception("No label given in input.")
        self.label = label

        if "provider" not in kwargs:
            raise Exception("No provider given in input.")
        elif kwargs["provider"] not in ACTIVE_MODELS.keys():
            msg = (
                "Provider name not given or non-supported provider given: "
                f"{kwargs['provider']}."
            )
            raise ValueError(msg)

        if "model" not in kwargs or not kwargs["model"]:
            self.parameters["model"] = (
                ACTIVE_MODELS[kwargs["provider"]][DEFAULT_MODEL]
            )

        if kwargs["provider"] not in PROVIDERS_NEED_DUMMY_PROMPT:
            if "prompt" not in kwargs or not kwargs["prompt"]:
                raise ValueError("Prompt is required and cannot be empty.")

        try:
            self.api_key = self._seek_api_key(
                api_key_pairs, ACTIVE_MODELS[kwargs["provider"]][KEY_NAME]
            )
        except Exception as e:
            raise Exception(f"Failed finding API key. {e}") from e

        self.verified_OK = True

    def create(self) -> dict:
        """
        Call only after verification confirmed passed.

        Returns: in dictionary format such as:
          - label: same as given in input
          - instance of LLM ready to run
        """
        if not self.verified_OK:
            msg = "Unable to create because not verified or no input."
            raise Exception(msg)

        try:
            to_create = ACTIVE_MODELS[self.parameters["provider"]][CLASS]
            instance = to_create(api_key=self.api_key, **self.parameters)

        except Exception as e:
            raise Exception("Failed creating LLM instance.") from e

        self.verified_OK = False

        return {self.label: instance}

    def _seek_api_key(
        self,
        api_key_pairs: dict = {},
        key_name: str = ''
    ) -> str:
        """
        2024-09-03: find API key for provider (key_name).
        First, check environment variables.
        Second, check one-time API key pairs.
        """
        value = os.getenv(key_name)
        value = value if value else api_key_pairs.get(key_name, None)
        if key_name == DUMMY_KEY_NAME:
            value = "dummy"
        elif value is None:
            msg = (
                f"{key_name} is not found in environment variables"
                " or one-time API key pairs."
            )
            raise Exception(msg)
        return value
