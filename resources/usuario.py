from email.policy import default
import json

from flask_restful import Resource, reqparse
from models.usuario import ClientModel, UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp

'''class Adm():
    
    atributos = reqparse.RequestParser()
    #atributos.add_argument('user_id', type=str)
    atributos.add_argument('login', type=str, required=True, help='o campo login nao pode estar em branco')
    atributos.add_argument('senha', type=str, required=True, help='campo senha nao pode esta em branco')
    atributos.add_argument('email', type=str)

    def __init__(self,login, senha, email):
        #self.user_id = user_id
        self.login = login
        self.senha = senha
        self.email = email'''
    
'''class Cliente(Adm):
    def __init__(self, login, senha, email, cont_n, saldo):
        super().__init__(login, senha, email)
        self.cont_n = cont_n
        self.saldo = saldo
        novos_atr = Adm.atributos.copy()
       
        novos_atr.add_argument(f'{self.cont_n}')
        novos_atr.add_argument(f'{self.saldo}')'''
    
class UseRegister(Resource):
    
    atributos = reqparse.RequestParser()
    #atributos.add_argument('user_id', type=str)
    atributos.add_argument('login', type=str, required=True, help='o campo login nao pode estar em branco')
    atributos.add_argument('senha', type=str, required=True, help='campo senha nao pode esta em branco')
    atributos.add_argument('email', type=str)
    
    def post(self, user_id):
        
        if UserModel.find_user(user_id): #Adm.atributos.parse_args

            return {'message':'nao e possivel criar mais adm'}
        
        dados = UseRegister.atributos.parse_args()
        
        user = UserModel(user_id, **dados)
        user.save_user()

        return {'messager':'usuario adm criado'}
        '''        except:
                    return {'message':'nao pode ser criado'}, 500'''    
    
class Usercliente(Resource):
    
    @jwt_required()
    def post(self, user_id):
        if ClientModel.find_cliente(user_id):
            return {'message':f"o cliente '{user_id}',ja exites"}
       
        novos_args = UseRegister.atributos.copy() 
        #novos_args.add_argument('login', type=str, required=True)
        #novos_args.add_argument('senha', type=str, required=True, unique=True)
        #novos_args.add_argument('email', type=str, required=True, unique=True)
        novos_args.add_argument('cont_n', type=str, required=True)
        novos_args.add_argument('saldo', type=str, required=True, default=0)
        dados = novos_args.parse_args()
        user = ClientModel(user_id, **dados)
        user.save_user()
        return {'messager':'usuario cliente criado'}
    def get(self, user_id):
        users = ClientModel.find_cliente(user_id)
        if users:
            return users.json()
        return {'message':f"usuario {user_id}"}
class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)

        if user:
            return user.json()
        return {'menssage': 'cliente nao encontrado'}, 404
'''class UserCliente(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('login', type=str, required=True, help='o campo login nao pode estar em branco')
    atributos.add_argument('senha', type=str, required=True, help='campo senha nao pode esta em branco')
    atributos.add_argument('email', type=str)
    atributos.add_argument('cont_n', type=str, required=True, help='o cmp')
    atributos.add_argument('saldo', type=str)

   
    def post(self, user_id):
        
        if ClientModel.find_cliente(user_id):
            return {'message':f'o cliente {user_id} ja existe'}
        else:
            dados = UserCliente.atributos.parse_args()
        
            user = ClientModel(user_id,**dados)

            user.save_user()

            return {'messager':'usuario cliente criado'}

    def get(self, user_id):
        user = ClientModel.find_cliente(user_id)

        if user:
            return user.json()
        return {'menssage': 'cliente nao encontrado'}, 404'''
class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = UseRegister.atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])
        #
        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id) 
            return {'access_token':token_de_acesso}, 200
            #return {'message':'user not confirmed.'}, 400

        return {'message':'o nome ou senha esta incorreto.'},401#nao autorizado