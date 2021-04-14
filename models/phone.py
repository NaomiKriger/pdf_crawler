from .pdf import PdfModel
from ..db import db


class PhoneModel(db.Model):
    __tablename__ = 'phones'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.Integer)  # same phone number can appear in
    # TODO: 1) check if there's a way to create a list. 2) make query syntax correct
    pdfs = db.Column(db.varchar, foreign_key=PdfModel.id.filter(phone == phone_number for phone in PdfModel.phones))

    def extract_phone_from_pdf(self, pdf):
        pass
