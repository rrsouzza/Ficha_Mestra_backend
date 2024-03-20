from flask import Flask, jsonify, render_template, request, redirect, url_for
import urllib.request, json
#from flask_sqlalchemy import SQLAlchemy
import requests
import json
# stepper


#pip install requests
#pip install url_fot
#pip install 


app = Flask(__name__)

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fichamestre.bd"


#db = SQLAlchemy(app)
app.app_context().push()

link_banco = "https://tccfichas-default-rtdb.firebaseio.com/"

list_login = ""
Todos_arquivos = {}
final = {}
teste = "te"

Id_usuario_Login = [] # Armazena o Id do usuário

def criar_mesa(): # Criar a função para armazenar as fichas no bando de dados
    return redirect(url_for('pagina_inicial'))
    pass

# Eviando dados do JSON para a tela de criação das fichas
@app.route('/dados-fichas',methods=["GET"])
def enviarDados(): # Criar a função para criar as mesas no bando de dados
    arquivo = open("dicionario_RPG.json", "r", encoding='utf-8')
    return arquivo


@app.route('/', methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form.get("login") and request.form.get("senha"):
            id_usuarios = requests.get(f'{link_banco}/Usuario/.json').json()
            for id_user in id_usuarios:
                if (id_usuarios[id_user]["Nome"] == request.form.get("login")) or (id_usuarios[id_user]["Email"] == request.form.get("login")):
                    if id_usuarios[id_user]["Senha"] == request.form.get("senha"):
                        Id_usuario_Login.append(id_user)
                        return redirect(url_for('pagina_inicial'))
                    else:
                       return render_template("index.html", ativar="Login Incorreto1")
                else:
                    return render_template("index.html", ativar="Login Incorreto2")
        else:
            return render_template("index.html", ativar="Login Incorreto3")
    return render_template("index.html")

@app.route('/cadastro', methods=["GET","POST"])
def cadastro():
    if request.method == "POST":
        if request.form.get("nome") and request.form.get("senha"):
            list_login = {"Nome": request.form.get("nome"), "Senha": request.form.get("senha"), "Email": request.form.get("email"),"Aniversario": request.form.get("aniversario")}
            requisicao = requests.post(f'{link_banco}/Usuario/.json', data=json.dumps(list_login))
            return redirect(url_for('login'))

    return render_template("cadastro.html")

@app.route('/pagina_inicial', methods=["GET","POST"])
def pagina_inicial():
    mesas_Jogador = []
    mesas_Mestre = []
    requisicao_mesas = requests.get(f'{link_banco}/Mesa/.json').json()
    for id_mesa in requisicao_mesas:
        if requisicao_mesas[id_mesa]['Mestre'] != str(Id_usuario_Login[0]):
            for jogadores in  requisicao_mesas[id_mesa]['Jogadores']:
                if jogadores == str(Id_usuario_Login[0]):
                    mesas_Jogador.append(requisicao_mesas[id_mesa])
        else:
            mesas_Mestre.append(requisicao_mesas[id_mesa])
    
    with open("dicionario_RPG.json", encoding='utf-8') as arquivos:
        dados = json.load(arquivos)

    for i in dados:
        Todos_arquivos.update(i)

    return render_template("pagina_inicial.html",dados= Todos_arquivos, mesas_Mestre = mesas_Mestre, mesas_Jogador = mesas_Jogador)


@app.route('/criar_ficha_D&D', methods=["GET","POST"])
def criar_ficha_DeD():
    pass


@app.route('/hello-world', methods=["GET"])
def helloworld():
    arry = jsonify({'Olá': 'mundo','Teste':"teste mensagem"})
    arry.headers.add('Access-Control-Allow-Origin', '*')
    return arry


if __name__ =="__main__":
    app.run(debug=True)