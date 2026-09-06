from transformers import pipeline


# TRANSLATE TEXT (model is french to english)
classifier = pipeline("translation", model = "Helsinki-NLP/opus-mt-fr-en")



output = classifier("Je veux des sandwichs" )



print( output )

# [{'translation_text': 'I want sandwiches'}]