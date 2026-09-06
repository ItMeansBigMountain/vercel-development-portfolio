from transformers import pipeline


# SCORE HOW MUCH RESEMBALENCE A STRING HAS TO IDENTIFIED CATEGORIES
classifier = pipeline("zero-shot-classification")



output = classifier(
    "This is a lesson about Tranformers Library",
    candidate_labels = ["education", "politics" , "business"]
)



print( output )

# {'sequence': 'This is a lesson about Tranformers Library', 'labels': ['education', 'business', 'politics'], 'scores': [0.9901474118232727, 0.007111092563718557, 0.0027414762880653143]}