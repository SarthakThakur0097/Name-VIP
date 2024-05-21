import re

def check_keywords_in_snippet(snippet, keywords):
    unique_keywords = set()
    for keyword in keywords:
        if re.search(r'\b' + re.escape(keyword.lower()) + r'(\.|)\s?\b', snippet.lower()):
            unique_keywords.add(keyword)
    return unique_keywords
