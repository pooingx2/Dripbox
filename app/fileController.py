#-*- coding: utf-8 -*-

from app.models import *

# 같은 폴더 안에 파일이 존재하는지 확인
import ssg_model


def isExist(parent, name):
    files = File.objects.filter(parent=parent, name=name)
    print files.__len__()

    if files.__len__() == 0:
        return False
    else:
        return True


# 폴더 생성
def createFolder(name, type, size, parent, user, path):
    if isExist(parent, name):
        return False
    else:
        file = File(name=name, type=type, size=size, parent=parent, user=user, path=path)
        file.save()
        return True


# 파일 업로드
def upload(name, type, size, parent, user, file, path):
    if isExist(parent, name):
        return False
    else:
        uploadFile = file
        print uploadFile._name
        # SDK upload 호출

        file = File(name=name, type=type, size=size, parent=parent, user=user, path=path)
        file.save()
        return True


# 파일 업로드
def download(id):

    file
    try:
        temp = File.objects.get(id=id)
        interface = ssg_model.interface.SSGInterface()
        file_buf = interface.download()
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
