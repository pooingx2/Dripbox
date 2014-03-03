
__author__ = 'PJY'
from django.template import loader, Context, Template
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app.models import User, File
import fileController

import json


def hello(request):
    return HttpResponse("Hello World2")


def main(request):

    if "email" in request.session:
        sessionEmail = request.session["email"]
        t = loader.get_template('home.html')
        c = Context({'email': sessionEmail},)
    else:
        t = loader.get_template('main.html')
        c = Context()

    return HttpResponse(t.render(c))


@csrf_exempt
def signup(request):

    print '\n\nsignup'

    if request.method == 'POST':

        email = request.POST['email']
        pwd = request.POST['pwd']
        temp = ""

        try:
            temp = User.objects.get(email=email).email
        except Exception as e:
            print e

        if not temp == email:
            user = User(email=email, pwd=pwd)
            user.save()
            msg = "Signup Success"
            status = 1
        else:
            msg = "Email is already taken"
            status = 0
            #return HttpResponse(json.dumps(dict), mimetype="application/json", status=500)
        print "asd"

        dict = {'email': email, 'msg': msg, 'status': status}

        return HttpResponse(json.dumps(dict), mimetype="application/json")


@csrf_exempt
def login(request):

    print '\n\nlogin'

    if request.method == 'POST':

        try:
            email = request.POST['email']
            pwd = request.POST['pwd']
            user = User.objects.get(email=email)
            if not pwd == user.pwd:
                msg = "Password Incorrect"
                status = 0
            else:
                request.session['email'] = email
                msg = "Login Success"
                status = 1
        except Exception as e:
            msg = str(e)
            status = 0
            print e

        dict = {'email': email, 'msg': msg, 'status': status}

        return HttpResponse(json.dumps(dict), mimetype="application/json")


def user(request):

    print '\n\nUser\n\n'
    users = User.objects.all()

    for user in users:
        print user.email + " " + user.pwd

    HttpResponse("Hello World2")


def logout(request):

    request.session.clear()

    t = loader.get_template('main.html')
    c = Context()

    return HttpResponse(t.render(c))


@csrf_exempt
def home(request):
    """

    :param request:
    :return:
    """
    if "email" in request.session:

        sessionEmail = request.session["email"]
        if request.method == 'POST':
            option = request.POST['option']

            if option == "create":
                name = request.POST['name']
                type = request.POST['type']
                size = request.POST['size']
                parent = request.POST['parent']
                path = request.POST['path'] + " / " + name

                if fileController.createFolder(name, type, size,
                                               parent, User.objects.get(email=sessionEmail), path):
                    msg = "Create Success"
                    status = 1
                else:
                    msg = "Name is duplication"
                    status = 0

                dict = {'msg': msg, 'status': status}

            elif option == "upload":
                name = request.POST['name']
                type = request.POST['type']
                size = request.POST['size']
                parent = request.POST['parent']
                uploadFile = request.FILES['file']
                path = request.POST['path'] + " / " + name
                if fileController.upload(name, type, size, parent,
                                         User.objects.get(email=sessionEmail), uploadFile, path):
                    msg = "Upload Success"
                    status = 1
                else:
                    msg = "Name is duplication"
                    status = 0

                dict = {'msg': msg, 'status': status}

            elif option == "download":
                id = request.POST['id']
                file = fileController.download(sessionEmail, id)
                msg = "Download Success"
                status = 1

                dict = {'msg': msg, 'status': status}
                # dict = {'msg': msg, 'status': status, 'file': file}

            elif option == "delete":
                id = request.POST['id']
                fileController.delete(sessionEmail, id)
                msg = "Delete Success"
                status = 1

                dict = {'msg': msg, 'status': status}

            return HttpResponse(json.dumps(dict), mimetype="application/json")

        if request.method == 'GET':

            path = "root"
            try:
                current = request.GET['id']
                path = File.objects.get(id=current).path
            except Exception as e:
                current = "root"
                print e

            # files = File.objects.all()
            # files = File.objects.filter(parent=current)

            folders = File.objects.select_related().filter(user=sessionEmail, parent=current, type='folder')
            files = File.objects.select_related().filter(user=sessionEmail, parent=current).exclude(type='folder')

            t = loader.get_template('home.html')
            c = Context({'email': sessionEmail, 'folders': folders, 'files': files, 'path': path},)

            return HttpResponse(t.render(c))

    else:
        t = loader.get_template('main.html')
        c = Context()

        return HttpResponse(t.render(c))
