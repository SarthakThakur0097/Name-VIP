import logging
from utils.keywords import check_keywords_in_snippet
from services.instagram import get_instagram_followers

# Configure logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create a FileHandler to write logs to a text file (overwrite mode)
file_handler = logging.FileHandler('logs.txt', mode='w')  # Change mode to 'w' for overwrite
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def calculate_vip_status(name, search_results, general_keywords, doctor_keywords):
    logger.info(f"Calculating VIP status for {name}...")
    vip_status = 0
    links = []

    if search_results:
        instagram_followers = 0
        unique_general_keywords = set()
        unique_doctor_keywords = set()

        for result in search_results:
            snippet = result.get('snippet', '')
            link = result['link']
            logger.debug(f"Snippet: {snippet}...\nLink: {link}\n")

            unique_general_keywords.update(check_keywords_in_snippet(snippet, general_keywords))
            unique_doctor_keywords.update(check_keywords_in_snippet(snippet, doctor_keywords))

            followers_count = get_instagram_followers(snippet)
            links.append(link)
            instagram_followers = max(instagram_followers, followers_count)

            logger.info(f"Snippet: {snippet}")  # Include the snippet in the log

        if len(unique_general_keywords) >= 2:
            vip_status = 1
            logger.info(f"{name} - VIP Status 1: 2 or more general keywords")

        if instagram_followers >= 100000:
            logger.info("100k+ followers")
            vip_status = 2

        if instagram_followers >= 100000 and len(unique_general_keywords) >= 2:
            vip_status = 3

        if instagram_followers >= 100000 and len(unique_doctor_keywords) == 1:
            vip_status = 4

        if instagram_followers >= 100000 and len(unique_doctor_keywords) >= 2:
            vip_status = 5

        if unique_general_keywords:
            logger.info(f"Unique general keywords for {name}: {' '.join(unique_general_keywords)}")

        if unique_doctor_keywords:
            logger.info(f"Unique doctor keywords for {name}: {' '.join(unique_doctor_keywords)}")

        logger.info(f"{name}, VIP Status: {vip_status}")
        logger.info("")  # Add a blank line after each person
        logger.info("-" * 50)  # Add a hyphen line after each person

    else:
        logger.warning(f"No search results found for {name}")
        logger.info(f"{name} - VIP Status 0: Not a VIP")
        logger.info("")  # Add a blank line after each person
        logger.info("-" * 50)  # Add a hyphen line after each person

    return vip_status, links
