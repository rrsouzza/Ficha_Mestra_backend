import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore, db, auth
from google.cloud.firestore_v1.base_query import FieldFilter

db = firestore.client()
characters_Ref = db.collection('characters')

charactersAPI = Blueprint('charactersAPI', __name__)

@charactersAPI.after_request
def after_request(response):
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Methods'] = '*'
  response.headers['Access-Control-Allow-Headers'] = '*'
  return response

@charactersAPI.route('/add/<id_user>', methods=['POST', 'OPTIONS'])
def create(id_user):
  try:
    user = auth.get_user(id_user)
    print('user: ', user)
  except Exception as e:
    return jsonify({ "success": False, "message": "Usuário inexistente" }), 401
  
  try:
    id = uuid.uuid4()
    body = request.json
    new_id = id.hex

    body["user"] = id_user
    body["id"] = new_id
    characters_Ref.document(new_id).set(body)

    return jsonify({ "success": True, "data": body }), 200
  except Exception as e:
    return f"An Error Occured: {e}"


@charactersAPI.route('/get-by-character/<id_character>', methods=['GET'])
def get(id_character):
  try:
    doc_ref = characters_Ref.where(filter = FieldFilter("id", "==", id_character)).stream()
    return jsonify({ "data": doc_ref }), 200
  except Exception as e:
    return f"An Error Occurred: {e}"


@charactersAPI.route('/get-by-user/<id_user>', methods=['GET'])
def get_by_user(id_user):
  try:
    docs_ref = characters_Ref.where(filter = FieldFilter("user", "==", id_user)).stream()
    items = []
    for doc in docs_ref:
      items.append(doc.to_dict())
    return jsonify({ "data": items }), 200
  except Exception as e:
    return f"An Error Occured: {e}"
  

@charactersAPI.route('/put/<id_character>', methods=['PUT'])
def put(id_character):
  try:
    # character = characters_Ref.where(filter = FieldFilter("id", "==", id_character)).stream()
    body = request.json

    characters_Ref.document(id_character).set(body, merge = True)

    return jsonify({ "success": True, "data": body }), 200
  except Exception as e:
    print("e: ------- 1\n", e)
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