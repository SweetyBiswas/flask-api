# from crypt import methods
from flask import jsonify,request, Blueprint,Flask,Request,make_response,session,render_template
# from student.main import func
from my_app.model.student import Student
# from student import app
from my_app import db,bcrypt
import jwt
from my_app import func
from functools import wraps
from datetime import datetime,timedelta
from flask import  current_app
from my_app.helpers.user import *
from flask_mail import *
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# import psycopg2
# conn = psycopg2.connect("dbname=sweety user=postgres password=sweety123")
# cursor = conn.cursor()

# main=Blueprint('main',__name__)
main = Blueprint('main', __name__)
from flask import Flask, flash, render_template, request, redirect


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try: 
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            #current_user = Student.query.filter_by(s_no=data['s_no']).first()
            s_no=data['s_no']
            current_user=student_for_s_no(s_no)

        

        except Exception as e:
            return str(e)
        # except:
        #     return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

        # except jwt.ExpiredSignatureError:
        #     msg = 'Token expired. Get new one'
        #     return msg
        # except jwt.DecodeError:
        #     msg = 'Error decoding signature.'
        #     return msg
        # except jwt.InvalidTokenError:
        #     return 'Invalid Token.'
        # except Exception as e:
        #     return str(e)

  
@main.route('/register', methods=['POST'])
def register():
    ''' This is the register api.'''
    request_data = request.get_json()
    x=func.register_student(request_data)
    return str(x)    

@main.route('/fetch_student', methods=['POST'])
@token_required
def fetch_student(current_user):
    ''' This is the api for fetch student details,which is secure using JWT Token,user can only fetch student details if user has valid token'''
    if not current_user.name:
        return jsonify({'message' : 'Cannot perform that function!'})   
    else:
        request_data = request.get_json()
        x=func.fetch_student_details(request_data)
        return x


@main.route('/modify_student', methods=['POST']) # for calling the API from Postman/SOAPUI
@token_required
def modify_student(current_user):
    ''' This is the api for modify student address if student email id known ,only if valid token provided'''
    if not current_user.name:
        return jsonify({'message' : 'Cannot perform that function!'})    
    else:
        request_data = request.get_json()
        x=func.modify_user(request_data)
        return x


@main.route('/login', methods=['POST']) # for calling the API from Postman
@token_required
def student_login(current_user):
    ''' For login student need to privide email id and password '''
    if not current_user.name:
        return jsonify({'message' : 'Cannot perform that function!'})   
    else:
        request_data = request.get_json()
        x=func.login_student(request_data)
        return str(x)


        
@main.route('/change_password', methods=['POST']) 
@token_required
def change_password(current_user):
    ''' This is api for change password . To change the password student need to privide email id ,correct password and the new password'''
    if not current_user.name:
        return jsonify({'message' : 'Cannot perform that function!'})  
    else:
        request_data = request.get_json()
        x=func.change_password(request_data)
        return str(x)


@main.route('/forgot_password', methods=['POST']) 

def forgot_password():

    ''' This is the api to get token if student forgot password,student need to privide registered email id ...in that email id token will be send'''


    request_data = request.get_json()
    x=func.forgot_password(request_data)
    return str(x)


@main.route('/reset_password', methods=['POST']) 
@token_required
def reset_password(current_user):
    ''' This is api to reset student password if student forgot the password.Student need to provide token that send to their registered mail id and new password'''
    if not current_user.name:
        return jsonify({'message' : 'Cannot perform that function!'})  
    else:
        request_data = request.get_json()
        x=func.reset_password(request_data)
        return str(x)











# @main.route('/otp_generate', methods=['GET', 'POST']) 
# @token_required
# def otp_generate(current_user):
#     if not current_user.name:
#         return jsonify({'message' : 'Cannot perform that function!'})  
#     if (request.method=='POST'):
#         request_data = request.get_json()
#         x=func.otp_generate(request_data)
#         return str(x)

# @main.route('/forget_password', methods=['GET', 'POST']) 
# @token_required
# def forget_password(current_user):
#     if not current_user.name:
#         return jsonify({'message' : 'Cannot perform that function!'})  
#     if (request.method=='POST'):
#         request_data = request.get_json()
#         x=func.forget_password(request_data)
#         return str(x)