import pandas as pd
from services.search import search_results_by_name
from services.vip_status import calculate_vip_status
from services.excel import read_names_from_excel
from utils.keywords import check_keywords_in_snippet
from services.instagram import get_instagram_followers
from dotenv import load_dotenv
import os
# Constants
file_path = r"famous_people.xlsx"
sheet_name = "Sheet1"
first_name_column = "First Name"
middle_name_column = "Middle Name"
last_name_column = "Last Name"
load_dotenv()
print(os.getenv("API_KEY"))
api_key = os.getenv("API_KEY")
cx = os.getenv("CX")
general_keywords = ["CEO", "Founder", "Co-founder", "President", "Celebrity", "Chief Executive Officer", "Entrepreneur"]
doctor_keywords = ["Doctor", "Doc", "dr.", "Chief", "Board Certified", "MD", "Radiologist", "researcher", "crunchbase", "zocdoc", "physician"]

# Read names from Excel sheet
names = read_names_from_excel(file_path, sheet_name, first_name_column, last_name_column, middle_name_column)

# Create a new DataFrame to store the results
results_df = pd.DataFrame(columns=["Name", "VIP", "Link 1", "Link 2", "Link 3", "Link 4", "Link 5"])

# Search for LinkedIn profiles for each name
for name in names:
    search_results = search_results_by_name(name, api_key, cx)
    vip_status, links = calculate_vip_status(name, search_results, general_keywords, doctor_keywords)
    results_df = pd.concat([results_df, pd.DataFrame({"Name": [name], "VIP": [vip_status], "Link 1": [links[0] if len(links) > 0 else ""], "Link 2": [links[1] if len(links) > 1 else ""], "Link 3": [links[2] if len(links) > 2 else ""], "Link 4": [links[3] if len(links) > 3 else ""], "Link 5": [links[4] if len(links) > 4 else ""]})], ignore_index=True)
    print(f"Name: {name}, VIP Status: {vip_status}")

# Save results to Excel file
output_file = "VIP_results.xlsx"
results_df.to_excel(output_file, index=False)
print(f"Results saved to {output_file}")
