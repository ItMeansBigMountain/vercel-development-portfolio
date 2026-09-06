from transformers import pipeline


# FILL IN THE BLANK
classifier = pipeline("fill-mask")



output = classifier(
    "This is a lesson about <mask>",
    top_k=2
)



print( output )


# [{'score': 0.014694135636091232, 'token': 10795, 'token_str': ' evolution', 'sequence': 'This is a lesson about evolution'}, {'score': 0.011852252297103405, 'token': 27352, 'token_str': ' humility', 'sequence': 'This is a lesson about humility'}]