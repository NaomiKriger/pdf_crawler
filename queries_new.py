# from flask import Flask
# from db import db
# from models.all_models import PdfModel
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'My connection string'
# db.init_app(app)
#
# with app.app_context():
#     db.create_all()
#
# PdfModel.query.limit(5).all()
