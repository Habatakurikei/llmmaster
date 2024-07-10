# API settings
ANTHROPIC_KEY_NAME = 'ANTHROPIC_API_KEY'
GEMINI_KEY_NAME = 'GEMINI_API_KEY'
GROQ_KEY_NAME = 'GROQ_API_KEY'
OPENAI_KEY_NAME = 'OPENAI_API_KEY'
PERPLEXITY_KEY_NAME = 'PERPLEXITY_API_KEY'

PERPLEXITY_EP = 'https://api.perplexity.ai'

# TTI setting
MAX_TOKENS = 4096
TEMPERATURE = 0.7

# TTT settings
OPENAI_TTI_SIZE_LIST = ['256x256', '512x512', '1024x1024',
                        '1024x1792', '1792x1024']
OPENAI_TTI_QUALITY_LIST = ['standard', 'hd']
OPENAI_TTI_DEFAULT_SIZE = '1024x1024'
OPENAI_TTI_DEFAULT_QUALITY = 'hd'
OPENAI_TTI_DEFAULT_N = 1

# settings for summon
SUMMON_LIMIT = 32
WAIT_FOR_SUMMONING = 1

# Default models setting
DEFAULT_TTT_MODELS = {'anthropic': 'claude-3-5-sonnet-20240620',
                      'google': 'gemini-1.5-flash',
                      'groq': 'llama3-70b-8192',
                      'openai': 'gpt-4o',
                      'perplexity': 'llama-3-sonar-large-32k-online'}

DEFAULT_TTI_MODELS = {'openai_tti': 'dall-e-3'}


def _full_default_list():
    full_list = {}
    full_list.update(DEFAULT_TTT_MODELS)
    full_list.update(DEFAULT_TTI_MODELS)
    return full_list


FULL_DEFAULT_MODELS = _full_default_list()
