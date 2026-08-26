import json
import os
from pathlib import Path

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    EntitiesOptions,
    KeywordsOptions,
    CategoriesOptions,
    ConceptsOptions,
    EmotionOptions,
    RelationsOptions,
    SemanticRolesOptions,
    SentimentOptions,
    SyntaxOptions,
)

DEFAULT_IBM_NLU_CREDENTIALS_FILE = '/opt/data/credentials/ibm-nlu-api-key.json'
DEFAULT_IBM_NLU_URL = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/dd2384c5-cbf9-45c5-9dc8-fb9dd95dea56'


def _credentials_from_file():
    credentials_file = os.getenv('IBM_WATSON_CREDENTIALS_FILE') or os.getenv('WATSON_CREDENTIALS_FILE') or DEFAULT_IBM_NLU_CREDENTIALS_FILE
    path = Path(credentials_file)
    if not path.exists():
        return {}
    with path.open() as handle:
        return json.load(handle)


def _get_credentials():
    file_credentials = _credentials_from_file()
    api_key = (
        os.getenv('WATSON_API_KEY')
        or os.getenv('WATSON_APIKEY')
        or os.getenv('WATSON_NLU_APIKEY')
        or os.getenv('IBM_WATSON_API_KEY')
        or file_credentials.get('apikey')
    )
    url = (
        os.getenv('WATSON_SERVICE_URL')
        or os.getenv('WATSON_INSTANCE_URL')
        or os.getenv('WATSON_NLU_URL')
        or os.getenv('IBM_WATSON_SERVICE_URL')
        or file_credentials.get('url')
        or DEFAULT_IBM_NLU_URL
    )
    return api_key, url


def login():
    api_key, url = _get_credentials()
    if not api_key or not url:
        raise RuntimeError('IBM Watson NLU credentials are not configured')
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator,
    )
    natural_language_understanding.set_service_url(url)
    return natural_language_understanding


def analyzeText(client, text):
    response = client.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=True, sentiment=True, limit=2),
            categories=CategoriesOptions(limit=100),
            concepts=ConceptsOptions(limit=100),
            emotion=EmotionOptions(),
            relations=RelationsOptions(),
            semantic_roles=SemanticRolesOptions(keywords=True, entities=True),
            sentiment=SentimentOptions(),
            syntax=SyntaxOptions(sentences=True),
        ),
    ).get_result()
    return json.dumps(response, indent=2)


# Compatibility shim for old Discord bot code that expected IBM Tone Analyzer.
# Tone Analyzer is no longer needed here; return a Tone-like response derived from NLU emotion/sentiment.
def toneLogin():
    return login()


def tone_CLIENT(client, text):
    result = json.loads(analyzeText(client, text))
    emotion = result.get('emotion', {}).get('document', {}).get('emotion', {})
    sentiment = result.get('sentiment', {}).get('document', {})
    tones = []
    for name, score in sorted(emotion.items(), key=lambda item: item[1], reverse=True):
        if score >= 0.25:
            tones.append({'score': score, 'tone_id': name, 'tone_name': name.capitalize()})
    if not tones and sentiment.get('label'):
        tones.append({
            'score': abs(sentiment.get('score') or 0),
            'tone_id': sentiment['label'],
            'tone_name': sentiment['label'].capitalize(),
        })
    return json.dumps({'document_tone': {'tones': tones}}, indent=2)
