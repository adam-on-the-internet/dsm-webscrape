import os.path

import fitz  # this is pymupdf

from models.Generic.PDFExtraction import PDFExtraction
from util import request_util


def write_file_by_sections(path, title, sections):
    file = open(path, "w")
    file.write("# " + title)
    file.write("\n\n")
    for section in sections:
        write_section(file, section)
    file.close()


def write_section(file, section):
    if len(section.lines) > 0:
        file.write("## " + section.title)
        file.write("\n\n")
        for line in section.lines:
            file.write(line)
            file.write("\n")
        file.write("\n\n")


def does_path_exist(path):
    return os.path.exists(path)


def make_directory_if_not_exists(path):
    if not does_path_exist(path):
        os.makedirs(path)


def download_file_locally(download_url, destination_file):
    print(f"     * Downloading file...")
    content = request_util.get_online_file_contents(download_url)
    write_file(content, destination_file)


def write_file(content, destination_file):
    with open(destination_file, 'wb') as f:
        f.write(content)


def convert_pdf_to_plaintext(pdf_filename, plaintext_filename, title):
    # extract all information from the PDF
    pdf_extraction = extract_pdf(pdf_filename)

    # handle text
    text = get_start_text(title)
    text = text + pdf_extraction.text
    text = text + get_end_text()

    # handle links
    text = text + "\n\n---- LINKS START ----\n\n"
    for link in pdf_extraction.links:
        text = text + link + "\n"
    text = text + "\n\n---- LINKS END ----\n\n"

    # write a copy
    if plaintext_filename is not None:
        write_plaintext_doc(plaintext_filename, text)

    return text


def extract_pdf(pdf_filename):
    text = ""
    links = []
    with fitz.open(pdf_filename) as doc:
        page_index = 1
        for page in doc:

            # extract text
            if page_index == 1:
                text = text + get_page_break(page_index)
            text = text + page.get_text()
            page_index = page_index + 1
            text = text + get_page_break(page_index)

            # extract links
            links = links + page.get_links()

    # cleanup links
    unique_links = get_unique_links(links)

    return PDFExtraction(text, unique_links)


def get_page_break():
    return get_page_break(None)


def get_page_break(page_number):
    page_number_piece = ""
    if page_number_piece is not None:
        page_number_piece = " " + str(page_number) + " ----\n"
    return "\n---- PAGE BREAK ----" + page_number_piece


def get_start_text(title):
    title_piece = ""
    if title is not None:
        title_piece = "---- TITLE: " + title + " ----\n\n"
    return title_piece + "---- DOCUMENT START ----\n\n"


def get_end_text():
    return "\n---- DOCUMENT END ----\n"


def get_unique_links(all_links):
    unique_links = []
    for link in all_links:
        if "uri" in link and link['uri'] not in unique_links:
            uri = link['uri']
            unique_links.append(uri)
    return unique_links


def write_plaintext_doc(filename, text):
    document = open(filename, "w")
    document.write(text)
    document.close()
