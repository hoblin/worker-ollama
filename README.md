# worker-ollama
Ollama Docker Container for RunPod Serverless Endpoint

## Usage

You can use this endpoint by making a POST request to the serverless URL. Here's an example of a request:

```json
{
  "input": {
    "method_name": "generate",
    "input": {
      "model": "dolphin-mixtral",
      "prompt": {
        "context": "A radiant portrait by Aliza Razell; showing a contemplative young lady, gazing intently into the distance in her minimalist studio, featuring sharp cheekbones, entrancing hazel eyes, strands of chestnut hair falling over her shoulder, and a stroke of vibrant watercolor across her visage.",
        "token": "visage",
        "pos": "NOUN",
        "lemma": "visage"
      },
      "format": "json",
      "system": "You are the \"Comprehensive English Language Dictionary\" API. Your job is to respond with Sense for the given linguistic lemma, along with all the possible Synonyms having the same sense and applicable within the same context.\n\n<|im_start|>user\n{\"context\":\"A radiant portrait by Aliza Razell; showing a contemplative young lady, gazing intently into the distance in her minimalist studio, featuring sharp cheekbones, entrancing hazel eyes, strands of chestnut hair falling over her shoulder, and a stroke of vibrant watercolor across her visage.\",\"token\":\"visage\",\"pos\":\"NOUN\",\"lemma\":\"visage\"}<|im_end|>\n<|im_start|>assistant\n{\"lemma\":\"visage\",\"pos\":\"NOUN\",\"sense\":\"The face or facial expression of a person.\",\"synonyms\":[\"countenance\",\"face\",\"expression\",\"features\",\"physiognomy\",\"mug\",\"profile\",\"mien\",\"aspect\",\"look\",\"appearance\",\"phiz\",\"lineaments\",\"demeanor\"]}<|im_end|>\n"
    }
  }
}
```
