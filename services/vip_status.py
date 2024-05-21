from utils.keywords import check_keywords_in_snippet
from services.instagram import get_instagram_followers

def calculate_vip_status(name, search_results, general_keywords, doctor_keywords):
    print(f"Calculating VIP status for {name}...")
    vip_status = 0
    links = []
    if search_results:
        instagram_followers = 0
        unique_general_keywords = set()
        unique_doctor_keywords = set()
        for result in search_results:
            snippet = result.get('snippet', '')
            link = result['link']
            print(f"Snippet: {snippet}...\nLink: {link}\n")
            unique_general_keywords.update(check_keywords_in_snippet(snippet, general_keywords))
            unique_doctor_keywords.update(check_keywords_in_snippet(snippet, doctor_keywords))
            followers_count = get_instagram_followers(snippet)
            links.append(link)
            instagram_followers = max(instagram_followers, followers_count)

        if len(unique_general_keywords) >= 2:
            vip_status = 1
            print(f"{name} - VIP Status 1: 2 or more general keywords")
        if instagram_followers >= 100000:
            print("100k+ followers")
            vip_status = 2
        if instagram_followers >= 100000 and len(unique_general_keywords) >= 2:
            vip_status = 3
        if instagram_followers >= 100000 and len(unique_doctor_keywords) == 1:
            vip_status = 4
        if instagram_followers >= 100000 and len(unique_doctor_keywords) >= 2:
            vip_status = 5
    else:
        print(f"{name} - VIP Status 0: Not a VIP")
    print(f"{name}, VIP Status: {vip_status}")
    return vip_status, links
