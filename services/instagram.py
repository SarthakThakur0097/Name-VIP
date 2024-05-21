import re

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
