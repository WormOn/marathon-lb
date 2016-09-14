#/usr/bin/env python
#coding utf-8

import logging
import json

import requests
from bottle import Bottle,request


from query_tool import *

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S')


app=Bottle()

def balance_algorithm(app):
    result={
            "status":"",
            "app":app,
            "balance":[]
            }
    get_balance()
    apps_list()
    try:
        apps=[]
        balance=[]
        with open('haproxy_apps','r+') as fapp:
            print ("============================================open haproxy_apps========================================")
            for line_app in fapp.readlines():
                apps.append(line_app.split()[0])
            print (apps)
        with open('balance_algorithm','r+') as fbalance:
            print ("============================================open balance_algorithm========================================")
            for line_balance in fbalance.readlines():
                print ("in for ..................")
                print (line_balance.split())
                balance_r=line_balance.split()[0]
                balance.append(balance_r)
            print ("balance:",balance)
        combination=zip(apps,balance)
        print ("combination:",combination)
        for iterm in combination:
            print (iterm[0]==app)
            if iterm[0]==app:
                result["balance"]=iterm[1]
                result["status"]="OK"
                break
    except Exception:
        logging.debug("Open haproxy_apps or balance_algorithm Failed...")
        result["status"]="NOT OK"
    return result
def acl_list(app):
    result={
            "status":"",
            "acl":[]
            }
    try:
        acl_r=get_acl(app)
        result["acl"]=acl_r
        result["status"]="OK"
    except Exception:
        logging.debug("Call get_acl() Failed...")
        result["status"]="NOT OK"
    return result
@app.route('/instances/:app',method=['GET','POST'])
def instances_get(app):

   # app_instances_r=app_instances(app)
    #print(app_instances_r)
    result={
            "status":"",
            "app":app,
            "instances":[]
            }
    print("instances_get:",app)
    instances=app_instances(app)
    print("instances:",instances)
    try:
        app_instances_r=app_instances(app)
        print(app_instances_r)
        result["instances"]=app_instances_r[1:]
        result["status"]="OK"
    except Exception:
        logging.debug("Call the method app_instances() Failed...")
        result["status"]="NOT OK"
    print("result:",result)
    return result
        
@app.route('/lbnodes/:app',method=['GET','POST'])
def combine(app):
    result={
            "status":"",
            "acl":[],
            "lbpolicy":[],
            }
    try:
        balance_r=balance_algorithm(app)
        logging.debug("==================================print balance_r===========================================")
        logging.debug(balance_r)
        result["lbpolicy"]=balance_r["balance"]
        acl_r=acl_list(app)
        logging.debug("==================================print acl_r===========================================")
        logging.debug(acl_r)
        if len(acl_r["acl"]):
            result["status"]=True
            result["acl"]=acl_r["acl"]
        else:
            result["status"]=False
            result["acl"]=acl_r["acl"]

    except Exception:
        logging.debug("Call balance_algorithm() or acl_list() Failed!!!...")

    return result
@app.route('/test/:app',method=['GET','POST'])
def test_r(app):
    result=app_instances(app)
    print(result)

if __name__=='__main__':
    #test_r('marathon-user')
    #r=instances('marathon-user')
    #print (r)
    app.run(host='0.0.0.0',port=8888)
    #lb=combine('calico')
    #print(lb)
    #inst=instances_get('calico')
    #print(inst)
    #balance=balance_algorithm('calico')
    #print(balance)


