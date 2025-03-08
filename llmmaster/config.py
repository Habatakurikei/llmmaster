# Active model settings
CLASS = "class"
KEY_NAME = "key_name"
DEFAULT_MODEL = "default_model"

# API key settings
ADOBE_FIREFLY_CLIENT_ID_NAME = "ADOBE_FIREFLY_CLIENT_ID"
ADOBE_FIREFLY_CLIENT_SECRET_NAME = "ADOBE_FIREFLY_CLIENT_SECRET"
ANTHROPIC_KEY_NAME = "ANTHROPIC_API_KEY"
CEREBRAS_KEY_NAME = "CEREBRAS_API_KEY"
DALLE_KEY_NAME = "DALLE_API_KEY"
DEEPSEEK_KEY_NAME = "DEEPSEEK_API_KEY"
DUMMY_KEY_NAME = "DUMMY_API_KEY"
ELEVENLABS_KEY_NAME = "ELEVENLABS_API_KEY"
FAL_KEY_NAME = "FAL_KEY"
GOOGLE_KEY_NAME = "GOOGLE_API_KEY"
GROQ_KEY_NAME = "GROQ_API_KEY"
LUMAAI_KEY_NAME = "LUMAAI_API_KEY"
MESHY_KEY_NAME = "MESHY_API_KEY"
MISTRAL_KEY_NAME = "MISTRAL_API_KEY"
OPENAI_KEY_NAME = "OPENAI_API_KEY"
PERPLEXITY_KEY_NAME = "PERPLEXITY_API_KEY"
RUNWAY_KEY_NAME = "RUNWAY_API_KEY"
SAMBANOVA_KEY_NAME = "SAMBANOVA_API_KEY"
SKYBOX_KEY_NAME = "SKYBOX_API_KEY"
STABLE_DIFFUSION_KEY_NAME = "STABLE_DIFFUSION_API_KEY"
TRIPO_KEY_NAME = "TRIPO_API_KEY"
XAI_KEY_NAME = "XAI_API_KEY"

# REST API settings
REQUEST_ACCEPTED = 202
REQUEST_CREATED = 201
REQUEST_OK = 200
POSITIVE_RESPONSE_CODES = [REQUEST_ACCEPTED, REQUEST_CREATED, REQUEST_OK]

MULTIPART_BOUNDARY = "LLMMasterMultiPartBoundary"
X_API_KEY = "x-api-key"
XI_API_KEY = "xi-api-key"

# Summon default settings
SUMMON_LIMIT = 150
WAIT_FOR_STARTING = 1.0

# Text-To-Text settings
# Note:
# top_p is common for all models but top_k is only for anthropic and google.
# Not available for openai, groq and perplexity (OpenAI-based models).
# 2025-01-21: removed typical model lists. See official documentation.
DEFAULT_TOKENS = 4096
TEMPERATURE = 0.7
TOP_P = 0.9
TOP_K = 30

# Adobe Firefly
ADOBE_FIREFLY_TOKEN_PRE_EP = "https://ims-na1.adobelogin.com/ims/token/v3?"
ADOBE_FIREFLY_TOKEN_POST_EP = (
    "&grant_type=client_credentials&scope=openid,AdobeID,firefly_enterprise,"
    "firefly_api,ff_apis"
)
ADOBE_FIREFLY_TTI_EP_BASE = "https://firefly-api.adobe.io/"
ADOBE_FIREFLY_TTI_EP_GENERATE = "/images/generate"

ADOBE_FIREFLY_CONTENT_CLASS = ["art", "photo"]
ADOBE_FIREFLY_TTI_MODELS = ["v3", "v2"]
ADOBE_FIREFLY_TTI_SIZE_LIST = [
    {"width": 2048, "height": 2048}, {"width": 2304, "height": 1792},
    {"width": 1792, "height": 2304}, {"width": 2688, "height": 1536},
    {"width": 1344, "height": 768}, {"width": 1152, "height": 896},
    {"width": 896, "height": 1152}, {"width": 1024, "height": 1024}
]
ADOBE_FIREFLY_DEFAULT_N = 1
ADOBE_FIREFLY_MAX_N = 4

# Anthropic
ANTHROPIC_TTT_EP = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION_HEADER = "2023-06-01"

# Cerebras
CEREBRAS_TTT_EP = "https://api.cerebras.ai/v1/chat/completions"

# DeepSeek
DEEPSEEK_TTT_EP = "https://api.deepseek.com/chat/completions"

# ElevenLabs
ELEVENLABS_BASE_EP = "https://api.elevenlabs.io"
ELEVENLABS_TTS_EP = "/v1/text-to-speech"
ELEVENLABS_TTSE_EP = "/v1/sound-generation"
ELEVENLABS_TTVOICE_EP = "/v1/text-to-voice/create-previews"
ELEVENLABS_AISO_EP = "/v1/audio-isolation"
ELEVENLABS_VOICECHANGE_EP = "/v1/speech-to-speech"
ELEVENLABS_DUB_EP = "/v1/dubbing"

ELEVENLABS_MORIOKI_VOICE_ID = "8EkOjt4xTPGMclNlh1pk"
ELEVENLABS_DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

# Fal Common
FAL_BASE_EP = "https://queue.fal.run"
FAL_RESULT_EP = "/requests/{request_id}/status"
FAL_STATUS_IN_PROGRESS = ["IN_QUEUE", "IN_PROGRESS"]
WAIT_FOR_FAL_RESULT = 5.0

# Flux1 Fal
FLUX1_FAL_TTI_EP = "/fal-ai/flux"
FLUX1_FAL_ITI_EP = "/fal-ai/flux"
WAIT_FOR_FLUX1_FAL_RESULT = 3.0

# Google
GOOGLE_GEMINI_BASE_EP = "https://generativelanguage.googleapis.com"
GOOGLE_GEMINI_TTT_EP = "/v1beta/models/{model}:generateContent"
GOOGLE_GEMINI_UPLOAD_EP = "/upload/v1beta/files"
GOOGLE_GEMINI_DELETE_EP = "/v1beta"
GOOGLE_GEMINI_FILE_LIST_EP = "/v1beta/files"
WAIT_FOR_GOOGLE_VTT_RESULT = 5.0

# Groq
GROQ_BASE_EP = 'https://api.groq.com/openai'
GROQ_TTT_EP = "/v1/chat/completions"
GROQ_TRANSCRIPTION_EP = "/v1/audio/transcriptions"
GROQ_TRANSLATION_EP = "/v1/audio/translations"

# Luma Dream Machine
LUMAAI_BASE_EP = "https://api.lumalabs.ai/dream-machine"
LUMAAI_RESULT_EP = "/v1/generations/{id}"
LUMAAI_TTI_EP = "/v1/generations/image"
LUMAAI_ITI_EP = "/v1/generations/image"
LUMAAI_TTV_EP = "/v1/generations"
LUMAAI_ITV_EP = "/v1/generations"
LUMAAI_VTV_EP = "/v1/generations"

LUMAAI_STATUS_IN_PROGRESS = ["queued", "dreaming"]
WAIT_FOR_LUMAI_RESULT = 5.0

# Meshy
MESHY_BASE_EP = "https://api.meshy.ai/openapi"
MESHY_TT3D_EP = "/v2/text-to-3d"
MESHY_IT3D_EP = "/v1/image-to-3d"
MESHY_REMESH_EP = "/v1/remesh"
MESHY_TTTX_EP = "/v1/text-to-texture"

MESHY_MODE_PREVIEW = "preview"
MESHY_MODE_REFINE = "refine"
MESHY_STATUS_FOR_RESULT = ["SUCCEEDED", "FAILED", "EXPIRED"]
MESHY_STATUS_IN_PROGRESS = ["IN_PROGRESS", "PENDING"]
WAIT_FOR_MESHY_RESULT = 5.0

# Mistral AI
MISTRAL_BASE_EP = "https://api.mistral.ai"
MISTRAL_TTT_EP = "/v1/chat/completions"
MISTRAL_FIM_EP = "/v1/fim/completions"
MISTRAL_AGENT_EP = "/v1/agents/completions"

# OpenAI
OPENAI_BASE_EP = "https://api.openai.com"
OPENAI_TTT_EP = "/v1/chat/completions"
OPENAI_TTS_EP = "/v1/audio/speech"
OPENAI_TRANSLATION_EP = "/v1/audio/translations"
OPENAI_TRANSCRIPTION_EP = "/v1/audio/transcriptions"
OPENAI_TTI_EP = "/v1/images/generations"
OPENAI_IMAGE_EDIT_EP = "/v1/images/edits"
OPENAI_IMAGE_VARIATIONS_EP = "/v1/images/variations"

OPENAI_TTS_VOICE_DEFAULT = "alloy"

# Perplexity
PERPLEXITY_TTT_EP = "https://api.perplexity.ai/chat/completions"

# Runway
RUNWAY_BASE_EP = "https://api.dev.runwayml.com"
RUNWAY_ITV_EP = "/v1/image_to_video"
RUNWAY_RESULT_EP = "/v1/tasks/{id}"

RUNWAY_STATUS_IN_PROGRESS = ["PENDING", "THROTTLED", "RUNNING"]
RUNWAY_VERSION = "2024-11-06"
WAIT_FOR_RUNWAY_RESULT = 5.0

# Sambanova
SAMBANOVA_TTT_EP = "https://api.sambanova.ai/v1/chat/completions"

# Skybox
SKYBOX_BASE_EP = "https://backend.blockadelabs.com/api/v1"
SKYBOX_EXPORT_EP = "/skybox/export"
SKYBOX_EXPORT_RESULT_EP = "/skybox/export/{id}"
SKYBOX_GENERATION_EP = "/skybox"
SKYBOX_GENERATION_RESULT_EP = "/imagine/requests/{id}"

SKYBOX_STATUS_IN_PROGRESS = ["pending", "dispatched", "processing"]
SKYBOX_STATUS_RESULT = ["complete", "abort", "error"]
WAIT_FOR_SKYBOX_RESULT = 5.0

# Stable Diffusion
STABLE_DIFFUSION_BASE_EP = "https://api.stability.ai"
STABLE_DIFFUSION_TTI_EP = "/v2beta/stable-image/generate"
STABLE_DIFFUSION_ITI_EP = "/v2beta/stable-image"
STABLE_DIFFUSION_3D_EP = "/v2beta/3d"
STABLE_DIFFUSION_RESULT_EP = "/v2beta/results/{id}"
STABLE_DIFFUSION_ITV_START_EP = "/v2beta/image-to-video"
STABLE_DIFFUSION_ITV_RESULT_EP = "/v2beta/image-to-video/result/{id}"

STABLE_DIFFUSION_STATUS_IN_PROGRESS = ["in-progress"]
WAIT_FOR_STABLE_DIFFUSION_ITI_RESULT = 5.0
WAIT_FOR_STABLE_DIFFUSION_ITV_RESULT = 5.0

# Tripo 3D
TRIPO_BASE_EP = "https://api.tripo3d.ai/v2/openapi"
TRIPO_RESULT_EP = "/task/{task_id}"
TRIPO_TASK_EP = "/task"
TRIPO_UPLOAD_EP = "/upload"
TRIPO_WALLET_EP = "/user/balance"

TRIPO_STATUS_IN_PROGRESS = ["running", "queued"]
TRIPO_MODE_TT3D = "text_to_model"
TRIPO_MODE_IT3D = "image_to_model"
TRIPO_MODE_MV3D = "multiview_to_model"
TRIPO_MODE_REFINE = "refine_model"
TRIPO_MODE_APRC = "animate_prerigcheck"
TRIPO_MODE_ARIG = "animate_rig"
TRIPO_MODE_ARETARGET = "animate_retarget"
TRIPO_MODE_STYLIZE = "stylize_model"
TRIPO_MODE_TEXTURE = "texture_model"
TRIPO_MODE_CONVERSION = "convert_model"
WAIT_FOR_TRIPO_RESULT = 5.0

# Voicevox
VOICEVOX_BASE_EP = "http://localhost:50021"
VOICEVOX_QUERY_EP = "/audio_query"
VOICEVOX_SYNTHESIS_EP = "/synthesis"

# XAI
XAI_TTT_EP = "https://api.x.ai/v1/chat/completions"

# Models that prompt is not required
PROVIDERS_NEED_DUMMY_PROMPT = [
    "elevenlabs_aiso",
    "elevenlabs_dub",
    "elevenlabs_voicechange",
    "elevenlabs_voicedesign",
    "flux1_fal_iti",
    "groq_stt",
    "openai_iti",
    "openai_stt",
    "meshy_it3d",
    "meshy_remesh",
    "meshy_tt3d_refine",
    "meshy_tttx",
    "runway_itv",
    "skybox_ptiv",
    "stable_diffusion_it3d",
    "stable_diffusion_iti",
    "stable_diffusion_itv",
    "tripo_it3d",
    "tripo_mv3d",
    "tripo_texture",
    "tripo_refine",
    "tripo_aprc",
    "tripo_arig",
    "tripo_aretarget",
    "tripo_stylization",
    "tripo_conversion"
]
