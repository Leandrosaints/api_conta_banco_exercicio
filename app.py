from flask import Flask

from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.usuario import  UseRegister,UserLogin, Usercliente, LoginClient

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def criarbanco():
    banco.create_all()

api.add_resource(UseRegister, '/user/<int:user_id>')
#api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Usercliente, '/cliente/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(LoginClient, '/cliente/login')
if __name__=="__main__":
    from sql_alchemy import banco
    banco.init_app(app)
    app.run()
