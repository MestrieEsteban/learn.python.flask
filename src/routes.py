from flask import request, jsonify
from sqlalchemy import create_engine
import json


def postCar():
    fields = ['car_brand', 'car_model', 'car_power']
    if not all(k in request.form for k in fields):
        return jsonify({'error': 'Missing field in request'}), 200
    data = request.form
    car_brand = data['car_brand']
    car_model = data['car_model']
    car_power = data['car_power']
    engine = create_engine('sqlite:///cars.sqlite')
    conn = engine.connect()
    try:
        conn.execute("INSERT INTO cars (brand, model, power) VALUES (?, ?, ?)",(car_brand, car_model, car_power))
        return jsonify({'success': 'Car added'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error adding car'}), 200
    finally:
        conn.close()

    return jsonify({'message': 'Car created successfully'})

def getCars():
    engine = create_engine('sqlite:///cars.sqlite')
    conn = engine.connect()
    try:
        cars = conn.execute("SELECT * FROM cars").fetchall()
        if cars:
            return {'results': [dict(zip(tuple(cars[0].keys()), row)) for row in cars]}   
        else:
            return jsonify({'error': 'No cars found'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error getting cars'}), 200
    finally:
        conn.close()

def getCar(id):
    engine = create_engine('sqlite:///cars.sqlite')
    conn = engine.connect()
    try:
        car = conn.execute("SELECT * FROM cars WHERE id = ?",(id,)).fetchone()
        if car:
            return {'results': [dict(zip(tuple(car.keys()), car))]}   
        else:
            return jsonify({'error': 'No car found'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error getting car'}), 200
    finally:
        conn.close()

def putCar(id):
    fields = ['car_brand', 'car_model', 'car_power']
    if not all(k in request.form for k in fields):
        return jsonify({'error': 'Missing field in request'}), 200
    data = request.form
    car_brand = data['car_brand']
    car_model = data['car_model']
    car_power = data['car_power']
    engine = create_engine('sqlite:///cars.sqlite')
    conn = engine.connect()
    try:
        conn.execute("UPDATE cars SET brand = ?, model = ?, power = ? WHERE id = ?",(car_brand, car_model, car_power, id))
        return jsonify({'success': 'Car updated'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error updating car'}), 200
    finally:
        conn.close()

def deleteCar(id):
    engine = create_engine('sqlite:///cars.sqlite')
    conn = engine.connect()
    try:
        conn.execute("DELETE FROM cars WHERE id = ?",(id,))
        return jsonify({'success': 'Car deleted'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error deleting car'}), 200
    finally:
        conn.close()

def postOrder:
    fields = ['car_id', 'customer_id', 'order_price']
    if not all(k in request.form for k in fields):
        return jsonify({'error': 'Missing field in request'}), 200
    data = request.form
    car_id = data['car_id']
    customer_id = data['customer_id']
    order_price = data['order_price']
    order_status = 'pending'
    created_at = datetime.now()
    engine = create_engine('sqlite:///cars.sqlite')
    conn = engine.connect()
    try:
        conn.execute("INSERT INTO orders (car_id, customer_id, price, status, created_at) VALUES (?, ?, ?, ?, ?)",(car_id, customer_id, order_price, order_status, created_at))
        return jsonify({'success': 'Order added'}), 200
