import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore, db
from google.cloud.firestore_v1.base_query import FieldFilter

db = firestore.client()
fichas_Ref = db.collection('fichas')

fichaAPI = Blueprint('fichaAPI', __name__)


@fichaAPI.route('/add', methods=['POST'])
def create():
  try:
    id = uuid.uuid4()
    body = request.json
    new_id = id.hex
    
    fichas_Ref.document(new_id).set(body)
    body.id = new_id

    return jsonify({"success": True, "data": body}), 200
  except Exception as e:
    return f"An Error Occured: {e}"


@fichaAPI.route('/get/<id>', methods=['GET'])
def get(id_ficha):
  try:
    doc_ref = db.collection("fichas").where(filter = FieldFilter("id", "==", id_ficha)).stream()
    return jsonify({"data": doc_ref}), 200
  except Exception as e:
    return f"An Error Occurred: {e}"


@fichaAPI.route('/get/<id_user>', methods=['GET'])
def get_by_user(id_user):
  try:
    docs_ref = db.collection("fichas").where(filter = FieldFilter("user", "==", id_user)).stream()
    items = {}
    for doc in docs_ref:
      items.update({doc.id : doc.to_dict()})
    return jsonify({"data": items}), 200
  except Exception as e:
    return f"An Error Occured: {e}"
  

@fichaAPI.route('/put/<id_ficha>',methods=['PUT'])
def put(id_ficha):
  try:
    ficha = fichas_Ref.document(id_ficha)
    body = request.json

    ficha.update(body)

    return jsonify({"success": True, "data": ficha}), 200
  except Exception as e:
    return f"An Error Occured: {e}"


@fichaAPI.route('/delete/<id_ficha>', methods=['DELETE'])
def delete(id_ficha):
  try:
    fichas_Ref.document(id_ficha).delete()
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