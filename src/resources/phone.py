from collections import defaultdict

from flask import request
from flask_restful import Resource

from src.models.all_models import PhoneModel


class Phone(Resource):

    @classmethod
    def get(cls, phone) -> tuple:
        phone_object = PhoneModel.find_by_phone(phone)
        if phone_object:
            return phone_object.json()
        return {'message': f'phone {phone} was not found'}, 404

    @classmethod
    def post(cls, phone) -> tuple:
        if PhoneModel.find_by_name(phone):
            return {'message': f'pdf {phone} already exists'}, 400
        data = request.get_json()
        pdfs = [PhoneModel(pdf) for pdf in data['pdfs']]
        print('data = ', data)
        print(f'pdfs = {[str(p) for p in pdfs]}')
        pdf = PhoneModel(phone)

        try:
            pdf.save_to_db()
        except Exception as e:
            print(e)
            return {'message': 'an error occurred'}, 500
        return pdf.json(), 201

    @classmethod
    def delete(cls, phone) -> tuple:
        phone = PhoneModel.find_by_phone(phone)
        if not phone:
            return {'message': f'phone {phone} was not found'}, 404
        phone.delete_from_db()
        return {'message': f'phone {phone} deleted'}, 201


class PhoneList(Resource):

    @classmethod
    def get(cls) -> dict:
        result = defaultdict(list)
        phones = [phone for phone in PhoneModel.query.all()]
        for phone in phones:
            pdf_names = [pdf.name for pdf in phone.pdfs]
            result[phone.phone_number].extend(pdf_names)
        for phone_key in result:
            result[phone_key] = sorted(result[phone_key])
        return result
