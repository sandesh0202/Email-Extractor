import os
import re
import pandas as pd
from pdfminer.high_level import extract_text

pdf_directory = "path_to_your_pdf_folder"
emails = []
email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

def extract_emails_from_pdf(pdf_path):
    try:
        text = extract_text(pdf_path)
        found_emails = re.findall(email_pattern, text)
        return found_emails
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return []

for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, filename)
        extracted_emails = extract_emails_from_pdf(pdf_path)
        for email in extracted_emails:
            emails.append({"Filename": filename, "Email": email})

df = pd.DataFrame(emails)
df.to_csv("extracted_emails.csv", index=False)
