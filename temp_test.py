# # from models.pdf import PdfModel
import re
from pathlib import Path
import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

folder_path = Path("C:", "/", "repositories", "pdfs_for_crawler", "file_2.pdf")
phone_pattern_regex = r"([0-9]{3})[-.]?([0-9]{3})[-.]?([0-9]{4})"


def convert_pdf_to_txt(path):
    resource_manager = PDFResourceManager()
    retstr = io.StringIO()
    laparams = LAParams()
    device = TextConverter(resource_manager, retstr, laparams=laparams)
    file_path = open(path, 'rb')
    interpreter = PDFPageInterpreter(resource_manager, device)
    password = ""
    max_pages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(file_path, pagenos, maxpages=max_pages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    file_path.close()
    device.close()
    text = retstr.getvalue()
    retstr.close()
    return text


file_as_string = convert_pdf_to_txt(str(folder_path))
print(file_as_string)

matches = re.findall(phone_pattern_regex, file_as_string)
phones = [''.join(match) for match in matches] # not converting to int since this would remove the preceding 0
print(phones)
