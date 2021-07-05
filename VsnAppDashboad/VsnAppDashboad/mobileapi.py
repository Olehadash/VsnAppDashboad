from VsnAppDashboad import app, db
from flask import Flask, request, jsonify
from VsnAppDashboad.models import Session, Imageslink
from datetime import datetime

@app.route('/create_session', methods=['POST'])
def create_session():
    folder_name = request.form.get('folder_name')
    license_number = request.form.get('car_number')
    date_of_check = datetime.strptime(request.form.get('date_of_check'), '%Y-%m-%d_%H-%M-%S')
    garage_name = request.form.get('garage_name')
    apriser_name = request.form.get('apriser_name')
    garage_phone = request.form.get('garage_phone')

    session = Session.query.filter_by(googleFolder=folder_name).first()

    if not session:
        new_session = Session(googleFolder=folder_name, garage_name = garage_name, license_number = license_number, date_of_check = date_of_check, apriser_name = apriser_name, garage_phone=garage_phone)
        db.session.add(new_session)
        db.session.commit()
        return jsonify (msg = "Success"),200

    return jsonify (msg = "Allreaddy exist"),200


@app.route('/add_session', methods=['POST'])
def add_session():
    image_link = request.form.get('image_link')
    folder_name = request.form.get('folder_name')

    session = Session.query.filter_by(googleFolder=folder_name).first()

    if not session:
        return jsonify (msg = "Session not Exist"), 402
    
    imag = Imageslink.query.filter_by(link = image_link).first()

    if not imag:
        imag_new = Imageslink(link = image_link)
        db.session.add(imag_new)
        session.images.append(imag_new)
        db.session.commit()
        return jsonify (msg = "Success"),200

    return jsonify (msg = "Allreaddy exist"),200

