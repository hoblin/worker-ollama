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
        json={"name": model_name},
    )
    response.encoding = "utf-8"
    return response.json()


def handler(job: HandlerJob):
    input = job["input"]

    # Check if the model is in the list of models
    model_name = input["input"]["model"]
    if model_name not in models:
        # If the model is not in the list, download it
        pull_model(model_name)
        # Add the model to the list
        models.append(model_name)

    logging.info(f"Generating using model: {model_name}")

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
