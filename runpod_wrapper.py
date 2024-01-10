# This is runpod_wrapper.py file
import runpod
from typing import Any, Literal, TypedDict
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)


class HandlerInput(TypedDict):
    method_name: Literal["generate"]
    input: Any


class HandlerJob(TypedDict):
    input: HandlerInput


# Load the list of models at startup
base_url = "http://localhost:11434"
response = requests.get(f"{base_url}/api/tags")
# Extract the model names
models = [model["name"] for model in response.json()["models"]]
logging.info(f"Loaded models: {models}")


def pull_model(model_name: str):
    """Download a new model."""
    logging.info(f"Pulling model: {model_name}")
    response = requests.post(
        url=f"{base_url}/api/pull",
        headers={"Content-Type": "application/json"},
        json={
            "name": model_name,
            "stream": False
        },
    )
    response.encoding = "utf-8"
    return response.json()


def handler(job: HandlerJob):
    input = job["input"]

    # Split the model name and tag
    model_name, _, model_tag = input["input"]["model"].partition(':')

    # Check if the model is in the list of models
    if model_tag:
        model_in_list = input["input"]["model"] in models
    else:
        model_in_list = any(model.split(
            ':')[0] == model_name for model in models)

    if not model_in_list:
        logging.info(f"Model not in list: {input['input']['model']}")
        # If the model is not in the list, download it
        pull_model(input["input"]["model"])
        # Add the model to the list
        models.append(input["input"]["model"])

    logging.info(f"Generating using model: {input['input']['model']}")

    # Streaming is not supported in serverless mode
    input["input"]["stream"] = False

    response = requests.post(
        url=f"{base_url}/api/{input['method_name']}/",
        headers={"Content-Type": "application/json"},
        json=input["input"],
    )
    response.encoding = "utf-8"

    return response.json()


runpod.serverless.start({"handler": handler})
