import json
import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../llmmaster"))

import pytest
from requests.models import Response

from llmmaster import LLMMaster


API_KEY_FILE = "api_key_pairs.txt"
TEST_OUTPUT_PATH = "test-outputs"


@pytest.fixture(scope="session", autouse=True)
def setup_api_client() -> None:
    pass


def load_api_keys() -> str:
    return Path(API_KEY_FILE).read_text(encoding="utf-8")


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--run-api",
        action="store_true",
        default=False,
        help="Run tests that make actual API calls"
    )
    parser.addoption(
        "--load-api-file",
        action="store_true",
        default=False,
        help="Load API keys from text file defined in conftest.py"
    )


def verify_instance(instance: any, expected_class: any) -> bool:
    """
    Simple function to verify instance type in LLMMaster.
    """
    print(f"Parameters = {instance.parameters}")
    return False if not isinstance(instance, expected_class) else True


def write_json(save_as: str = '', output: dict = {}) -> None:
    """
    Write convereted Response to a JSON file.
    Only text contents are available.
    Error occurs if output includes any binary data.
    """
    os.makedirs(TEST_OUTPUT_PATH, exist_ok=True)

    filepath = os.path.join(TEST_OUTPUT_PATH, save_as)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Saved as {filepath}")


def run_llmmaster(master: LLMMaster) -> None:
    """
    Main execution function to test LLMMaster.
    This function is used for dict output with text content only.
    Use `execute_restapi()` for general REST API.
    """
    print("Run LLMMaster from run_llmmaster()")

    try:
        master.run()

    except Exception as e:
        msg = f"An error occurred during API calls: {str(e)}"
        raise Exception(msg)

    print("Payloads")
    for key, instance in master.instances.items():
        print(f"Payload for {key} = {instance.payload}")

    print("Responses")
    for key, result in master.results.items():
        if isinstance(result, dict):
            print(f"Result for {key} = {json.dumps(result, indent=2)}")
            write_json(save_as=f"{key}.json", output=result)
        else:
            print(f"Result for {key}, type ({type(result)}) = {result}")

    print(f"Elapsed time in total (sec): {master.elapsed_time}")


def execute_restapi(master: LLMMaster, format: str = '') -> None:
    """
    This function is used for general REST API.
    Save response data in json and binary format.
    """
    print("Run LLMMaster from execute_restapi()")

    try:
        master.run()
    except Exception as e:
        pytest.fail(f"An error occurred during API calls: {str(e)}")

    print("Responses")

    for name, response in master.results.items():
        if isinstance(response, Response):
            save_response(response, key=name, format=format)
        else:
            msg = f"Failed to generate in {name}: {response}"
            raise Exception(msg)

    print(f"Elapsed time in total (sec): {master.elapsed_time}")


def save_response(
    response: Response,
    key: str = '',
    format: str = ''
) -> None:
    """
    Save response data of REST API in json and binary format.
    Arguments:
      - response: object returned from requests get/post
      - key: base file name for json and binary
      - format: extension, e.g. jpg, png, wav, mp4
    Remarks:
      - response.connection not implemented
      - response.raw not implemented
    """
    response_dict = {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "url": response.url,
        "encoding": response.encoding,
        "reason": response.reason,
        "elapsed": str(response.elapsed),
        "cookies": {k: v for k, v in response.cookies.items()},
        "history": [
            {
                "url": r.url,
                "status_code": r.status_code,
                "reason": r.reason
            }
            for r in response.history
        ],
        "request": {
            "method": response.request.method,
            "url": response.request.url,
            "headers": dict(response.request.headers),
        }
    }

    # response.request.body
    buff = response.request.body
    if isinstance(buff, bytes):
        response_dict["request"]["body"] = "Binary data output."
    elif isinstance(buff, str):
        response_dict["request"]["body"] = buff
    else:
        response_dict["request"]["body"] = None

    # response.text
    if ("text" in response.headers["Content-Type"] or
       "xml" in response.headers["Content-Type"]):
        response_dict["text"] = response.text
    else:
        response_dict["text"] = "Non-text content output."

    # handle response.content based on its type
    if hasattr(response, "content") and isinstance(response.content, bytes):
        save_as = os.path.join(TEST_OUTPUT_PATH, f"{key}.{format}")
        with open(save_as, "wb") as f:
            f.write(response.content)
        msg = f"Binary content saved to {save_as}"
        response_dict["content"] = msg
        print(msg)

    # save to JSON file
    save_as = os.path.join(TEST_OUTPUT_PATH, f"{key}.json")
    with open(save_as, "w", encoding="utf-8") as f:
        json.dump(response_dict, f, indent=2, ensure_ascii=False)
    print(f"Response information saved to {save_as}")
