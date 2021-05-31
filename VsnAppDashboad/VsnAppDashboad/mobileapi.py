from VsnAppDashboad import app, db
from flask import Flask
from VsnAppDashboad.models import Session, Imageslink


@app.route('/create_session', methods=['POST'])
def create_session():
    folder_name = request.form.get('folder_name')

    session = Session.query.filter_by(googleFolder=folder_name).first()

    if not session:
        new_session = Session(googleFolder=folder_name)
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

