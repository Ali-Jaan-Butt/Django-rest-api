from django.shortcuts import render
from django.http import HttpResponse
import pymongo
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string
from django.http import JsonResponse
from django.urls import path
from django.conf import settings
from django.core.management import execute_from_command_line
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
import json
from sentence_transformers import SentenceTransformer, util
import requests

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

def for_fun(request):
    a = 2
    return a

def profile(request):
    with open('log_email.txt', 'r') as file:
        em = file.read()
    client = pymongo.MongoClient()
    database_name = "web_project"
    db = client[database_name]
    collection_name = "signup_data"
    collection = db[collection_name]
    cursor = collection.find()
    for document in cursor:
        obj = document
        if em==obj['Email']:
            prof_email = em
            prof_name = obj['Name']
            tags = obj['Tags']
            if tags!=None:
                tags = obj['Tags']
    inf = {'User_Name':prof_name, 'User_Email':prof_email, 'Tags':tags}
    return render(request, 'temp/profile.html', inf)

def save_tags(request):
    if request.method == 'POST':
        tag = request.POST.get('tags-input')
        up_tag = None
        with open('log_email.txt', 'r') as file:
            email = file.read()
        client = pymongo.MongoClient()
        database_name = "web_project"
        db = client[database_name]
        collection_name = "signup_data"
        collection = db[collection_name]
        cursor = collection.find()
        for document in cursor:
            obj = document
            if email==obj['Email']:
                up_tag = tag
                ud_obj = { '$set': {'Tags':up_tag}}
                collection.update_one(obj, ud_obj)
    return interns_list(request)

def cli_dash(request):
    res = requests.get('http://127.0.0.1:8000/api/items/')
    data = res.json()
    dict_data = {index: value for index, value in enumerate(data)}
    data = {'dict_data':dict_data}
    return render(request, 'temp/client_dash.html', data)

def interns_list(request):
    with open('log_email.txt', 'r') as file:
        gm = file.read()
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    res = requests.get('http://127.0.0.1:8000/api/items/')
    data = res.json()
    results = []
    client = pymongo.MongoClient()
    database_name = "web_project"
    db = client[database_name]
    collection_name = "signup_data"
    collection = db[collection_name]
    cursor = collection.find()
    for document in cursor:
        obj = document
        if gm == obj['Email']:
            if obj['Tags'] != None:
                user_tag = obj['Tags']
            else:
                user_tag = None
    if user_tag != None:
        for ml in data:
            des = [ml['Description']]
            tag = [user_tag]
            job_embeddings = model.encode(des, convert_to_tensor=True)
            profile_embeddings = model.encode(tag, convert_to_tensor=True)
            similarity_scores = util.pytorch_cos_sim(job_embeddings, profile_embeddings)
            results.append(similarity_scores)
        def find_top_n_max_indices(lst, n):
            indexed_lst = list(enumerate(lst))
            sorted_lst = sorted(indexed_lst, key=lambda x: x[1], reverse=True)
            top_n = sorted_lst[:n]
            top_n_values = [item[1] for item in top_n]
            top_n_indices = [item[0] for item in top_n]
            return top_n_values, top_n_indices
        top_values, top_indices = find_top_n_max_indices(results, 3)
        data_mod = [data[ind] for ind in top_indices]
        dict_data = {index: value for index, value in enumerate(data_mod)}
    else:
        dict_data = {index: value for index, value in enumerate(data)}
    data = {'dict_data':dict_data}
    return render(request, 'temp/job_posting.html', data)

def applied(request):
    if request.method == 'POST':
        with open('log_email.txt', 'r') as file:
            link_email = file.read()
        title = request.POST.get('int-title')
        company = request.POST.get('int-comp')
        location = request.POST.get('int-loc')
        duration = request.POST.get('int-dur')
        description = request.POST.get('int-des')
        print(title)
    return interns_list(request)

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
    return cli_dash(request)

def login_info(request):
    if request.method == 'POST':
        con_email = None
        con_pass = None
        log = {}
        log['User_Type'] = 'Nothing'
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
                user_type = obj['User_Type']
        if con_pass!=None:
            if con_email==login_email and con_pass==login_pass:
                log = {'Email':login_email, 'Password':login_pass, 'User_Type':user_type}
                with open('log_email.txt', 'w') as file:
                    file.write(login_email)
                client = pymongo.MongoClient()
                database_name = "web_project"
                db = client[database_name]
                collection_name = "login_data"
                collection = db[collection_name]
                collection.insert_one(log)
                print(user_type)
                print(login_email)
                print(login_pass)
                if user_type=='client':
                    get_items(request)
                    return cli_dash(request)
                elif user_type=='job_seeker':
                    get_items(request)
                    return interns_list(request)
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
    return for_fun(request)

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
        sign = {'Name':name, 'Email':email, 'Password':password, 'Confirm_Password':conf_pass, 'User_Type':user_type, 'Tags':None}
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