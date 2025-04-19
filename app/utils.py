
import re
from nltk.stem import WordNetLemmatizer
import pickle
import json

model__ = None
common_pidgin_slang = None

def normalize_text(text):
    ## Fix common typos
    text = re.sub(r"\b(?:tran[s|z]f?er|tf|trf)\b", "transfer", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(?:mon[i|e])\b", "money", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(?:plent[i|y])\b", "plenty", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(?:notin)\b", "nothing", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(?:acount|acnt|aza)\b", "account", text, flags=re.IGNORECASE)
    #standardize currency symbols
    text = re.sub(r"\$|USD|us\sdollars", "usd ", text)
    text = re.sub(r"₦|NGN|naira", "ngn ", text)
    # Remove excessive punctuation (keep ? and ! for urgency cues)
    text = re.sub(r"[^\w\s|!|?]","",text)
    return text.lower()

def preserve_pidgin(text):
    for slang,std in common_pidgin_slang.items():
        pattern = rf"\b{slang}\b"
        text = re.sub(pattern,std,text, flags=re.IGNORECASE)
    return text

def remove_contact_info(text):
    text = re.sub(r"\b(?:\+?\d{10,13}|[\w\.-]+@[\w\.-]+|\w+\.(?:com|ng|org))\b", "[CONTACT]", text)
    return text
 
def lemmatize(text):
    lemmatizer = WordNetLemmatizer()
    words = " ".join([lemmatizer.lemmatize(text,pos="a") for text in text.split(" ")])
    return words

def highlight_scam_terms(text):
    SCAM_KEYWORDS = ["maga","inheritance", "lottery", "urgent", "percentage", "bonus"]
    for term in SCAM_KEYWORDS:
        text = re.sub(rf"\b{term}\b", f"SCAM_{term}", text, flags=re.IGNORECASE)
    return text

def load_model():
    global model__,common_pidgin_slang
    try:
        with open("model_/scam_model.plk","rb") as f:
            model__ = pickle.load(f)
        with open("common_slangs.json","r") as f:
            common_pidgin_slang = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: Could not find one of the required files: {e}")
    except Exception as e:
        print(f"Error loading mode:{e}")

if __name__ == "__main__":
    load_model()