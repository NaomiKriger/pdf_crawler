from flask_restful import Resource
from flask_restful import reqparse
from sqlalchemy.exc import NoResultFound

from db import db
from models.documentation_example import Parent, Child


class Documentation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phones',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    @classmethod
    def get(cls, name):
        # parent = Parent.find_by_name(name)
        parent = Parent.query.filter_by(name=name)
        if parent:
            return parent.json()
        return {'message': f'parent {name} was not found'}, 404

    @classmethod
    def post(cls, name):
        # p = Parent.query.filter_by(name=name).one()
        # if p:
        #     print(p)
        #     return {'parent': 'exists'}
        try:
            parent = Parent.query.filter_by(name=name).one()
            # return {'message': f'pdf {name} already exists'}
        except NoResultFound:
            parent = Parent()
            parent.name = name
            child = Child()
            parent.children.append(child)
            db.session.add(child)
            db.session.add(parent)
            db.session.commit()
            return parent.name, 201

        # data = Documentation.parser.parse_args()
        # pdf = Parent(name, data['phones'])

        try:
            parent.save_to_db()
        except:
            return {'message': 'an error occurred'}, 500
        return {'message': f'pdf {name} already exists'}
        # return pdf.json(), 201
