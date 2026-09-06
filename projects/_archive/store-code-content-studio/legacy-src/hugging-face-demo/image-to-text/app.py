# ENVIRONMENT VARIABLES
from dotenv import find_dotenv , load_dotenv
import os 



# HUGGING FACE AI MODELS
from transformers import pipeline
import requests


# LANGCHAIN
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI





# LOAD API KEYS FROM .ENV
load_dotenv(find_dotenv())
huggingFaceToken = os.getenv("HUGGINGFAVEHUB_API_TOKEN")










def generate_story_GPT(scenario):
    template = """
    You are a story teller,
    you can generate a short story based on a simple narritive. Be as creative and wayward as you would like. Please keep the story within 50 words.

    CONTEXT: {scenario}
    STORY: 
    
    """

    # CREATE PROMPT
    prompt = PromptTemplate(template=template, input_variables=["scenario"])

    # CREATE LLM CHAIN USING PROMPT
    story_llm = LLMChain(
        llm = OpenAI(model_name="gpt-3.5-turbo", temperature = 1),
        prompt=prompt,
        verbose=True
    )

    # FIT VARS CONFIGURED IN PROMPT
    story = story_llm.predict(scenario=scenario)

    print(story)
    return story


def img2Text(url):
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    text = image_to_text(url)[0]["generated_text"]
    print(text)
    return text


def text2Speech(story):
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











# Calling functions down here
scenario = img2Text("jasonandi.png")
# story = generate_story_GPT(scenario)
# text2Speech(story)