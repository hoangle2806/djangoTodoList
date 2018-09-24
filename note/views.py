# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import requests
# from grequests import AsyncRequest
import json

from django.shortcuts import render,redirect

def home(request):
    return render(request, "index.html",{})

def logInView(request):
    #sanity check and then extract data out of the POST request
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        #timeout parameter is used for async call.
        URL = 'http://127.0.0.1:8000/api/auth/login/'
        response = requests.post(URL,{
            'username':username,
            'password': password
        },timeout = 1)
        if response.status_code == 200:
            response = response.json()
        return redirect('http://127.0.0.1:8000/user/{}/{}'.format(response['user']['username'],response['token']))
    else:
        return render(request, "loginView.html",{})

def RegisterView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        data = json.dumps({
            'username' : username,
            'password' : password
        })
        print data
        URL = 'http://127.0.0.1:8000/api/auth/register/'
        response = requests.post(URL, headers={
            'Content-Type':'application/json',
        }, data= data, timeout = 1)
        if response.status_code == 200:
            return redirect("/login/")
        else:
            return render(request, "registerView.html", {
                'error' : "Account already exists",
                "serverCode" : response.status_code
            })
    return render(request, "registerView.html", {})

def UserView(request,username,token):
    #This is used to post a notes
    if request.method == "POST":
        note = request.POST.get('note_input')
        URL = 'http://127.0.0.1:8000/api/notes/'
        data = json.dumps({
            'text': note
        })
        response = requests.post(URL,headers={
        'Content-Type':'application/json',
        "Authorization" : 'Token {}'.format(token)
        }, data= data, timeout = 5)
        if response.status_code < 200 or response.status_code > 300:
            return render(request,"somethingWrong.html",{})

    URL = 'http://127.0.0.1:8000/api/notes/'
    response = requests.get(URL,headers={
        'Content-Type':'application/json',
        "Authorization" : 'Token {}'.format(token)
    },timeout = 1)
    if response.status_code < 200 or response.status_code > 300:
            return render(request,"somethingWrong.html",{})
    return render(request, "userView.html", {
        'data' : response.json(),
        'token' : token,
        'username' : username
    })

def DeleteView(request,username,note_id,token):
    URL = 'http://127.0.0.1:8000/api/notes/{}'.format(note_id)
    response = requests.delete(URL,headers = {
        'Content-Type':'application/json',
        "Authorization" : 'Token {}'.format(token)
    },timeout = 1)
    if response.status_code < 200 or response.status_code > 300:
            return render(request,"somethingWrong.html",{})
    return redirect("/user/{}/{}".format(username,token))

def DeleteView(request,username,note_id,token):
    URL = 'http://127.0.0.1:8000/api/notes/{}'.format(note_id)
    response = requests.delete(URL,headers = {
        'Content-Type':'application/json',
        "Authorization" : 'Token {}'.format(token)
    },timeout = 1)
    if response.status_code < 200 or response.status_code > 300:
            return render(request,"somethingWrong.html",{})
    return redirect("/user/{}/{}".format(username,token))

def EditView(request,username,note_id,token):
    editedText = request.POST.get('editedText')
    data = json.dumps({
            'text': editedText,
    })
    URL = 'http://127.0.0.1:8000/api/notes/{}/'.format(note_id)
    response = requests.put(URL,headers = {
        'Content-Type':'application/json',
        "Authorization" : 'Token {}'.format(token)
    }, data = data,timeout = 1)
    if response.status_code < 200 or response.status_code > 300:
            return render(request,"somethingWrong.html",{})
    return redirect("/user/{}/{}".format(username,token))

