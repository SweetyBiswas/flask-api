# from datetime import datetime
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from flask import current_app
from my_app import db



class Student(db.Model):
    
    s_no = db.Column(db.Integer, primary_key=True,unique=True)
    name = db.Column(db.String(100), nullable=False)
    username=db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), unique=False,nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())


    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    #     return s.dumps({'s_no': self.s_no}).decode('utf-8')


    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         s_no = s.loads(token)['s_no']
    #     except:
    #         return None
    #     return Student.query.get(s_no)





# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     public_id = db.Column(db.String(50), unique=True)
#     name = db.Column(db.String(50))
#     password = db.Column(db.String(80))
#     admin = db.Column(db.Boolean)
  