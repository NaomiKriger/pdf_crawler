import io
import re
from pathlib import Path

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from db import db

folder_path = Path("C:", "/", "repositories", "pdfs_for_crawler", "file_2.pdf")
phone_pattern_regex = r"([0-9]{3})[-.]?([0-9]{3})[-.]?([0-9]{4})"

association_table = db.Table('association', db.Model.metadata,
                             db.Column('pdfs_id', db.Integer, db.ForeignKey('pdfs.id')),
                             db.Column('phones_id', db.Integer, db.ForeignKey('phones.id'))
                             )


class PdfModel(db.Model):
    __tablename__ = 'pdfs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    phones = db.relationship("PhoneModel", secondary=association_table, backref='pdfs')

    def __init__(self, name, phones):
        self.name = name
        self.phones = phones

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        for phone in self.phones:
            pdfs = phone.pdfs
            if len(pdfs) == 1 and pdfs[0].name == self.name:
                db.session.delete(phone)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def pdfs_by_phones(cls, phone):
        return cls.query.filter_by(phone in cls.phones).all()  # TODO: resolve this

    def json(self):
        return {'name': self.name, 'phones': [str(p) for p in self.phones]}

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

    @staticmethod
    def extract_phones_from_pdf(pdf_path):
        pdf_text = PdfModel.convert_pdf_to_txt(pdf_path)

        matches = re.findall(phone_pattern_regex, pdf_text)
        phones = [''.join(match) for match in matches]
        return phones

    # def save_phone_in_pdf_to_db(self, pdf_path):
    #     phones = self.extract_phones_from_pdf(pdf_path)
    #     for phone in phones:
    #         db.session.add(phone)
    #     db.session.commit()


class PhoneModel(db.Model):
    __tablename__ = 'phones'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone_number = db.Column(db.String)

    def __init__(self, phone_number):
        self.phone_number = phone_number

    def __str__(self):
        return f'<PhoneModel - {self.phone_number}>'

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, phone):
        return cls.query.filter_by(phone=phone).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def find_pdfs(self):
        return self.query.filter_by(phone_number=self.phone_number).all()
