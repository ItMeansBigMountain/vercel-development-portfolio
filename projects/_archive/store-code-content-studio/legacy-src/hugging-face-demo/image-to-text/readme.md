# [HuggingFace Models](https://huggingface.co/models)

- using the python `transformers` lib we can interact with HuggingFace Hub


## [Tasks](https://huggingface.co/tasks)
- Categories of AI models



# TRANSFORMERS PYTHON PYPY 
```
from transformers import pipeline

# LOAD HUGGING FACE API
load_dotenv(find_dotenv())

# LOAD TASK AND MODEL IN PIPELINE PARAMS
image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

# OUTPUT
text = image_to_text("path-to-pic.png")[0]["generated_text"]
print(text)


```


# REQUESTS PYTHON API 
```
import requests

huggingFaceToken = os.getenv("HUGGINGFAVEHUB_API_TOKEN")


# INIT API VARS
API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
headers = {"Authorization": f"Bearer {huggingFaceToken}"}
payload = { "inputs": story, }

# POST API CALL
response = requests.post(API_URL, headers=headers, json=payload)

# SAVE RESPONSE INTO FILE
with open("audio.flac", "wb") as file:
    file.write(response.content)

# display
print(response.content)


```