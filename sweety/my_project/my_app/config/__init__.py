
import json
import os
# with open('email.json','r') as f:
#     parameters=json.load(f)['parameter']

class Config:
   
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_CONNECTION')
    #SECRET_KEY='52969bb25fde496f8c5f36c1cd8e6a33'
    SECRET_KEY='thisissecret'


    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    #MAIL_USERNAME = parameters['gmail-user']
    MAIL_USERNAME = os.environ.get('gmail_user_id')
    MAIL_PASSWORD =os.environ.get('gmail_pass')
    #MAIL_PASSWORD = parameters['gmail-password']
    # app.config['SECRET_KEY']='52969bb25fde496f8c5f36c1cd8e6a33'

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sweety123@localhost/sweety'