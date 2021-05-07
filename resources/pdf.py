from flask import request
from flask_restful import Resource

from models.all_models import PdfModel, PhoneModel


class Pdf(Resource):

    @classmethod
    def get(cls, name):
        pdf = PdfModel.find_by_name(name)
        if pdf:
            return pdf.json()
        return {'message': f'pdf {name} was not found'}, 404

    @classmethod
    def post(cls, name):
        if PdfModel.find_by_name(name):
            return {'message': f'pdf {name} already exists'}
        data = request.get_json()
        phone_numbers = [PhoneModel(phone_number) for phone_number in data['phones']]
        print('data = ', data)
        print(f'phone_numbers = {[str(p) for p in phone_numbers]}')
        # print(f'phone_numbers = {[p.__str__() for p in phone_numbers]}')
        pdf = PdfModel(name, phone_numbers)

        try:
            pdf.save_to_db()
        except Exception as e:
            print(e)
            return {'message': 'an error occurred'}, 500
        return pdf.json(), 201
        # return 'created', 201

    @classmethod
    def delete(cls, name):
        pdf = PdfModel.find_by_name(name)
        if not pdf:
            return {'message': f'pdf {name} was not found'}, 404
        pdf.delete_from_db()
        return {'message': f'pdf {name} deleted'}, 201


class PdfList(Resource):

    @classmethod
    def get(cls):
        pdfs = [pdf.json() for pdf in PdfModel.find_all()]
        return {'pdf list': [pdf for pdf in pdfs]}
