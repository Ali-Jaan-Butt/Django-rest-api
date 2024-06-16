from django.shortcuts import render
from django.http import HttpResponse
import pymongo
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string
from fastapi import FastAPI
from django.http import JsonResponse
from django.urls import path
from django.conf import settings
from django.core.management import execute_from_command_line
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
import json

client = MongoClient('mongodb://localhost:27017/')
db = client['web_project']
collection = db['interns_data']

@csrf_exempt
def get_items(request):
    if request.method == 'GET':
        items = list(collection.find({}, {'_id': 1, 'Title': 1, 'Company': 1, 'Location': 1, 'Duration': 1, 'Description': 1}))
        for item in items:
            item['_id'] = str(item['_id'])
        return JsonResponse(items, safe=False)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def get_item(request, item_id):
    if request.method == 'GET':
        try:
            item = collection.find_one({'_id': ObjectId(item_id)}, {'_id': 1, 'Title': 1, 'Company': 1, 'Location': 1, 'Duration': 1, 'Description': 1})
            if item:
                item['_id'] = str(item['_id'])
                return JsonResponse(item)
            else:
                return JsonResponse({'error': 'Item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def create_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = collection.insert_one(data)
        return JsonResponse({'_id': str(result.inserted_id)}, status=201)
    return JsonResponse({'error': 'Invalid method'}, status=405)

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

def client_dashboard(request):
    return render(request, 'temp/post_intern.html')

def save_internship(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        comp = request.POST.get('company')
        loc = request.POST.get('location')
        dur = request.POST.get('duration')
        des = request.POST.get('description')
        client = pymongo.MongoClient()
        database_name = "web_project"
        db = client[database_name]
        collection_name = "interns_data"
        collection = db[collection_name]
        jobs = {'Title':title, 'Company':comp, 'Location':loc, 'Duration':dur, 'Description':des}
        collection.insert_one(jobs)
        get_items(request)
    return render(request, 'temp/client_dash.html')

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
                if obj['User_Type']=='client':
                    return render(request, 'temp/client_dash.html')
                elif obj['User_Type']=='job_seeker':
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