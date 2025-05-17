import requests
from bs4 import BeautifulSoup
import re
import random


# English: An API for the dexonline.ro website, a website for the DEX (The Romanian Explanatory Dictionary)
# Romana: Un API pentru site-ul dexonline.ro

def getdefinition(word):
    word = word.strip().lower()
    url = "https://dexonline.ro/definitie/" + str(word)
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error: {response.status_code}"

    soup = BeautifulSoup(response.text, features="html5lib")
    definition = soup.find_all("span", {"class": "tree-def"}) # finds the definition, for now definition
    if not definition:
        return "The definition cannot be found. Check for typos"

    return definition[0]

def getetymology(word):
    word = word.strip().lower()
    url = "https://dexonline.ro/definitie/" + str(word)
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error: {response.status_code}"

    soup = BeautifulSoup(response.text, features="html5lib")
    language = soup.find_all("span", {"class": "tag"}) # finds the language(s) from which the word comes from
    etymology = soup.find("li", {"class" : "type-etymology depth-1"}) # finds the etymology of the word from the page
    if not etymology:
        return "The etymology cannot be found. Check for typos"

    etym_text = etymology.get_text(separator=" ", strip=True)
    clean_etym = re.sub(r"DEX\s*'?\d+", "", etym_text).strip() # removes the DEX text and year text from the etymology
    clean_etym = re.sub(r'\b(DN|DLRM|NODEX)\b', ' ', clean_etym) # removes the internal dexonline abbreviations
    return clean_etym

    match = re.search(r'From\s+(\w+)\.?\s+([\w\-]+)', etym_text)
    if match:
        lang = match.group(1)
        root = match.group(2)
        return f'From {lang}: "{root}"'

    return f"Etymology: {etym_text}"

def getrandomword(word=None):
    url = "https://dexonline.ro/cuvinte-aleatorii"
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error: {response.status_code}"

    soup = BeautifulSoup(response.text, features="html5lib")
    ranwords = soup.find_all("a", href=lambda x: x and x.startswith("/definitie/"))
    words = [w.text.strip() for w in ranwords if w.text.strip()]
    chosen_word = random.choice(words)

    if not ranwords:
        return "The random words cannot be found for some reason."

    return chosen_word

def getwordofday(word=None):
    url = "https://dexonline.ro/cuvantul-zilei"
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error: {response.status_code}"

    soup = BeautifulSoup(response.text, features="html5lib")
    wordday = soup.find("b")
    wordofday = wordday.get_text().strip()
    if not wordday:
        return "The word of the day cannot be found for some reason."

    return wordofday
