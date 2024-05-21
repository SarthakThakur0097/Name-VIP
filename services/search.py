import requests

def search_results_by_name(name, api_key, cx):
    url = f"https://www.googleapis.com/customsearch/v1?q={name}&key={api_key}&cx={cx}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        search_results = data.get('items', [])[:5]
        return search_results
    else:
        return None
