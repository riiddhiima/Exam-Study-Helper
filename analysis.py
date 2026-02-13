import re
from collections import Counter
import os

def get_top_repeated_questions(subject, top_n=5):
    path = fr"D:\Study\Projects\contextAG\data\combined_subjects\{subject}_combined.txt"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Clean headers and boilerplate
    text = re.sub(r"(KIIT[\s\S]{0,100}Examination-\d{4})", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Candidates are required[\s\S]*?(?=\n)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Answer any[\s\S]*?(?=\n)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"SECTION-[A-Z][\s\S]*?(?=\n)", "", text, flags=re.IGNORECASE)

    # Extract actual questions (e.g., numbered or lettered)
    questions = re.findall(r"(?:\(?[0-9]{1,2}\)?[\.\)]\s+.*?)(?=\n|$)", text)
    sub_questions = re.findall(r"\([a-h]\)\s+.*?(?=\n|$)", text, flags=re.IGNORECASE)

    all_qs = questions + sub_questions
    cleaned_qs = [q.strip() for q in all_qs if 10 < len(q.strip()) < 300 and "examination" not in q.lower()]

    counter = Counter(cleaned_qs)
    return [q for q, _ in counter.most_common(top_n)]
