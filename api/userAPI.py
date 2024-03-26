import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore, auth

db = firestore.client()
# user_Ref = db.collection('user')

userAPI = Blueprint('userAPI', __name__)

@userAPI.route('/add', methods=['POST'])
def create():
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