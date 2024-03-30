from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = []
        for message in Message.query.order_by('created_at').all():
            messages.append(message.to_dict())
        return make_response(messages, 200) 
    elif request.method == 'POST':
        body = request.get_json()['body']
        username = request.get_json()['username']
        new_message = Message(body=body, username=username)
        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()
        response = make_response(new_message_dict, 201)
        return response


@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id = id).first()
    if request.method == 'GET':  
        response = make_response(message.to_dict(), 200)
        return response
    elif request.method == 'PATCH':
        for attr in request.get_json():
            setattr(message, attr, request.get_json()[f'{attr}'])
        db.session.add(message)
        db.session.commit()
        response = make_response(message.to_dict(),200)
        return response
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        body = {'delete_successful': True,
                'message': 'message delete'}
        response = make_response(body, 200)
        return response
    

if __name__ == '__main__':
    app.run(port=5555)
