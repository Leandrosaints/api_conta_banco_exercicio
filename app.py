from flask import Flask, jsonify
from config import Config_token
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.usuario import  Logout, TokenRefresh, UseRegister, UserLogin, Usercliente, LoginClient
from blacklist import BLACKLIST
from datetime import timedelta

app = Flask(__name__)
app.config.from_object('config')
app.config.from_object(Config_token())#forma de chamar a class do config.py acessando assim as config passada

api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def criarbanco():
    banco.create_all()




@jwt.token_in_blocklist_loader
def verificar_blacklist(self, token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader#token revogado
def token_invalidado(jwt_header, jwt_payload):
   
    return jsonify({'message':'voce foi deslogado.'}), 401

api.add_resource(UseRegister, '/user/<int:user_id>')
api.add_resource(Usercliente, '/cliente/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/token_refresh')
api.add_resource(Logout, '/logout')
api.add_resource(LoginClient, '/cliente/login')
if __name__=="__main__":
    from sql_alchemy import banco
    banco.init_app(app)
    app.run()
