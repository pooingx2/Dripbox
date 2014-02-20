#-*- coding: utf-8 -*-

from app.models import *


# 같은 폴더 안에 파일이 존재하는지 확인
def isExist(parent, name):
    files = File.objects.filter(parent=parent, name=name)
    print files.__len__()

    if files.__len__() == 0:
        return False
    else:
        return True


# 폴더 생성
def createFolder(name, type, size, parent, user):
    if isExist(parent, name):
        return False
    else:
        file = File(name=name, type=type, size=size, parent=parent, user=user)
        file.save()
        return True


# 파일 업로드
def upload(name, type, size, parent, user, file):
    if isExist(parent, name):
        return False
    else:
        # SDK upload 호출
        uploadFile = file
        print uploadFile._name

        file = File(name=name, type=type, size=size, parent=parent, user=user)
        file.save()
        return True


# 파일 업로드
def download(id):

    file
    try:
        temp = File.objects.get(id=id)

        # SDK download 호출 (리턴값 멍미?)
    except Exception as e:
        print e
        return str(e)
    return file


# 파일 삭제
def delete(id):

    file
    try:
        # SDK delete 호출 (리턴값 멍미?)

        File.objects.filter(id=id).delete()
    except Exception as e:
        print str(e)

    return file
