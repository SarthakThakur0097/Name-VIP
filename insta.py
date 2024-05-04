import pandas as pd
import requests
import re

def search_results_by_name(name, api_key, cx, keywords):
    url = f"https://www.googleapis.com/customsearch/v1?q={name}&key={api_key}&cx={cx}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Extract the first 5 search results
        search_results = data.get('items', [])[:5]
        return search_results
    else:
        return None

# Read names from Excel sheet
def read_names_from_excel(file_path, sheet_name, first_name_column, last_name_column, middle_name_column=None):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    if middle_name_column:
        names = df.apply(lambda x: f"{x[first_name_column]} {x[middle_name_column]} {x[last_name_column]}" if pd.notnull(x[middle_name_column]) else f"{x[first_name_column]} {x[last_name_column]}", axis=1).tolist()
    else:
        names = df.apply(lambda x: f"{x[first_name_column]} {x[last_name_column]}", axis=1).tolist()
    return names

# Check if snippet contains any of the specified keywords
def calculate_keywords_in_snippet(snippet, keywords):
    unique_keywords = set()
    for keyword in keywords:
        if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', snippet.lower()):
            unique_keywords.add(keyword)
            print(f"Keyword found: {keyword}")
    return len(unique_keywords)

def get_instagram_followers(snippet):
    followers = re.findall(r'(\d+(?:\.\d+)?[mMkK]?)\s*followers', snippet, re.IGNORECASE)
    if followers:
        followers_str = followers[0].replace(',', '')
        if 'm' in followers_str.lower():
            followers_count = int(float(followers_str.lower().replace('m', '')) * 1000000)
        elif 'k' in followers_str.lower():
            followers_count = int(float(followers_str.lower().replace('k', '')) * 1000)
        else:
            followers_count = int(followers_str)
        return followers_count
    else:
        return 0

def calculate_vip_status(name, snippets, general_keywords, doctor_keywords):
    print(f"Calculating VIP status for {name}...")
    vip_status = 0
    links = []
    if snippets:
        vip_count = 0
        instagram_followers = 0
        unique_keywords = set()
        keyword_count_doctor = 0
        for snippet in snippets:
            link = snippet['link']
            print(f"Snippet: {snippet['snippet'][:20]}...\nLink: {link}\n")
            # Check if snippet contains any of the specified keywords
            keyword_count_general = calculate_keywords_in_snippet(snippet['snippet'], general_keywords)
            keyword_count_doctor = max(keyword_count_doctor, calculate_keywords_in_snippet(snippet['snippet'], doctor_keywords))
            unique_keywords.update(set(general_keywords).intersection(snippet['snippet'].lower().split()))
            unique_keywords.update(set(doctor_keywords).intersection(snippet['snippet'].lower().split()))
            followers_count = get_instagram_followers(snippet['snippet'])
            if followers_count >= 100000 and len(unique_keywords) >= 2:
                vip_count += 1
                print(f"{name} - 100k or more followers and 2 or more general keywords: {', '.join(unique_keywords)}")
            elif followers_count >= 100000:
                vip_count += 1
                print(f"{name} - 100k or more followers")
            elif len(unique_keywords) >= 2:
                vip_count += 1
                print(f"{name} - 2 or more general keywords: {', '.join(unique_keywords)}")
            elif keyword_count_doctor >= 2:
                vip_count += 1
                print(f"{name} - 2 or more doctor-related keywords: {', '.join(unique_keywords)}")
            elif keyword_count_doctor == 1:
                vip_count += 1
                print(f"{name} - 1 doctor-related keyword: {', '.join(unique_keywords)}")
            links.append(link)
            instagram_followers = max(instagram_followers, followers_count)

        if vip_count >= 2 and keyword_count_doctor >= 2:
            vip_status = 5
            print(f"{name} - VIP Status 5: 2 or more doctor-related keywords and 100k or more followers")
        elif vip_count >= 2:
            vip_status = 5
            print(f"{name} - VIP Status 5: 2 or more keywords")
        elif vip_count == 1 and keyword_count_doctor >= 1:
            vip_status = 4
            print(f"{name} - VIP Status 4: 1 doctor-related keyword")
        elif vip_count == 1:
            vip_status = 1
            print(f"{name} - VIP Status 1: 2 or more keywords")
        elif instagram_followers >= 100000:
            vip_status = 2
            print(f"{name} - VIP Status 2: 100k or more followers")
        elif vip_count >= 2:
            vip_status = 3
            print(f"{name} - VIP Status 3: 100k or more followers and 2 or more keywords")
        else:
            vip_status = 0
            print(f"{name} - VIP Status 0: Not a VIP")
    print(f"{name}, VIP Status: {vip_status}")
    return vip_status, links


# Debugging snippets
snippets = [
    {
        "snippet": "A member of the Democratic Party, he was the first African-American president in U.S. history. Obama previously served as a U.S. senator representing Illinois ......",
        "link": "https://en.wikipedia.org/wiki/Barack_Obama"
    },
    {
        "snippet": "36M Followers, 10 Following, 919 Posts - Barack Obama (@barackobama) on Instagram: \"Dad, husband, President, citizen.\"...",
        "link": "https://www.instagram.com/barackobama/?hl=en"
    },
    {
        "snippet": "Barack Obama served as the 44th President of the United States. His story is the American story — values from the heartland, a middle-class upbringing in a ......",
        "link": "https://www.whitehouse.gov/about-the-white-house/presidents/barack-obama/"
    },
    {
        "snippet": "Welcome to the Office of Barack and Michelle Obama. We Love You Back. Play video. The Office of Barack and Michelle Obama · Obama Foundation. obama.org. © 2023 ......",
        "link": "https://www.barackobama.com/"
    },
    {
        "snippet": "Great news today: The Biden Administration announced that DACA recipients will now be able to get health care coverage through the Affordable Care Act....",
        "link": "https://twitter.com/BarackObama"
    }
]

general_keywords = ["CEO", "Founder", "Co-founder" , "President"]
doctor_keywords = ["Doctor", "Doc", "dr.", "Chief", "Board Certified", "MD", "Radiologist", "researcher", "crunchbase", "zocdoc", "physician", "provider", "Celebrity", "Chief Executive Officer", "Entrepreneur"]

name = "Barack Hussein Obama"

calculate_vip_status(name, snippets, general_keywords, doctor_keywords)
