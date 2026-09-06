from transformers import pipeline


# GENERATE TEXT
classifier = pipeline("text-generation", model="distilgpt2")


# OUTPUT
output = classifier(
    "I will beat Edlen Ring on the day I ",
    num_return_sequences = 2
    # max_length = 60,
)


# DISPLAY
print( output )






# DEFAULT
# [{'generated_text': "I will beat Edlen Ring on the day I _______ hit you in the face with a bike helmet and you will live with a mental health issue later.\n\nYou could die when you're old enough to start a family… and it's"}]

# DISTILGP2
# [{'generated_text': 'I will beat Edlen Ring on the day I \ue000 m leave. With him is the most magnificent of the greats, and that it is to the people of Connecticut.'}]