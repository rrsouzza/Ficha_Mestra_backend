import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore, db
from google.cloud.firestore_v1.base_query import FieldFilter, Or

db = firestore.client()
mesas_Ref = db.collection('mesas')

mesaAPI = Blueprint('mesaAPI', __name__)


@mesaAPI.route('/add', methods=['POST'])
def create():
  try:
    id = uuid.uuid4()
    body = request.json

    mesas_Ref.document(id.hex).set(body)
    return jsonify({"success": True, "data": body}), 200
  except Exception as e:
    return f"An Error Occured: {e}"

  
@mesaAPI.route('/get/<id>', methods=['GET'])
def get(id_mesa):
  try:
    doc_ref = db.collection("mesas").where(filter = FieldFilter("id", "==", id_mesa)).stream()
    return jsonify({"data": doc_ref}), 200
  except Exception as e:
    return f"An Error Occurred: {e}"


@mesaAPI.route('/get/<id_user>', methods=['GET'])
def get_by_user(id_user):
  try:
    filter_1 = FieldFilter("id_mestre", "==", id_user)
    filter_2 = FieldFilter("id_jogadores", "array_contains", id_user)

    or_filter = Or([filter_1,filter_2])

    docs_ref = (db.collection("mesas").where(filter = or_filter).stream())
    
    items = {}
    for doc in docs_ref:
      items.update({doc.id : doc.to_dict()})

    return jsonify({"data": items}), 200
  except Exception as e:
    return f"An Error Occured: {e}"
  

@mesaAPI.route('/put/<id_mesa>', methods=["PUT"])
def put(id_mesa):
  try:
    mesa_ref = mesas_Ref.document(id_mesa)
    body = request.json

    mesa_ref.update(body)
    return jsonify({"success": True, "data": body}), 200
  except Exception as e:
    return f"An Error Occured: {e}"
  

@mesaAPI.route('/delete/<id_mesa>', methods=['DELETE'])
def delete(id_mesa):
  try:
    mesas_Ref.document(id_mesa).delete()
    return jsonify({"success": True}), 200
  except Exception as e:
    return f"An Error Occured: {e}"
  
# --------------------- #

# @userAPI.route('/pesquisa-mesas/<id_jogador>/<pesquisa>', methods=['GET'])
# def pesquisa_mesa(id_jogador, pesquisa):
#   try:
#     filter_1 = FieldFilter("Nome_mesa", "==", pesquisa)
#     filter_2 = FieldFilter("Tipo_da_Mesa", "==", pesquisa)

#     filter_3 = FieldFilter("Id_Mestre", "==", id_jogador)
#     filter_4 = FieldFilter("Id_Jogadores", "array_contains", id_jogador)

#     or_filter = Or([filter_1,filter_2])
#     or_filter_validador = Or([filter_3,filter_4])

#     docs_ref = (db.collection("Mesa").where(filter=or_filter_validador).where(filter= or_filter).stream()) #https://firebase.google.com/docs/firestore/query-data/queries?hl=pt-BR#compound_and_queries
#     arquivos = {}
#     for doc in docs_ref:
#       arquivos.update({doc.id : doc.to_dict()})
#     return jsonify({"arquivos": arquivos}), 200
#   except Exception as e:
#     return f"An Error Occured: {e}"
