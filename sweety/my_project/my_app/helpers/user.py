from my_app.model.student import Student
from my_app import db,bcrypt


def student_for_email(email):
    student = Student.query.filter_by(email=email).first()
    return student


def student_for_s_no(s_no):
    student = Student.query.filter_by(s_no=s_no).first()
    return student



def generate_hashed_password(password):
    hashed_pw=bcrypt.generate_password_hash(password).decode('utf-8')
    return hashed_pw


def check_hashed_password(db_pass,given_pass):
    if bcrypt.check_password_hash(db_pass,given_pass):
        return True
    else:
        return False







# hashed_new_pw=bcrypt.generate_password_hash(new_password).decode('utf-8')
# student.password = hashed_new_pw
# db.session.commit()


#                     hashed_pw=bcrypt.generate_password_hash(password).decode('utf-8')
#                     student = Student(name=name,username=username,password=hashed_pw,email=email,address=address)
#                     db.session.add(student)
#                     db.session.commit()



