import base64
import os
from mimetypes import guess_type
from urllib.parse import urlparse
from urllib.parse import urlunparse

from requests import post
from requests.models import Response

from .config import TRIPO_BASE_EP
from .config import TRIPO_UPLOAD_EP


# Vision input for Image-To-Text LLMs

def common_vision_prompt(
    prompt: str = '',
    image_path: list[str] = []
) -> list[dict]:
    """
    Common function for vision input to LLM.
    Features:
      - Both online and local image paths are supported.
      - Multiple images can be provided, while each LLM may have
        different limits.
    """
    contents = [{"type": "text", "text": prompt}]

    for entry in image_path:
        if entry.startswith(("http://", "https://")):
            # Handle online image
            url = _sanitize_url(entry)
        else:
            # Handle local image
            file_type = guess_type(entry)[0]
            image_data = _encode_base64(entry)
            url = f"data:{file_type};base64,{image_data}"

        contents.append({
            "type": "image_url",
            "image_url": {
                "url": url
            }
        })

    return contents


def anthropic_vision_prompt(
    prompt: str = '',
    image_path: list[str] = []
) -> list[dict]:
    """
    Create a prompt for Anthropic LLM vision input.
    Set return object to prompt of LLMMaster (content in messages).
    Acceptable image formats: jpeg, png, gif and webp.
    Online image URL: not supported.
    Local image path: supported.
    """
    contents = [{"type": "text", "text": prompt}]
    for entry in image_path:
        contents.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": guess_type(entry)[0],
                "data": _encode_base64(entry),
            }
        })
    return contents


def google_vision_prompt(
    prompt: str = '',
    image_path: list[str] = []
) -> list[dict]:
    """
    Create a prompt for Google LLM vision input.
    Set return object to prompt of LLMMaster (parts in contents).
    Only local image paths are supported. Deprecated for online image URL.
    """
    parts = [{"text": prompt}]
    for entry in image_path:
        parts.append({
            "inline_data": {
                "mimeType": guess_type(entry)[0],
                "data": _encode_base64(entry)
            }
        })
    return parts


def xai_vision_prompt(
    prompt: str = '',
    image_path: list[str] = []
) -> list[dict]:
    """
    Create a prompt for XAI LLM vision input.
    Set return object to prompt of LLMMaster (content in messages).
    Both online and local image paths are supported.
    Different from Groq, XAI needs 'detail' option.
    """
    contents = [{"type": "text", "text": prompt}]

    for entry in image_path:
        if entry.startswith(("http://", "https://")):
            # Handle online image
            url = _sanitize_url(entry)
        else:
            # Handle local image
            file_type = guess_type(entry)[0]
            image_data = _encode_base64(entry)
            url = f"data:{file_type};base64,{image_data}"

        contents.append({
            "type": "image_url",
            "image_url": {
                "url": url,
                "detail": "high"
            }
        })

    return contents


def groq_vision_prompt(
    prompt: str = '',
    image_path: list[str] = []
) -> list[dict]:
    """
    Create a prompt for Groq LLM vision input.
    Important: currently only one image is supported.
    """
    return common_vision_prompt(prompt, image_path)


def mistral_vision_prompt(
    prompt: str = '',
    image_path: list[str] = []
) -> list[dict]:
    """
    Same as Groq but multiple images are acceptable.
    """
    return common_vision_prompt(prompt, image_path)


def openai_vision_prompt(
    prompt: str,
    image_path: list[str]
) -> list[dict]:
    """
    Only online image URL is supported.
    """
    contents = [{"type": "text", "text": prompt}]
    for entry in image_path:
        contents.append({
            "type": "image_url",
            "image_url": {
                "url": _sanitize_url(entry)
            }
        })
    return contents


def sambanova_vision_prompt(
    prompt: str = '',
    image_path: list[str] = []
) -> list[dict]:
    """
    Same as Groq.
    Important: currently only one image is supported.
    """
    return common_vision_prompt(prompt, image_path)


# Image input for other modality models

def common_image_input(image_path: str = '') -> str:
    """
    Common function for image input.
    Both local file path and online URLs are supported.
    Use direct URL or base64 encoded data.
    Binary data not supported.
    """
    url = ""
    if image_path.startswith(("http://", "https://")):
        # Handle online image
        url = _sanitize_url(image_path)
    else:
        # Handle local image
        file_type = guess_type(image_path)[0]
        image_data = _encode_base64(image_path)
        url = f"data:{file_type};base64,{image_data}"
    return url


def flux1_fal_image_input(image_path: str = '') -> str:
    """
    Flux1 Fal Image-To-Image model input.
    """
    return common_image_input(image_path)


def meshy_image_input(image_path: str = '') -> str:
    """
    Meshy Image-To-3D model input.
    """
    return common_image_input(image_path)


def runway_image_input(image_path: str = '') -> str:
    """
    Runway Image-To-Video model input.
    """
    return common_image_input(image_path)


def skybox_image_input(image_path: str = '') -> str:
    """
    Skybox Image-To-Panorama model input.
    """
    return common_image_input(image_path)


def tripo_image_input(image_path: str = '', api_key: str = '') -> dict:
    """
    Tripo Image-To-3D model input.
    Both local and online image paths are supported.
    Tripo asks to upload image to its server so api_key is required.
    """
    file = {}

    if image_path.startswith(("http://", "https://")):
        # Handle online image
        file["url"] = _sanitize_url(image_path)

    else:
        # Handle local image. Upload image to Tripo server and get file id.
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")

        url = TRIPO_BASE_EP + TRIPO_UPLOAD_EP
        headers = {"Authorization": f"Bearer {api_key}"}

        with open(image_path, "rb") as fp:
            files = {"file": (image_path, fp, guess_type(image_path)[0])}
            response = post(url, headers=headers, files=files)

        response_json = response.json()
        file["file_token"] = response_json["data"]["image_token"]

    file["type"] = os.path.splitext(image_path)[1].lower()[1:]

    return file


# Audio input to LLM

def openai_audio_prompt(prompt: str = '', audio_path: str = '') -> list[dict]:
    """
    Create a prompt for OpenAI LLM audio input.
    Supported formats: wav only.
    """
    return [
        {
            "type": "text",
            "text": prompt
        },
        {
            "type": "input_audio",
            "input_audio": {
                "data": _encode_base64(audio_path),
                "format": os.path.splitext(audio_path)[1].lower()[1:]
            }
        }
    ]

# PDF input to LLM


def anthropic_pdf_prompt(
    prompt: str = '',
    pdf_path: str = ''
) -> list[dict]:
    """
    Create a prompt for Anthropic LLM PDF input.
    Set return object to prompt of LLMMaster (content in messages).
    """
    contents = [{"type": "text", "text": prompt}]
    contents.append({
        "type": "document",
        "source": {
            "type": "base64",
            "media_type": "application/pdf",
            "data": _encode_base64(pdf_path),
        }
    })
    return contents

# Output processing


def extract_llm_response(response: dict = {}) -> str:
    """
    Extract the response from the LLM output.
    """
    message = ""
    if "choices" in response and response["choices"]:
        # most common case
        for item in response["choices"]:
            if "message" in item and "content" in item["message"]:
                message += item["message"]["content"].strip()
    elif "content" in response and response["content"]:
        # for Anthropic
        for item in response["content"]:
            if "text" in item:
                message += item["text"].strip()
    elif "candidates" in response and response["candidates"]:
        # for Google
        for item in response["candidates"]:
            if "content" in item and "parts" in item["content"]:
                raw_text = item["content"]["parts"][0]["text"]
                message += raw_text.strip()
    elif "text" in response:
        message += response["text"].strip()
    else:
        message += "Unable to find text key in response."
    return message


def decode_base64(base64_string: str = '', save_as: str = '') -> bytes:
    """
    Decode base64 string to binary file like audio or image.
    Return the binary data, save it if save_as is provided or both.
    save_as: path to save the decoded file including extension.
    """
    binary_data = base64.b64decode(base64_string)
    if save_as:
        with open(save_as, "wb") as file:
            file.write(binary_data)
    return binary_data


def flux1_fal_image_save(
    result: dict = {},
    save_as: str = "flux1_fal_output"
) -> None:
    """
    Save the image data from Flux1 FAL response.
    """
    for i, item in enumerate(result["images"]):
        ext = item["content_type"].split("/")[1]
        b64 = item["url"].replace(f"data:{item['content_type']};base64,", "")
        decode_base64(b64, save_as=f"{save_as}_{i:02d}.{ext}")


# Supporting functions

def _encode_base64(file_path: str = '') -> str:
    """
    Encode image/audio to base64.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "rb") as fp:
        file_data = base64.b64encode(fp.read()).decode("utf-8")
    return file_data


def _sanitize_url(url: str = '') -> str:
    """
    Sanitize the URL to remove any trailing slashes.
    Used for image URL input.
    """
    parsed = urlparse(url)
    return urlunparse(parsed)


def debug_response(response: any) -> None:
    """
    Save the response to a text file.
    Used for debugging only.
    """
    save_as = "debug_response.txt"
    text = ''
    if isinstance(response, Response):
        text += f"Status = {response.status_code}\n"
        text += f"Text = {response.text}\n"
    elif isinstance(response, str):
        text += f"Response (str) = {response}\n"
    else:
        text += "Response is not a string or Response object\n"
    with open(save_as, "w", encoding="utf-8") as file:
        file.write(text)
        print(f"Debug response saved to {save_as}")
