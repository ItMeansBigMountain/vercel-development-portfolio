from transformers import pipeline


# RATE POSITIVE NEUTRAL NEGATIVE OF TEXT
classifier = pipeline("sentiment-analysis")


# OUTPUT
output = classifier.predict(  ["Go fall in a ditch somewhere","but i love you"]  )


# DISPLAY
print( output )