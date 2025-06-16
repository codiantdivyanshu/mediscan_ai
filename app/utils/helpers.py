# app/utils/helpers.py

import re
from typing import Optional
from datetime import datetime

def clean_text(text: str) -> str:
    text = text.replace("\n", " ").replace("\r", " ")
    return re.sub(r"\s+", " ", text).strip()

def extract_first_match(pattern: str, text: str, flags=0) -> Optional[str]:
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else None

def extract_all_matches(pattern: str, text: str, flags=0) -> list:
    return re.findall(pattern, text, flags)

def normalize_date(date_str: str) -> Optional[str]:
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None

