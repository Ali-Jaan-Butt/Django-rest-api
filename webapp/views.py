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

def generate_verification_code(length=6):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def send_verification_email(recipient_email, verification_code):
    sender_email = "interns.hub510@gmail.com"
    sender_password = "sherlocked21239"
    subject = "Your Verification Code of Interns.hub"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    body = f"Your verification code is: {verification_code}"
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Verification email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def email_verify(request):
    if request.method=='POST':
        recipient_email = request.POST.get('verify-email')
        verification_code = generate_verification_code()
        send_verification_email(recipient_email, verification_code)
    return verify(request)