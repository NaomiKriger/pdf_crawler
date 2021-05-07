# import io
# import re
#
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.pdfpage import PDFPage
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql.sqltypes import ARRAY, String
# from sqlalchemy import PickleType, types
# from sqlalchemy.dialects.postgresql import ARRAY
#
# from db import db
# from models import association_table
#
# phone_pattern_regex = r"([0-9]{3})[-.]?([0-9]{3})[-.]?([0-9]{4})"
#
#
# '''
# methods to set the column to a list:
# 1) phones = db.Column(MutableList.as_mutable(ARRAY(String(100))), default=[])
# 2) PickleType
# 3) create a separate table
# 4) use a concatenated string
# '''
#
#
# class PdfModel(db.Model):
#
#     __tablename__ = 'pdfs'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80))
#     phones = relationship("PhoneModel", secondary=association_table, backref="pdfs")
#     foreign_keys = [association_table.c.phones_id, association_table.c.pdfs_id]
#
# def __init__(self, name, phones):
#     self.name = name
#     self.phones = phones
#
#     def json(self):
#         return {'id': self.id,
#                 'name': self.name,
#                 'phones': self.phones}
#
#     @classmethod
#     def find_all(cls):
#         return cls.query.all()
#
#     @classmethod
#     def find_by_name(cls, name):
#         return cls.query.filter_by(name=name).first()
#
#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()
#
#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()
#
#     @staticmethod
#     def convert_pdf_to_txt(path):
#         resource_manager = PDFResourceManager()
#         retstr = io.StringIO()
#         laparams = LAParams()
#         device = TextConverter(resource_manager, retstr, laparams=laparams)
#         file_path = open(path, 'rb')
#         interpreter = PDFPageInterpreter(resource_manager, device)
#         password = ""
#         max_pages = 0
#         caching = True
#         pagenos = set()
#
#         for page in PDFPage.get_pages(file_path, pagenos, maxpages=max_pages,
#                                       password=password,
#                                       caching=caching,
#                                       check_extractable=True):
#             interpreter.process_page(page)
#
#         file_path.close()
#         device.close()
#         text = retstr.getvalue()
#         retstr.close()
#         return text
#
#     @staticmethod
#     def extract_phones_from_pdf(pdf_path):
#         pdf_text = PdfModel.convert_pdf_to_txt(pdf_path)
#
#         matches = re.findall(phone_pattern_regex, pdf_text)
#         phones = [''.join(match) for match in matches]
#         return phones
#
#     def save_phone_in_pdf_to_db(self, pdf_path):
#         phones = self.extract_phones_from_pdf(pdf_path)
#         for phone in phones:
#             db.session.add(phone)
#         db.session.commit()
#
#
# class PhoneModel(db.Model):
#     __tablename__ = 'phones'
#
#     id = db.Column(db.Integer, primary_key=True)
#     phone_number = db.Column(db.Integer)
#     # pdfs = relationship("PdfModel", secondary=association_table, backref="phones")
#
#     def __init__(self, name, phone_number, pdfs):
#         self.name = name
#         self.phone_number = phone_number
#         self.pdfs = pdfs
#
#     def json(self):
#         return {'id': self.id,
#                 'phone_number': self.phone_number,
#                 'pdfs': self.pdfs}
#
#     @classmethod
#     def find_all(cls):
#         return cls.query.all()
#
#     def extract_phone_from_pdf(self, pdf):
#         pass
