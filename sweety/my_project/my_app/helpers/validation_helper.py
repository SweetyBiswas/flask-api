
import re

from soupsieve import match
from my_app.config.regex_config import *



# def email_validator(email):
    
#     if re.match(email_regex,email):
#         return True
#     else:
#         return False


def email_validator(email):
    patten=re.compile(email_regex)
    if patten.match(email):
        return True
    else:
        return False



def username_validator(username):
    patern=re.compile(username_regex)
    if patern.match(username):
        return True
    else:
        return False


def password_validator(password):  
    # password_reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
      
    # compiling regex
    pat = re.compile(password_regex)
      
    # searching regex                 
    mat = re.search(pat,password)
      
    # validating conditions
    if mat:
        return True
    else:
        return False