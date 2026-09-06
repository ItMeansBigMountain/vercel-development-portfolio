from transformers import pipeline


# SPLIT A SENTENCE UP TO IT'S MENTIONED ENTITIES
classifier = pipeline("ner" , grouped_entities=True)



output = classifier( "Paris Hilton went to Paris France." )



print( output )



# [
#     {'entity_group': 'PER', 'score': 0.99415296, 'word': 'Paris Hilton', 'start': 0, 'end': 12}, 
#     {'entity_group': 'LOC', 'score': 0.9986485, 'word': 'Paris France', 'start': 21, 'end': 33}
# ]