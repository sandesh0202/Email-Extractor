# PDF Information Extractor

This Python script extracts useful information such as phone numbers, email addresses, LinkedIn profiles, and specific skills from PDF files and outputs them into a CSV file. It utilizes `PyPDF2` for extracting text and hyperlinks from PDFs, regular expressions (`re`) for pattern matching, and basic file handling for processing multiple PDFs in a directory.

## Features

1. **Extract Text from PDF**: Extracts all the text and hyperlinks from each page of a PDF.
2. **Extract Phone Numbers**: Searches for and extracts phone numbers in various formats.
3. **Extract Emails**: Identifies and extracts valid email addresses from the text.
4. **Extract LinkedIn Profiles**: Detects LinkedIn profile URLs from both the text and hyperlinks.
5. **Extract Skills**: Matches skills from a predefined list (stored in a JSON file) against the text in the PDF.
6. **Output to CSV**: Generates a CSV file containing the extracted information.

## Requirements

Ensure you have the following Python libraries installed:

- `PyPDF2`
- `re` (Regular Expressions - built-in module)
- `json` (built-in module)
- `csv` (built-in module)
- `os` (built-in module)

Install PyPDF2 via pip:

```bash
pip install PyPDF2
```

## How to Use

1. **Set up the PDF folder**: Place all your PDF files in a folder. The script will process all PDFs in this folder.
2. **Prepare the Skills JSON File**: Prepare a JSON file that contains a list of skills. The JSON file should be in the following format:

```json
[
    "Python",
    "JavaScript",
    "Machine Learning",
    ...
]
```

3. **Run the Script**: Execute the script with the following parameters:
    - `pdf_folder`: The folder containing the PDF files.
    - `skills_file_path`: The path to the JSON file containing the list of skills.
    - `output_csv`: The name of the CSV file where the extracted data will be stored.

For example:

```bash
python script.py /path/to/pdf_folder /path/to/skills_file.json output.csv
```

## Script Breakdown

### 1. **extract_text_and_links_from_pdf(pdf_path)**
   - Extracts the text and hyperlinks from the PDF file at `pdf_path`.
   - Returns two items: `text` (the extracted text) and `links` (the extracted hyperlinks).

### 2. **extract_phone_numbers(text)**
   - Uses regular expressions to search for phone numbers in different formats in the extracted text.

### 3. **extract_emails(text)**
   - Finds email addresses in the extracted text using regular expressions.

### 4. **extract_linkedin_profiles(text, links)**
   - Extracts LinkedIn profile URLs from both the extracted text and links.
   - Uses a list of regular expressions to identify different LinkedIn URL patterns.

### 5. **load_skills(file_path)**
   - Loads a list of skills from a JSON file, converts all skills to lowercase for case-insensitive matching.

### 6. **extract_skills(text, skills_list)**
   - Matches skills from the list in the extracted text.
   - Returns a list of found skills.

### 7. **process_pdf(pdf_path, skills_list)**
   - Extracts all the relevant information from a single PDF file, including phone numbers, emails, LinkedIn profiles, and matched skills.

### 8. **main(pdf_folder, skills_file_path, output_csv)**
   - Processes all PDF files in the `pdf_folder`, extracts the information, and writes the results to a CSV file (`output_csv`).

## Example Output CSV

The output CSV will have the following structure:

| File            | Phone Numbers     | Emails                 | LinkedIn Profiles                        | Skills                  |
|-----------------|-------------------|------------------------|------------------------------------------|-------------------------|
| resume1.pdf     | 123-456-7890      | john@example.com        | https://www.linkedin.com/in/johndoe      | Python, JavaScript      |
| resume2.pdf     | 555-123-4567      | jane@example.com        | linkedin.com/in/janedoe                 | Machine Learning, Java  |
| ...             | ...               | ...                    | ...                                      | ...                     |

## Important Notes

- **PDF Structure**: The script works best with text-based PDFs. It may not perform well on PDFs that consist of scanned images.
- **Skill Matching**: The skill matching is case-insensitive and based on exact word matches.

## License

This project is licensed under the MIT License.

