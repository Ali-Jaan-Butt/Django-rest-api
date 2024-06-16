from django.shortcuts import render
from django.http import HttpResponse
import pymongo
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string

def myapp(request):
    return render(request, 'temp/login.html')

def signup(request):
    return render(request, 'temp/signup.html')

def forget(request):
    return render(request, 'temp/forget.html')

def verify(request):
    return render(request, 'temp/verify.html')

def update(request):
    return render(request, 'temp/update_pass.html')

def login_info(request):
    if request.method == 'POST':
        con_email = None
        con_pass = None
        login_email = request.POST.get('login_email')
        login_pass = request.POST.get('login_password')
        client = pymongo.MongoClient()
        database_name = "web_project"
        db = client[database_name]
        collection_name = "signup_data"
        collection = db[collection_name]
        cursor = collection.find()
        for document in cursor:
            obj = document
            if login_email==obj['Email'] and login_pass==obj['Password']:
                con_email = login_email
                con_pass = login_pass
        if con_pass!=None:
            if con_email==login_email and con_pass==login_pass:
                log = {'Email':login_email, 'Password':login_pass, 'User_Type':obj['User_Type']}
                client = pymongo.MongoClient()
                database_name = "web_project"
                db = client[database_name]
                collection_name = "login_data"
                collection = db[collection_name]
                collection.insert_one(log)
                print(login_email)
                print(login_pass)
                return render(request, 'temp/job_posting.html')
            else:
                print('Invalid login cridentials')
                log = {}
                log['User_Type'] = 'Nothing'
                return render(request, 'temp/login.html')
        else:
            print('Account not found')
            log = {}
            log['User_Type'] = 'Nothing'
            return render(request, 'temp/login.html')
    return log['User_Type']

def signup_info(request):
    if request.method == 'POST':
        client = pymongo.MongoClient()
        database_name = "web_project"
        db = client[database_name]
        collection_name = "signup_data"
        collection = db[collection_name]
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        conf_pass = request.POST.get('conf_pass')
        user_type = request.POST.get('user_type')
        sign = {'Name':name, 'Email':email, 'Password':password, 'Confirm_Password':conf_pass, 'User_Type':user_type}
        collection.insert_one(sign)
        return myapp(request)
    return user_type
    
letters_and_digits = string.ascii_letters + string.digits
code = ''.join(random.choice(letters_and_digits) for i in range(6))

def email_verify(request):
    if request.method=='POST':
        recipient_email = request.POST.get('verify-email')
        with open('up_pass_email.txt', 'w') as file:
            file.write(recipient_email)
        client = pymongo.MongoClient()
        database_name = "web_project"
        db = client[database_name]
        collection_name = "signup_data"
        collection = db[collection_name]
        cursor = collection.find()
        for document in cursor:
            obj = document
            if recipient_email==obj['Email']:
                conf_res_email = recipient_email
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login('interns.hub510@gmail.com', 'frer bnho uocd pztb')
            subject = 'Verification Code'
            body = 'Your verification code is: '+str(code)
            msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail('interns.hub510@gmail.com', conf_res_email, msg)
        return verify(request)
    return conf_res_email

def code_verify(request):
    if request.method=='POST':
        in_code = request.POST.get('ver_code')
        if in_code==code:
            return update(request)
        else:
            pass
    return in_code

def update_pass(request):
    if request.method=='POST':
        up_pass = request.POST.get('updated-pass')
        conf_up_pass = request.POST.get('conf-update-pass')
        with open('up_pass_email.txt', 'r') as file:
            up_email = file.read()
        if up_pass==conf_up_pass:
            client = pymongo.MongoClient()
            database_name = "web_project"
            db = client[database_name]
            collection_name = "signup_data"
            collection = db[collection_name]
            cursor = collection.find()
            for document in cursor:
                obj = document
                if up_email==obj['Email']:
                    found_pass = up_pass
            ud_obj = { '$set': {'Password':found_pass, 'Confirm_Password':found_pass}}
            collection.update_one(obj, ud_obj)
            print('Data updated')
    return render(request, 'temp/login.html')