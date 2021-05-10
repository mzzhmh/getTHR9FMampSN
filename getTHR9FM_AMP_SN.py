#!/usr/bin/python3.6
from easysnmp import Session
import re
import pprint
import requests
import sys
import time
import json

debugfile = open('debug.info','w')

with open("THR9_Single_TX.csv") as ifile:
    for line in ifile:
        name = line.split(",")[0]
        site = line.split(",")[1].split("\\")[2][0:4]
        baseURL = line.split(",")[4]
        print(name+","+site+","+baseURL,file=debugfile,flush=True)

        #post login
        payload = {'username': username,'password':encoded,'HTML5':'Login+(HTML5+Gui)'}
        loginURL = baseURL+"/servlet/LogonBrowser"
        print(loginURL,file=debugfile,flush=True)
        result = ""
        with requests.Session() as session:
            try:
                post = session.post(loginURL, data=payload, timeout = 15)
                time.sleep(0.3)
                #print(post.status_code)
                if (post.status_code == 200):
                #get how many AMPs
                    ampNumURL = baseURL+"/html5/ds9/tx/_TCE_:config:txControl/outputStage/1/numberOfAmplifiers"
                    print(ampNumURL,file=debugfile,flush=True)
                    ret2=session.get(ampNumURL,timeout=15)
                    time.sleep(0.3)
                    if (ret2.status_code == 200):
                        ampNum = ((json.loads(ret2.text))["val"])
                        print("AMP number:"+str(ampNum),file=debugfile,flush=True)
                        #now loop through to get the sn of each amp
                        for i in range(1,ampNum+1):
                            ampURL = baseURL+"/html5//ds9/tx/_STD_/ost.1:amp."+str(i)+"/typePlateHw:serialNo"
                            #get serial number
                            print(ampURL,file=debugfile,flush=True)
                            ret3 = session.get(ampURL,timeout=15)
                            time.sleep(0.3)
                            if (ret3.status_code == 200):
                                result = "amp"+str(i)+":"+str((json.loads(ret3.text))["val"])
                            else:
                                result = str(ret3.status_code)+"|||||"+"cannot get individual amp data"
                            print(name+","+site+","+baseURL+","+result,flush=True)
                    else:
                        result = str(ret2.status_code)+"|||||"+"cannot get AMP number"
                        print(name+","+site+","+baseURL+","+result,flush=True)
                        continue
                else:
                    result = str(post.status_code)+"|||||"+"cannot login"
                    print(name+","+site+","+baseURL+","+result,flush=True)
                    continue


                #logout
                logoutURL = baseURL+"/html5/logoff"
                r = session.get(logoutURL)

            except Exception as e:
                print(name+","+site+","+baseURL+","+str(e),flush=True)




