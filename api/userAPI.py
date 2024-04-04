import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore, auth, db
from google.cloud.firestore_v1.base_query import FieldFilter, Or, And

db = firestore.client() # Não está servindo para nada 
user_Ref_Mesa = db.collection('Mesa')


# Site para pesquisa da criação de usuários https://blog.rocketseat.com.br/desenvolvendo-aplicacoes-web-com-flask/
# 

userAPI = Blueprint('userAPI', __name__)

@userAPI.route('/add', methods=['POST'])
def create():
  #return f"Nome: {body.get('name')}\n Email: {body.get('email')} \n Senha: {body.get('password')}"
  try:
    # id = uuid.uuid4()
    # user_Ref.document(id.hex).set(request.json)
    # return jsonify({"success": True}), 200
    body = request.json

    print("body: ", body)

    user = auth.create_user(
      display_name = body.get('name'),
      email = body.get('email'),
      password = body.get('password'),
    )
    return jsonify({ "success": True, "user": body }), 200 # Não dá para retorna o user porque não é um JSON por isso reotrnei o body
  except Exception as e:
    return f"An Error Occured: {e}"

#  Referencias para criar usuários banco https://firebase.google.com/docs/database/admin/save-data?hl=pt-br  --> Salvar dados

  
@userAPI.route('/pesquisa-fichas/<id_conta>/<pesquisa>', methods=['GET'])
def pesquis_ficha(id_conta, pesquisa):
  try:
    filter_1 = FieldFilter("Nome_jogador", "==", pesquisa)
    filter_2 = FieldFilter("Nome_Personagem", "==", pesquisa)

    or_filter = Or(filters=[filter_1,filter_2]) #https://firebase.google.com/docs/firestore/query-data/queries?hl=pt-BR#or_queries

    docs_ref = (db.collection("Fichas").where(filter=FieldFilter("Id_conta", "==", id_conta)).where(filter=or_filter).stream())
    arquivos = {}
    for doc in docs_ref:
      arquivos.update({doc.id : doc.to_dict()})
    return jsonify({"arquivos": arquivos}), 200
  except Exception as e:
    return f"An Error Occured: {e}"
  
@userAPI.route('/pesquisa-mesas/<id_jogador>/<pesquisa>', methods=['GET'])
def pesquisa_mesa(id_jogador, pesquisa):
  try:
    filter_1 = FieldFilter("Nome_mesa", "==", pesquisa)
    filter_2 = FieldFilter("Tipo_da_Mesa", "==", pesquisa)

    filter_3 = FieldFilter("Id_Mestre", "==", id_jogador)
    filter_4 = FieldFilter("Id_Jogadores", "array_contains", id_jogador)

    or_filter = Or([filter_1,filter_2])
    or_filter_validador = Or([filter_3,filter_4])

    docs_ref = (db.collection("Mesa").where(filter=or_filter_validador).where(filter= or_filter).stream()) #https://firebase.google.com/docs/firestore/query-data/queries?hl=pt-BR#compound_and_queries
    arquivos = {}
    for doc in docs_ref:
      arquivos.update({doc.id : doc.to_dict()})
    return jsonify({"arquivos": arquivos}), 200
  except Exception as e:
    return f"An Error Occured: {e}"