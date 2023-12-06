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

@app.route('/')
def home():
    return '<h1>Home<h1>'

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    msgs = Message.query.order_by(Message.created_at).all()

    if request.method == 'GET':
        msg_list = [m.to_dict() for m in msgs]
        return make_response(msg_list, 200)
    
    elif request.method == 'POST': 
        new_msg = Message(
            body=request.get_json()["body"],
            username=request.get_json()["username"]
        )
        db.session.add(new_msg)
        db.session.commit()

        msg_dict = new_msg.to_dict()

        return make_response(msg_dict, 201)
        

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    msg = Message.query.filter(Message.id == id).first()

    if request.method == 'PATCH':
        for attr in request.get_json():
            setattr(msg, attr, request.get_json().get(attr))

        db.session.add(msg)
        db.session.commit()

        msg_dict = msg.to_dict()

        return make_response(msg_dict, 200)
    
    elif request.method == 'DELETE':
        db.session.delete(msg)
        db.session.commit()


if __name__ == '__main__':
    app.run(port=5555)
