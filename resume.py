import re
import json
import PyPDF2
import csv
import os

def extract_text_and_links_from_pdf(pdf_path):
    text = ""
    links = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        pages = len(reader.pages)
        for page_num in range(pages):
            page = reader.pages[page_num]
            text += page.extract_text()
            
            if '/Annots' in page:
                for annot in page['/Annots']:
                    obj = annot.get_object()
                    if '/A' in obj and '/URI' in obj['/A']:
                        links.append(obj['/A']['/URI'])
    
    return text, links

def extract_phone_numbers(text):
    phone_pattern = re.compile(r'\b(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b')
    return phone_pattern.findall(text)

def extract_emails(text):
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    return email_pattern.findall(text)

def extract_linkedin_profiles(text, links):
    linkedin_patterns = [
        r'https?://(?:www\.)?linkedin\.com/in/[\w-]+/?',
        r'https?://(?:www\.)?linkedin\.com/pub/[\w-]+(?:/[\w-]+){0,3}/?',
        r'https?://(?:www\.)?linkedin\.com/profile/view\?id=\d+',
        r'linkedin\.com/in/[\w-]+',
        r'linkedin\.com/pub/[\w-]+(?:/[\w-]+){0,3}'
    ]
    linkedin_regex = re.compile('|'.join(linkedin_patterns), re.IGNORECASE)
    profiles_from_text = linkedin_regex.findall(text)
    profiles_from_links = [link for link in links if linkedin_regex.search(link)]
    return list(set(profiles_from_text + profiles_from_links))

def load_skills(file_path):
    with open(file_path, 'r') as file:
        skills = json.load(file)
    return [skill.lower() for skill in skills]  # Convert all skills to lowercase

def extract_skills(text, skills_list):
    text_lower = text.lower()
    found_skills = set()
    
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills.add(skill)
    
    return list(found_skills)

def process_pdf(pdf_path, skills_list):
    text, links = extract_text_and_links_from_pdf(pdf_path)
    
    phone_numbers = extract_phone_numbers(text)
    emails = extract_emails(text)
    linkedin_profiles = extract_linkedin_profiles(text, links)
    found_skills = extract_skills(text, skills_list)
    
    return {
        'File': os.path.basename(pdf_path),
        'Phone Numbers': '; '.join(phone_numbers),
        'Emails': '; '.join(emails),
        'LinkedIn Profiles': '; '.join(linkedin_profiles),
        'Skills': '; '.join(found_skills)
    }

def main(pdf_folder, skills_file_path, output_csv):
    skills_list = load_skills(skills_file_path)
    
    results = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            result = process_pdf(pdf_path, skills_list)
            results.append(result)
    
    # Write results to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File', 'Phone Numbers', 'Emails', 'LinkedIn Profiles', 'Skills']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    print(f"Results have been written to {output_csv}")


if __name__ == "__main__":
    pdf_path = "Files"
    skills_file_path = "combined_skills.json"
    output_csv = "extracted_info.csv"
    main(pdf_path, skills_file_path, output_csv)