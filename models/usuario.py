
import sqlite3
from flask import request, url_for

from sql_alchemy import banco
class ClientModel(banco.Model):
    __tablename__ = 'clientes'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    cont_n = banco.Column(banco.Integer, nullable=False, unique=True)
    saldo = banco.Column(banco.Integer, nullable=False)
    
    def __init__(self, user_id, login, senha, email, cont_n, saldo):
        self.user_id = user_id
        self.login = login
        self.senha = senha
        self.email = email
        self.cont_n = cont_n
        self.saldo = saldo

    def json(self):

        return {
            'user_id':self.user_id,
            'login':self.login,
            'senha':self.senha,
            'email':self.email,
            'cont_n':self.cont_n,
            'saldo':self.saldo
        }
    @classmethod
    def find_by_login(cls, login):#essa func vai ser um classmethod, por isso nao herda self
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def update_user(self, login, senha, email, cont_n, saldo):
        self.login = login
        self.senha = senha
        self.email = email
        self.cont_n = cont_n
        self.saldo = saldo

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
    
    
    @classmethod 
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None
class UserModel(banco.Model):
    __tablename__ = 'usuarios'
    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False )
    senha = banco.Column(banco.String(40), nullable=False, unique=True)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)
    def __init__(self,user_id, login, senha, email, ativado):
        self.user_id = user_id
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado
    def json(self):

        return {
            'user_id':self.user_id,
            'login':self.login,
            'senha':self.senha,
            'email':self.email,
            'ativado':self.ativado
            
        }
    @classmethod
    def find_user_quant(cls, id):
        
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM usuarios WHERE ('{id}')")
        count = len(cursor.fetchall())

        if count:
            return count
        conn.close()

    @classmethod 
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None
    @classmethod
    def find_by_email(cls, email):
        email = cls.query.filter_by(email=email).first()
        if email:
            return email
        return None
    
    
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()
    
    
    def update_user(self, nome, senha, email):
        self.nome = nome
        self.senha = senha
        self.email = email
        


    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()