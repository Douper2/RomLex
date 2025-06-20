import requests
from bs4 import BeautifulSoup
import re
import random
import json

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

def getsynonym(word):
    word = word.strip().lower()
    url = "https://dexonline.ro/definitie/" + str(word)
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error: {response.status_code}"

    soup = BeautifulSoup(response.text, features="html5lib")
    span = soup.find_all("span", {"class": "badge-relation badge-relation-1"}) # finds the synonym
    synonyms = [span.get_text(strip=True) for span in span]
    if not synonyms:
        return "The synonym cannot be found. Check for typos"

    return synonyms

def getantonym(word):
    word = word.strip().lower()
    url = "https://dexonline.ro/definitie/" + str(word)
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error: {response.status_code}"

    soup = BeautifulSoup(response.text, features="html5lib")
    span = soup.find_all("span", {"class": "badge-relation badge-relation-2"}) # finds the antonym
    antonym = [span.get_text(strip=True) for span in span]
    if not antonym:
        return "The synonym cannot be found. Check for typos"

    return antonym

def check_pos(word=None):
    word = word.strip().lower()
    url = "https://dexonline.ro/definitie/" + str(word)
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error: {response.status_code}"

    soup = BeautifulSoup(response.text, features="html5lib")
    span = soup.find("span", {"class" : "tree-pos-info"})

    if not span:
        return "The part of speech cannot be found. Check for typos."

    return span

def derived_words(word=None):
    word = word.strip().lower()
    url = "https://ro.wiktionary.org/wiki/" + str(word)
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error: {response.status_code}"

    soup = BeautifulSoup(response.text, features="html5lib")
    span = soup.find_all("ul", id="mwbA")

    if not span:
        return f"The words derived from '{word}' cannot be found. Maybe the parser needs some coffee."

    derived = [a.text.strip()
               for ul in span
               for li in ul.find_all("li")
               for a in li.find_all("a")]

    if not derived:
        return f"The words derived from '{word}' cannot be found."

    return derived

def getexpressions(exp=None): # "exp" means expression
    exp = exp.strip().lower()
    url = "https://ro.wiktionary.org/wiki/" + str(exp)
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error: {response.status_code}"

    soup = BeautifulSoup(response.text, features="html5lib")
    span = soup.find_all("ul", id="mwiA")

    if not span:
        return f"The expressions with '{exp}' cannot be found."

    expression = [a.text.strip()
               for ul in span
               for a in ul.find_all("li", id=lambda x: x and x.startswith("mw"))]

    if not expression:
        return f"The expressions with '{exp}' cannot be found."

    return expression

def get_ipa(word):
    word = word.strip().lower()
    url = "https://ro.wiktionary.org/wiki/" + str(word)
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error: {response.status_code}"

    soup = BeautifulSoup(response.text, features="html5lib")
    span = soup.find("span", {"title" : "AFI"})

    if span:
        return span.text.strip()
    else:
        return f"The IPA pronunciation for {word} cannot be found."

def infowordjson(word):
    infoword = word.strip().lower()
    entry = {
        'word' : infoword,
        'definition' : getdefinition(infoword),
        'etymology' : getetymology(infoword),
        'part of speech' : check_pos(infoword),
        'synonyms' : getsynonym(infoword),
        'antonyms' : getantonym(infoword),
        'derived words' : derived_words(infoword),
        'expressions' : getexpressions(infoword)
    }
    return json.dumps(entry, ensure_ascii=False, indent=4)
