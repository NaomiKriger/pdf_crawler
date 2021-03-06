from flask import Flask
from flask_restful import Api

from db import db
from src.resources.pdf import Pdf, PdfList
from src.resources.phone import Phone, PhoneList

app = Flask(__name__)
app.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite://data.sb'
app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Pdf, '/pdf/<string:name>')
api.add_resource(Phone, '/phone/<string:phone>')
api.add_resource(PdfList, '/pdfs')
api.add_resource(PhoneList, '/phones')


if __name__ == '__main__':
    app.run()
