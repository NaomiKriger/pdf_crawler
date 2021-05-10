from collections import defaultdict

from flask import request
from flask_restful import Resource

from models.all_models import PhoneModel


class Phone(Resource):

    @classmethod
    def get(cls, phone):
        phone = PhoneModel.find_by_phone(phone)
        if phone:
            return phone.json()
        return {'message': f'pdf {phone} was not found'}, 404

    @classmethod
    def post(cls, phone):
        if PhoneModel.find_by_name(phone):
            return {'message': f'pdf {phone} already exists'}
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
    def delete(cls, phone):
        phone = PhoneModel.find_by_phone(phone)
        if not phone:
            return {'message': f'phone {phone} was not found'}, 404
        phone.delete_from_db()
        return {'message': f'phone {phone} deleted'}, 201


class PhoneList(Resource):

    @classmethod
    def get(cls):
        result = defaultdict(list)
        phones = [phone for phone in PhoneModel.query.all()]  # PhoneModel[index] // PhoneModel.query.all()[index]
        for phone in phones:
            pdf_names = [pdf.name for pdf in phone.pdfs]
            result[phone.phone_number].extend(pdf_names)
        return result


# TODO: remember - defaultdict & enumerate

'''
{
'123': ('pdf1', 'pdf2', 'pdf3'),
'145': ('pdf4', 'pdf2', 'pdf6')
}
'''
