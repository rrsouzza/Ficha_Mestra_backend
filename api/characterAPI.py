import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore, db
from google.cloud.firestore_v1.base_query import FieldFilter

db = firestore.client()
characters_Ref = db.collection('characters')

charactersAPI = Blueprint('charactersAPI', __name__)


@charactersAPI.route('/add', methods=['POST'])
def create():
  try:
    id = uuid.uuid4()
    body = request.json
    new_id = id.hex
    
    characters_Ref.document(new_id).set(body)
    body.id = new_id

    return jsonify({"success": True, "data": body}), 200
  except Exception as e:
    return f"An Error Occured: {e}"


@charactersAPI.route('/get-by-character/<id_character>', methods=['GET'])
def get(id_character):
  try:
    doc_ref = characters_Ref.where(filter = FieldFilter("id", "==", id_character)).stream()
    return jsonify({"data": doc_ref}), 200
  except Exception as e:
    return f"An Error Occurred: {e}"


@charactersAPI.route('/get-by-user/<id_user>', methods=['GET'])
def get_by_user(id_user):
  try:
    docs_ref = characters_Ref.where(filter = FieldFilter("user", "==", id_user)).stream()
    items = {}
    for doc in docs_ref:
      items.update({doc.id : doc.to_dict()})
    return jsonify({"data": items}), 200
  except Exception as e:
    return f"An Error Occured: {e}"
  

@charactersAPI.route('/put/<id_character>', methods=['PUT'])
def put(id_character):
  try:
    character = characters_Ref.document(id_character)
    body = request.json

    character.update(body)

    return jsonify({"success": True, "data": character}), 200
  except Exception as e:
    return f"An Error Occured: {e}"


@charactersAPI.route('/delete/<id_character>', methods=['DELETE'])
def delete(id_character):
  try:
    characters_Ref.document(id_character).delete()
    return jsonify({"success": True, }), 200
  except Exception as e:
    return f"An Error Occured: {e}"
  
# -------------------- #

# @userAPI.route('/pesquisa-fichas/<id_conta>/<pesquisa>', methods=['GET'])
# def pesquis_ficha(id_conta, pesquisa):
#   try:
#     filter_1 = FieldFilter("Nome_jogador", "==", pesquisa)
#     filter_2 = FieldFilter("Nome_Personagem", "==", pesquisa)

#     or_filter = Or(filters=[filter_1,filter_2]) #https://firebase.google.com/docs/firestore/query-data/queries?hl=pt-BR#or_queries

#     docs_ref = (db.collection("Fichas").where(filter=FieldFilter("Id_conta", "==", id_conta)).where(filter=or_filter).stream())
#     arquivos = {}
#     for doc in docs_ref:
#       arquivos.update({doc.id : doc.to_dict()})
#     return jsonify({"arquivos": arquivos}), 200
#   except Exception as e:
#     return f"An Error Occured: {e}"