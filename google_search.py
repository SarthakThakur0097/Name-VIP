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

def calculate_vip_status(name, search_results, general_keywords, doctor_keywords):
    print(f"Calculating VIP status for {name}...")
    vip_status = 0
    links = []
    if search_results:
        vip_count = 0
        instagram_followers = 0
        keyword_count_general = 0
        keyword_count_doctor = 0
        unique_keywords = set()
        for result in search_results:
            snippet = result.get('snippet', '')
            link = result['link']
            print(f"Snippet: {snippet}...\nLink: {link}\n")
            # Check if snippet contains any of the specified keywords
            keyword_count_general += calculate_keywords_in_snippet(snippet, general_keywords)
            keyword_count_doctor = max(keyword_count_doctor, calculate_keywords_in_snippet(snippet, doctor_keywords))
            unique_keywords.update(set(general_keywords).intersection(snippet.lower().split()))
            unique_keywords.update(set(doctor_keywords).intersection(snippet.lower().split()))
            followers_count = get_instagram_followers(snippet)
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

# Example usage
file_path = r"famous_people.xlsx"  # Use raw string literal
sheet_name = "Sheet1"  # Change to the name of your sheet
first_name_column = "First Name"   # Change to the name of the column containing first names
middle_name_column = "Middle Name"   # Change to the name of the column containing middle names
last_name_column = "Last Name"     # Change to the name of the column containing last names
api_key = "AIzaSyCYAkys1UQKqA9a0J0Mn-n2neAouJV6u8Q"
cx = "100e27accefea433f"
general_keywords = ["CEO", "Founder", "Co-founder", "provider", "Celebrity", "Chief Executive Officer", "President", "Entrepreneur"]
doctor_keywords = ["Doctor", "Doc", "dr.", "Chief", "Board Certified", "MD", "Radiologist", "researcher", "crunchbase", "zocdoc", "physician"]

# Read names from Excel sheet
names = read_names_from_excel(file_path, sheet_name, first_name_column, last_name_column, middle_name_column)

# Create a new DataFrame to store the results
results_df = pd.DataFrame(columns=["Name", "VIP", "Link 1", "Link 2", "Link 3", "Link 4", "Link 5"])

# Search for LinkedIn profiles for each name
for name in names:
    search_results = search_results_by_name(name, api_key, cx, general_keywords + doctor_keywords)
    vip_status, links = calculate_vip_status(name, search_results, general_keywords, doctor_keywords)
    results_df = pd.concat([results_df, pd.DataFrame({"Name": [name], "VIP": [vip_status], "Link 1": [links[0] if len(links) > 0 else ""], "Link 2": [links[1] if len(links) > 1 else ""], "Link 3": [links[2] if len(links) > 2 else ""], "Link 4": [links[3] if len(links) > 3 else ""], "Link 5": [links[4] if len(links) > 4 else ""]})], ignore_index=True)
    print(f"Name: {name}, VIP Status: {vip_status}")

# Save results to Excel file
output_file = "VIP_results.xlsx"
results_df.to_excel(output_file, index=False)
print(f"Results saved to {output_file}")