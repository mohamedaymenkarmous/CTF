from flask import Flask, render_template, request, session, redirect
import os
import requests
from captcha import verifyCaptchaValue

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('user')
    password = request.form.get('pass')
    captchaToken = request.form.get('captcha_verification_value')

    privKey = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" #redacted
    r = requests.get('http://127.0.0.1:{}/captchaVerify?captchaUserValue={}&privateKey={}'.format(str(port), captchaToken, privKey))
    #backdoored ;)))
    if username == "backd00r" and password == "catsrcool" and r.content == b'allow':
        session['logged'] = True
        return redirect('//redacted//')
    else:
        return "login failed"


@app.route('/captchaVerify')
def captchaVerify():
    #only 127.0.0.1 has access
    if request.remote_addr != "127.0.0.1":
        return "Access denied"

    token = request.args.get('captchaUserValue')
    privKey = request.args.get('privateKey')
    #TODO: remove debugging privkey for testing: 8EE86735658A9CE426EAF4E26BB0450E from captcha verification system
    if(verifyCaptchaValue(token, privKey)):
        return str("allow")
    else:
        return str("deny")