from flask import Flask
from flask_restful import Api

# from resources.documentation_example import Documentation
from db import db
from resources.pdf import Pdf, PdfList
from resources.phone import PhoneList

app = Flask(__name__)
app.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite://data.sb'
app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


# TODO: resolve the warning for the decorator below
# @jwt.user_claims_loader
# def add_claims_to_jwt(identity):
#     if identity == 1: # instead of hard coding, should read from a config file or a database
#         return {'is_admin': True}
#     return {'is_admin': False}

api.add_resource(Pdf, '/pdf/<string:name>')
api.add_resource(PdfList, '/pdfs')
api.add_resource(PhoneList, '/phones')

# api.add_resource(Documentation, '/parents/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)
