def format_article(article):
    return f"{article['title']}\n{article['link']}\n{article['summary']}\n"

def manage_configurations(config_file):
    import json
    with open(config_file, 'r') as file:
        return json.load(file)

def extract_relevant_info(article):
    return {
        'title': article.get('title', 'No Title'),
        'link': article.get('url', 'No URL'),
        'summary': article.get('summary', 'No Summary')
    }