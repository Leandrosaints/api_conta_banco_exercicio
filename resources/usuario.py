

from flask_restful import Resource, reqparse
from models.usuario import ClientModel, UserModel
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required,get_jwt, get_jwt_identity, )
from flask import jsonify
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

#class que resgistra os admi
#/User/{user_id}
class UseRegister(Resource):
    #atributos das class
    atributos = reqparse.RequestParser()
    #atributos.add_argument('user_id', type=str)
    atributos.add_argument('login', type=str, required=True, help='o campo login nao pode estar em branco')
    atributos.add_argument('senha', type=str, required=True, help='campo senha nao pode esta em branco')
    atributos.add_argument('email', type=str,  help="pfv add um email ao campo requerido")
    atributos.add_argument('ativado', type=bool)
    #busca os dados dos adm 
    #/user/{user_id}
    @jwt_required()
    def get(self, user_id):
        user = UserModel.find_user(user_id)

        if user:
            return user.json()#usar a func da class 'usermodel' para return em json
        return {'menssage': 'cliente nao encontrado'}, 404

    #criar os adm
    #/user/{user_id}
    def post(self, user_id):
        #usa a func da class abaixo para ver o numeros de linhas dados slv no bd
        id = UserModel.find_user_quant(user_id) #Adm.atributos.parse_args
        if id:
            if id >= 2:#se id for maior ou igual a 2, nao cria outro adm
                return {'message':'nao e possivel criar mais adm'}
        
        dados = UseRegister.atributos.parse_args()#pega os atribu da class 
        
        user = UserModel(user_id, **dados)#desempacota os atr e insere no bd
        user.save_user()

        return {'messager':'usuario adm criado'}
        '''        except:
                    return {'message':'nao pode ser criado'}, 500'''

    @jwt_required(fresh=True)
    def put(self, user_id):
        dados = UseRegister.atributos.parse_args()
        id_user = UserModel.find_user(user_id)
        if id_user:
            id_user.update_user(**dados)
            id_user.save_user()
            return {'message':'user atualizado'}
        try:
            user = ClientModel(user_id, **dados)
            user.save_user()
        except:
            
            return {'message':'erro ao tentar criar'}, 500
        return user.json(), 201
    #deleta os adm
    #/user/{user_id}
    @jwt_required(fresh=True)#login requerid
    def delete(self, user_id):
       

        id = UserModel.find_user_quant(user_id)
        if id <= 1:# nao exluir o adm se o numero de rows for menor que 1
            return {'message':'nao e possivel exluir o adm, pois so exite um salvo'}
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message':'user deleted'}
        return {'message':'nao foi possivel detelar'}, 500

#rota de cadstro cliente
#/cliente/{user_id}
class Usercliente(Resource):
    novos_args = UseRegister.atributos.copy()#cria uma copia dos atr da class 

    @jwt_required()
    def get(self, user_id):
        users = ClientModel.find_user(user_id)
        if users:
            return users.json()
        return {'message':f"usuario '{user_id}', nao encontrado"}
    #o parametro fresh so aceita o token que possui as credenciais senha e login corretas/ou seja o so sera acessado se o token nao for o refresh_token ou token atualizado
    @jwt_required(fresh=True)
    def post(self, user_id):
        if ClientModel.find_user(user_id):
            return {'message':f"o cliente '{user_id}',ja exites"}
    
        Usercliente.novos_args.add_argument('cont_n', type=str, required=True)
        Usercliente.novos_args.add_argument('saldo', type=str, required=True, default=0)
        Usercliente.novos_args.remove_argument('ativado')
        dados = Usercliente.novos_args.parse_args()
        user = ClientModel(user_id, **dados)
        user.save_user()
        return {'messager':'usuario cliente criado'}
    
    @jwt_required(fresh=True)
    def put(self, user_id):
      
        '''#dados = Usercliente.novos_args.parse_args()
        #args = reqparse.RequestParser()
        #args.add_argument('cont_n', type=str, required=True)
        #args.add_argument('saldo', type=str, required=True)
        #dados = args.parse_args()'''
        Usercliente.novos_args.add_argument('cont_n', type=str, required=True)
        Usercliente.novos_args.add_argument('saldo', type=str, required=True)
        dados = Usercliente.novos_args.parse_args()
        id_user = ClientModel.find_user(user_id)
        if id_user:
            id_user.update_user(**dados)
            id_user.save_user()
            return {'message':'user atualizado'}
        try:
            user = ClientModel(user_id, **dados)
            user.save_user()
            #return {'message':f"novo cliente '{user_id}' criado"}
        except:
            
            return {'message':'erro ao tentar criar'}, 500
        return user.json(), 201

    @jwt_required(fresh=True)
    def delete(self, user_id):
        

        user = ClientModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message':'user deleted'}
        return {'message':'erro ao tentar deletar'},500
'''class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)

        if user:
            return user.json()
        return {'menssage': 'cliente nao encontrado'}, 404'''
#Rota login cliente
#/cliente/login
class LoginClient(Resource):
    @classmethod
    def post(cls):
        dados = Usercliente.novos_args.parse_args()
        user = ClientModel.find_by_login(dados['login'])
        #
        if user and safe_str_cmp(user.senha, dados['senha']):
            return {'message':'login sucessuful'},200
            #token_de_acesso = create_access_token(identity=user.user_id) 
            #return {'access_token':token_de_acesso}, 200
            #return {'message':'user not confirmed.'}, 400

        return {'message':'o nome ou senha esta incorreto.'},401#nao autorizado

#rota de 
#/login
class UserLogin(Resource):
    
    @classmethod
    def post(cls):
       

        dados = UseRegister.atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])
        #
        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id, fresh=True)
            refresh_token = create_refresh_token(user.user_id) 
            
            return {'access_token':token_de_acesso,
                    'refresh_token':refresh_token
                    }, 200
                #refresh token token para atualizar o token de acesso
                
            #return {'message':'user not confirmed.'}, 400

        return {'message':'o nome ou senha esta incorreto.'},401#nao autorizado



#Class que atualizar o token de acesso
#/refrsh_token
class TokenRefresh(Resource):
    @jwt_required(refresh=True)#reque o token de refresh criado na hora do login
    def post(self):
        current_user = get_jwt_identity()#pega o id atual do jwt passado no token
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_new_token':new_token},200

#rota de deslogar 
#/logout
class Logout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']#'jti' vai pegar o id do jwt
        BLACKLIST.add(jwt_id)
        return {'message':'deslogado com sucesso!'}, 200
