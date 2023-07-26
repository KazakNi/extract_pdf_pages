from pypdf import PdfReader, PdfWriter
from pypdf._page import PageObject
import configparser

config = configparser.ConfigParser()
config.read(".cfg")
merger = PdfWriter()

def reading(filename: str) -> list[PageObject]:
    reader = PdfReader(filename)
    pages = reader.pages
    return pages

def check_keywords(text: str, keyword: str) -> bool:
    text = text.lower()
    if keyword.lower() in text:
        return True
    return False

def get_relevant_pages(pages: list[PageObject], filter_: str) -> list[int]:
    final_pages = []
    length = len(pages)
    for p_number in range(0, length, 3):
        text = pages[p_number].extract_text()
        print(p_number)
        if not check_keywords(text, filter_):
            print(f'writing.....{p_number}')
            final_pages.append(p_number)
    return final_pages

def merging(filename, page_numbers) -> None:
    merged_file = open(filename, "rb")
    merger.append(fileobj=filename, pages=page_numbers)
    output = open(f"result_{filename}.pdf", "wb")
    merger.write(output)
    merger.close()
    output.close()
    merged_file.close()

def main():
    filename = config["PDF"]["file2"]
    pages = reading(filename)
    page_numbers = get_relevant_pages(pages, "liquid")
    merging(filename, page_numbers)

if __name__ == '__main__':
    main()