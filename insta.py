import re

def check_keywords_in_snippet(snippet, keywords):
    unique_keywords = set()
    for keyword in keywords:
        if re.search(r'\b' + re.escape(keyword.lower()) + r'(\.|,|)\s?\b', snippet.lower()):
            unique_keywords.add(keyword)
            print(f"Keyword found: {keyword}")
    return unique_keywords

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
            # Check if snippet contains any of the specified keywords
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


# Calculate VIP status for Paul Jarrod Frank


name = "Paul Jarrod Frank"
search_results = [
    {
        "snippet": "Discover expert cosmetic dermatology at PFRANKMD by Dr. Paul Jarrod Frank. Transform your skin with cutting-edge treatments. Book your consultation today!...",
        "link": "https://www.pfrankmd.com/"
    },
    {
        "snippet": "195K Followers, 1846 Following, 2540 Posts - Paul Jarrod Frank MD (@drpauljarrodfrank) on Instagram: 'Celebrity Cosmetic Derm∙ SkinGuru ∙ FaceTuner .......",
        "link": "https://www.instagram.com/drpauljarrodfrank/?hl=en"
    },
    {
        "snippet": "In 2005, Dr. Frank launched PFRANKMD™ Skincare, his private label line of products for the consumer market. He continues to be an investigator and consultant .......",
        "link": "https://www.pfrankmd.com/about-dermatology-office-nyc/dr-paul-frank-cosmetic-dermatologist/"
    },
    {
        "snippet": "Cosmetic dermatology and medspa · Experience: PFRANKMD by Dr. Paul Jarrod Frank · Education: NYU langone hospital · Location: New York · 500+ connections on .......",
        "link": "https://www.linkedin.com/in/paul-jarrod-frank-md-1049682a"
    },
    {
        "snippet": "Mar 4, 2016 ... Dr. Frank, director of the Fifth Avenue Dermatology Surgery & Laser Center, meditates with his wife, goes to Central Park with his kids and .......",
        "link": "https://www.nytimes.com/2016/03/06/nyregion/how-paul-jarrod-frank-a-cosmeticdermatologist-spends-his-sundays.html"
    }
]
general_keywords = ["CEO", "Founder", "Co-founder", "President", "Celebrity", "Chief Executive Officer", "Entrepreneur"]
doctor_keywords = ["Doctor", "Doc", "dr.", "Chief", "Board Certified", "MD", "Radiologist", "researcher", "crunchbase", "zocdoc", "physician"]

calculate_vip_status(name, search_results, general_keywords, doctor_keywords)
