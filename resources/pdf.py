from flask import request
from flask_restful import Resource

from models.all_models import PdfModel, PhoneModel


class Pdf(Resource):

    @classmethod
    def get(cls, name) -> tuple:
        pdf = PdfModel.find_by_name(name)
        if pdf:
            return pdf.json()
        return {'message': f'pdf {name} was not found'}, 404

    @classmethod
    def post(cls, name) -> tuple:
        data = request.get_json()
        path = data['path']
        if PdfModel.find_by_name(name):
            return {'message': f'pdf {name} already exists'}, 400

        phones_from_pdf = PdfModel.extract_phones_from_pdf(path)
        phone_numbers = [PhoneModel(phone_number) for phone_number in phones_from_pdf]
        pdf = PdfModel(name, phone_numbers)

        try:
            pdf.save_to_db()
        except Exception as e:
            print(e)
            return {'message': 'an error occurred'}, 500
        return pdf.json(), 201

    @classmethod
    def delete(cls, name) -> tuple:
        pdf = PdfModel.find_by_name(name)
        if not pdf:
            return {'message': f'pdf {name} was not found'}, 404
        pdf.delete_from_db()
        return {'message': f'pdf {name} deleted'}, 201


class PdfList(Resource):

    @classmethod
    def get(cls) -> dict:
        pdfs = [pdf.json() for pdf in PdfModel.find_all()]
        sorted_pdfs_list = sorted([pdf for pdf in pdfs], key=lambda k: k['name'])
        return {'pdf list': sorted_pdfs_list}
