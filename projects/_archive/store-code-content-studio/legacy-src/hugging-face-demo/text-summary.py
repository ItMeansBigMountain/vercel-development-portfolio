from transformers import pipeline

# SUMMARIZE A PASSAGE
classifier = pipeline("summarization")



output = classifier(
    """
Hugging Face's Transformers library offers a wide array of pre-trained models and utilities that can be leveraged to build robust and scalable applications. For instance, if you're interested in Natural Language Processing (NLP), you can use the library to perform tasks like text classification, sentiment analysis, question-answering, and even text generation. Imagine building a customer service chatbot; you could use the question-answering models to automatically respond to customer queries, and sentiment analysis to gauge customer satisfaction. If you're into data analytics, you can use Transformers to extract insights from large volumes of text data. For example, you could analyze customer reviews to identify what features of a product or service are most liked or disliked. The library is also highly useful for educational applications. You could build a system that uses summarization models to condense long articles or documents for easier consumption. For more interactive experiences, you could use text generation models to create conversational agents that can assist in learning a new language or topic. The library supports multiple programming languages including Python and JavaScript, making it versatile for both server-side and client-side development. With its straightforward API and extensive documentation, getting started is generally quick, allowing you to focus more on application logic rather than model intricacies.
    """
)



print( output )

