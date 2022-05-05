from flask import render_template, url_for, flash, redirect, request, Blueprint
# from student.main import func
from my_app.model.student import Student
# from student import app
from my_app import db,bcrypt
import re
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from my_app.helpers.validation_helper import *
from my_app.helpers.user import *
from flask_mail import *
import random
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import jwt
from datetime import datetime,timedelta
# engine = db.create_engine("postgresql://postgres:sweety123@localhost/sweety")
# from sqlalchemy import create_engine
# engine = create_engine('postgresql://scott:tiger@localhost:5432/sweety')
# from sqlalchemy import create_engine
# engine = create_engine('postgresql+psycopg2://postgres:sweety123@localhost/sweety')
import logging
# import pdb
# pdb.set_trace()
# otp=random.randint(0000, 9999)
# from student import mail

LOG_FORMAT="%(lineno)d -- %(levelname)s -- %(asctime)s -- %(message)s"
logging.basicConfig(filename='logfile.log',level=logging.DEBUG,format=LOG_FORMAT,filemode='w')
logger=logging.getLogger()


def register_student(data):
    try:
        logger.debug('getting user name,address,phone no,email address,password for registration')
        name=data['name']
        username=data['username']
        password = data['password']
        email = data['email']
        address = data['address']       
        if email_validator(email):
            student=student_for_email(email)
            #student = Student.query.filter_by(email=email).first()
            if not student:
                if password_validator(password):
                    hashed_pw=generate_hashed_password(password)
                    student = Student(name=name,username=username,password=hashed_pw,email=email,address=address)
                    db.session.add(student)
                    db.session.commit()
                    return 'New student registration successful'
                else:
                    return "Provided password not strong..Password must contain letter,numerics,special character."
            else:
                return 'Email ID already exists !! Please Try using another email Or Login'                
        else:
            return 'You have entered a worng email id !! '
    except Exception as e:
        logger.error('this is a error message(may be database error)')      
        return e," Not Provited"


def fetch_student_details(data):
    try:
        email = data['email']        
        if email_validator(email):        
            student=student_for_email(email)
            if not student:
                return "No student registered using this mail id..!! Please resiter first"
            else:
                student_data = {}
                student_data['s_no'] = student.s_no
                student_data['name'] = student.name
                student_data['username'] = student.username
                student_data['email'] = student.email
                student_data['address'] = student.address
            return jsonify({'Student Details : ' : student_data})
        else:
            return 'You have entered a worng email id !! '
    except Exception as e:       
        return e,"Not Provited"


def modify_user(data):
    try:
        email=data['email']
        address=data['address']
        if email_validator(email):
            student=student_for_email(email)
            if not student:
                return "No student registered using this mail id..!! Please resiter first"
            else:
                student.address = address
                db.session.commit()
                return "Successfull updated the record of " + email
        else:
            return 'You have entered a worng email id !! '
    except Exception as e:       
        return e,"Not Provited"
   

def login_student(data):
    try:
        email=data['email']
        password=data['password']
        if email_validator(email):
            #checking the student with given mail is prsent or not
            student=student_for_email(email)
            if student:                
                pwd=student.password
                    #getting password
                if check_hashed_password(pwd,password):
                    payload_data = {"email": student.email,"s_no": student.s_no,"username": student.username,'exp' : datetime.utcnow() + timedelta(minutes=60)}
                    my_secret = current_app.config['SECRET_KEY']
                    token = jwt.encode(payload=payload_data,key=my_secret)
                    
                    return token
                
                    #TODO make a jwt token using users data and return in the response

                else:
                        # return 'email not exists'
                    return 'You have entered a wrong password'
            else:
                return 'student not registered.. please register first !!'
        else:
            return 'You have entered a worng email id !! '
    except Exception as e:       
            return e


def change_password(data):
    try:
        email=data['email']
        password=data['password']
        new_password=data['new_password']
        #checking provided mail id valid or not
        if email_validator(email):
            #checking the student with given mail is prsent or not
            student=student_for_email(email) 
            if student:               
                pwd=student.password
                if check_hashed_password(pwd,password):
                    #getting password
                # if bcrypt.check_password_hash(pwd,password):
                    if password_validator(new_password):
                        hashed_new_pw=generate_hashed_password(new_password)
                        student.password = hashed_new_pw
                        db.session.commit()
                        return "Successfull changed the password " 
                    else:
                        return "Provided password not strong..Password must contain letter,numerics,special character."
                else:
                        # return 'email not exists'
                    return 'You have entered a wrong password.. Please give correct password !!'
            else:
                return 'This Email Id not registered.. please register first !!'
        else:
            return 'You have entered a worng email id !! '
    except Exception as e:       
            return e




def forgot_password(data):
    ''' Sending token in email id to reset password'''
    try:
        email=data['email']
        if email_validator(email):
            #checking the student with given mail is registered or not
            student = Student.query.filter_by(email=email).first()
            if student:
                payload_data = {"email": student.email,"s_no": student.s_no,"username": student.username,'exp' : datetime.utcnow() + timedelta(minutes=60)}
                my_secret = current_app.config['SECRET_KEY']
                # 'exp' : datetime.utcnow() + timedelta(minutes = 30)
                # 'expiration': str(datetime.utcnow() + timedelta(minutes = 5))
                token = jwt.encode(payload=payload_data,key=my_secret)
                mail=Mail(current_app)
                msg=Message('Password Reset Request',sender='sweetybiswas433@gmail.com',recipients=[email])
                msg.body = 'To reset your password, use this token : '+'\n\n'+token+ '\n\n' + 'Please use this token before 5 minutes.' + '\n' + 'Post 1 Hour token will be invalid.\n If you did not make this request then simply ignore this email and no changes will be made.'                
                # msg.body='Hi,We received a request to access your Account. Your OTP  is :'+ str(otp) 
                mail.send(msg)
                return 'An email with a verification code Successfull sent to ',email
            else:
                return 'This Email Id not registered.. please register first !!'
        else:
            return 'You have entered a worng email id !! '
    except Exception as e:       
            return e


def reset_password(datas):
    try:
        token = None
        new_password=datas['new_password']
        if 'forget_pass_token' in request.headers:
            token = request.headers['forget_pass_token']
        if not token:
            return jsonify({'message' : 'Token is missing can not reset password!'}), 401            
        else:
            #if got the token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            #current_user = Student.query.filter_by(s_no=data['s_no']).first()
            email=data['email']
            student=student_for_email(email)
            if student:
                old_pass=student.password
                if bcrypt.check_password_hash(old_pass,new_password):
                    return "You have given your last password. Please provide a new secure password..!"
                elif password_validator(new_password):
                    hashed_new_pw=generate_hashed_password(new_password)                                  
                    student.password = hashed_new_pw
                    db.session.commit()
                    return "Token Verified.. Successfull changed the password " 
                else:
                    return "Please Provide a more secure password..Password must contain numerics,letters,special character !!"      
            else:
                return "Student not registered"                                      
    except jwt.ExpiredSignatureError:
        msg = 'Token expired. Get new one'
        return msg
    except jwt.DecodeError:
        msg = 'Error decoding signature.'
        return msg
    except jwt.InvalidTokenError:
        return 'Invalid Token.'
    except Exception as e:
        return e





# def otp_generate(data):
#     try:
#         email=data['email']

#         if email_validator(email)==True:
#             #checking the student with given mail is prsent or not
#             student=student_for_email(email)
#             if student:
#                 mail=Mail(current_app)
#                 msg=Message('Verification Code',sender='sweetybiswas433@gmail.com',recipients=[email])
                
#                 msg.body='Hi,We received a request to access your Account. Your OTP  is :'+ str(otp) 
#                 mail.send(msg)
#                 return 'An email with a verification code Successfull sent to ',email
#             else:
#                 return 'This Email Id not registered.. please register first !!'

#         else:
#             return 'You have entered a worng email id !! '
#     except Exception as e:       
#             return e


# def forget_password(data):
#     """this is the docstring for forget password"""
#     try:
#         email=data['email']
#         user_otp=data['otp']
#         new_password=data['new_password']
#         if email_validator(email)==True:
#             #checking the student with given mail is prsent or not
#             student=student_for_email(email)
#             if student: 
#                 if otp == int(user_otp):  

#                     hashed_new_pw=bcrypt.generate_password_hash(new_password).decode('utf-8')
#                     student.password = hashed_new_pw
#                     db.session.commit()
#                     return "OTP Verified .. Successfull changed the password " 
#                 else:
#                     return "OTP not verified.. Please try again !!"

#             else:
#                 return 'This Email Id not registered.. please register first !!'
#         else:
#             return 'You have entered a worng email id !! '
#     except Exception as e:       
#             return e








