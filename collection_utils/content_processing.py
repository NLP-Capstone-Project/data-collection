import os
import requests
import re
import sys

import textract


def extract_pdf_content(pdfUrl):
    """
    Given the url of a publication, strips the raw content from the
    PDF and returns it as a byte string.

    Returns None if the paper content couldn't be found.
    """

    # Collect PDF and store a temporary version.
    temp_pdf_path = "/tmp/publication.pdf"

    # Request fails for some urls; return None in this case.
    try:
        response = requests.get(pdfUrl)
    except:
        return None

    # Not all of the PDFs are extractable through a single get request.
    if not response.headers['content-type'] == 'application/pdf':
        return None

    paper_tmp = open(temp_pdf_path, 'wb')
    paper_tmp.write(response.content)

    # Extract text from the temp. PDF.
    text = textract.process(temp_pdf_path)

    return text


def clean_pdf_content(content):
    """
    Given the raw content of a publication pdf, filters out
    special characters, references, and other minutia and leaves
    behind only semantic content.

    Cuts out as much non-semantic content as possible (e.g. references,
    special characters, etc.).

    :param content: byte string
    :return
    """
    clean_text = content

    # Remove unicode characters
    clean_text = clean_text.decode('utf-8').encode('ascii', 'ignore')

    # Convert to string
    clean_text = str(clean_text)

    # Remove straggling hex digits
    clean_text = re.sub(r'\\x[a-zA-Z0-9]', ' ', clean_text)

    # Remove references (MUST DO THIS BEFORE REMOVING NEWLINE CHARS)
    # Assumes that bibliography always follows "References" or
    # "Acknowledgements" with a line break after it.
    if "Acknowledgements\\n" in clean_text:
        clean_text = clean_text.split("Acknowledgements\\n")[0]
    elif "References\\n" in clean_text:
        clean_text = clean_text.split("References\\n")[0]

    # Replace escaped newline characters
    clean_text = re.sub(r'\\n', '\n', clean_text)

    # Remove references with years (ex. (Boundless et al., 2006))
    match = r'\([^()]*\)'
    clean_text = re.sub(match, ' ', clean_text)

    return clean_text


def main():
    if len(sys.argv) < 2:
        print("I need the url of a research paper!")
        sys.exit()

    pdfUrl = sys.argv[1]

    print("Before:")
    raw_content = extract_pdf_content(pdfUrl)
    print(raw_content)

    print("After:")
    clean_content = clean_pdf_content(raw_content)
    print(clean_content)

    print("Lengths in words:\n Before: {}\n, After: {}"
          .format(len(str(raw_content).split()), len(clean_content.split())))

    print("Tokenized:", )


if __name__ == "__main__":
    main()
