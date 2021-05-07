# from sqlalchemy.orm import relationship
#
# from . import association_table
# from .pdf import PdfModel
# from ..db import db
#
#
# class PhoneModel(db.Model):
#     __tablename__ = 'phones'
#
#     id = db.Column(db.Integer, primary_key=True)
#     phone_number = db.Column(db.Integer)
#     pdfs = relationship("PdfModel", secondary=association_table, back_populates="phones")
#
#     def extract_phone_from_pdf(self, pdf):
#         pass
