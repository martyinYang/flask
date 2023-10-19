from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://nexxera:dev123@localhost:3306/petshop'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Model
class Pets(db.Model):
   __tablename__ = "pets"
   id = db.Column(db.Integer, primary_key=True)
   nome = db.Column(db.String(60))
   idade = db.Column(db.String(3))
   raca = db.Column(db.String(60))
   cor = db.Column(db.String(60))

   def create(self):
       db.session.add(self)
       db.session.commit()
       return self

   def __init__(self, nome, idade, raca, cor):
       self.nome = nome
       self.idade = idade
       self.raca = raca
       self.cor = cor

   def __repr__(self):
       return f"{self.id}"

class PetsSchema(ma.Schema):
   class Meta(ma.Schema.Meta):
       model = Pets
       sqla_session = db.session
   id = fields.Number(dump_only=True)
   nome = fields.String(required=True)
   idade = fields.String(required=True)
   raca = fields.String(required=True)
   cor = fields.String(required=True)

@app.route('/api/v1/pets', methods=['POST'])
def create_pets():
    data = request.get_json()
    pets_schema = PetsSchema()
    pet = Pets(**data)
    db.session.add(pet)
    db.session.commit()
    result = pets_schema.dump(pet)
    return make_response(jsonify({"pets": result}), 200)

@app.route('/api/v1/pets', methods=['GET'])
def index():
   get_pets = Pets.query.all()
   pets_schema = PetsSchema(many=True)
   pets = pets_schema.dump(get_pets)
   return make_response(jsonify({"pets": pets}))

@app.route('/api/v1/pets/<id>', methods=['GET'])
def get_pets_by_id(id):
   get_pet = Pets.query.get(id)
   pets_schema = PetsSchema()
   pet = pets_schema.dump(get_pet)
   return make_response(jsonify({"pet": pet}))

@app.route('/api/v1/pets/<id>', methods=['PUT'])
def update_pet_by_id(id):
   data = request.get_json()
   get_pets = Pets.query.get(id)
   if data.get('nome'):
       get_pets.nome = data['nome']
   if data.get('idade'):
       get_pets.idade = data['idade']
   if data.get('raca'):
        get_pets.raca = data['raca']
   if data.get('cor'):
       get_pets.cor = data['cor']
   db.session.add(get_pets)
   db.session.commit()
   pets_schema = PetsSchema(only=['id', 'titnomele', 'idade', 'raca', 'cor'])
   pets = pets_schema.dump(get_pets)

   return make_response(jsonify({"pets": pets}))

@app.route('/api/v1/pets/<id>', methods=['DELETE'])
def delete_pets_by_id(id):
   get_pets= Pets.query.get(id)
   db.session.delete(get_pets)
   db.session.commit()
   return make_response("", 204)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
