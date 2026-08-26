from transformers import pipeline

class ScriptGenerator:
    def __init__(self, model_name: str, device: int = -1):
        self.generator = pipeline("text-generation", model=model_name, device=device)

    def generate_script(self, prompt: str, max_length: int = 50, num_return_sequences: int = 1) -> str:
        # Actual prompt for the model
        actual_prompt = f"News Story: {prompt}\nPersonality: Analytical, Humorous, Sinister, Informative\nTarget Audience: 28-year-olds with nothing going on in their lives.\nRole: News anchor for a very famous news agency.\n\nReport:"
        
        outputs = self.generator(actual_prompt, max_length=max_length, num_return_sequences=num_return_sequences, return_full_text=False)
        
        if num_return_sequences == 1:
            return outputs[0]['generated_text']
        else:
            return [output['generated_text'] for output in outputs]






if __name__ == "__main__":
    import requests
    from bs4 import BeautifulSoup

    # INIT MODEL
    script_gen = ScriptGenerator("distilgpt2", device=0) 

    # EXTRACT HTML FROM REQUEST
    data = requests.get("https://www.foxnews.com/world/canada-under-fire-applauding-literal-nazi-parliament-during-zelenskyy-visit")
    html = data.text
    soup = BeautifulSoup(html, 'html.parser')
    main_content = soup.find('div', {'class': 'article-body'})


    # EXTRACT TEXT FROM HTML
    prompt = ""
    for string in list(set(main_content.stripped_strings))[:-20]:
        prompt += f"\n{string}"

    # OUTPUT
    # print(prompt)
    script = script_gen.generate_script(prompt, max_length=1024, num_return_sequences=1)
    print(script)


