from sqlalchemy.orm import relationship

from db import db

association_table = db.Table('association', db.Model.metadata,
                             db.Column('left_id', db.Integer, db.ForeignKey('left.id')),
                             db.Column('right_id', db.Integer, db.ForeignKey('right.id')),
                             extend_existing=True
                             )


class Parent(db.Model):
    __tablename__ = 'left'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    children = relationship("Child",
                            secondary=association_table)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Child(db.Model):
    __tablename__ = 'right'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
