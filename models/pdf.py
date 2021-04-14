import io
import re

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from .phone import PhoneModel
from ..db import db

phone_pattern_regex = re.compile(".*?(\(?\d{3})? ?[\.-]? ?\d{3} ?[\.-]? ?\d{4}.*?", re.S)


class PdfModel(db.Model):

    __tablename__ = 'pdfs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    phones = []  # temp - list or set of all phone numbers that appear in the PDF
    # TODO: 1) check if there's a way to create a list. 2) make query syntax correct
    # phones = db.Column(db.Integer, foreign_key=PhoneModel.pdfs.all() in id)

    def __init__(self, name, phones):
        self.name = name
        self.phones = phones

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'phones': self.phones}

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def find_by_name(self):
        return self.query.filter_by(name=self.name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
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

    def extract_phones_from_pdf(self, pdf_path):
        pdf_text = PdfModel.convert_pdf_to_txt(pdf_path)

        """this method crawls over the PDF and returns a list / set of all the phone numbers found in it"""
        if 'a' == 1:  # temp logic to remove PyCharm warning
            b = self.phones
        return []

    def save_phone_in_pdf_to_db(self, pdf_path):
        phones = self.extract_phones_from_pdf(pdf_path)
        for phone in phones:
            db.session.add(phone)
        db.session.commit()
