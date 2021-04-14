from .pdf import PdfModel
from ..db import db


class PhoneInPdfModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.Integer)
    pdf_id = db.Column(db.Integer, foreign_key=PdfModel.id)
