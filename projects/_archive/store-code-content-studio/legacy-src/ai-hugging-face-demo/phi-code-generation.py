import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# INIT MODEL STORAGE
cache_dir = os.path.abspath("./my_model_cache")
os.environ['TRANSFORMERS_CACHE'] = cache_dir

# INIT GPU CONSUMPTION
torch.set_default_device('cuda')

# AI MODEL
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-1_5", trust_remote_code=True, torch_dtype="auto")
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-1_5", trust_remote_code=True, torch_dtype="auto")

# INPUT PROMPT
prompt = """
please explain your capabilities as an LLM
"""
inputs = tokenizer(prompt, return_tensors="pt", return_attention_mask=False)


# OUTPUT
outputs = model.generate(**inputs, max_length=2048)
text = tokenizer.batch_decode(outputs)[0]
print(text)
