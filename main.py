import flask
import src.routes as routes
# from flask_cors import CORS

import sqlalchemy as db
from sqlalchemy.orm import declarative_base, relationship

engine = db.create_engine('sqlite:///cars.sqlite')
connection = engine.connect()
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    orders = relationship('Order', backref='customer', lazy=True)
    def __init__(self, address, phone, email):
        self.address = address
        self.phone = phone
        self.email = email
    def __repr__(self):
        return '<Customer %r>' % self.address

class Order(Base):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))  
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    status = db.Column(db.Enum('pending', 'complete', 'cancelled'))
    created_at = db.Column(db.DateTime)
    def __init__(self, customer_id, car_id, status, created_at):
        self.customer_id = customer_id
        self.car_id = car_id
        self.status = status
        self.created_at = created_at
    def __repr__(self):
        return '<Order %r>' % self.id
class Car(Base):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String)
    model = db.Column(db.String)
    power = db.Column(db.Integer)
    def __init__(self, brand, model, power):
        self.brand = brand
        self.model = model
        self.power = power
    def __repr__(self):
        return '<Car %r>' % self.id

Base.metadata.create_all(engine)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# CORS(app, origins='*', 
#      headers=['Content-Type', 'Authorization'], 
#      expose_headers='Authorization')

app.add_url_rule('/api/cars', 'getCars', routes.getCars, methods=['GET'])
app.add_url_rule('/api/cars', 'postCar', routes.postCar, methods=['POST'])
app.add_url_rule('/api/cars/<int:id>', 'getCar', routes.getCar, methods=['GET'])
app.add_url_rule('/api/cars/<int:id>', 'putCar', routes.putCar, methods=['PUT'])
app.add_url_rule('/api/cars/<int:id>', 'car', routes.deleteCar, methods=['DELETE'])


app.run()