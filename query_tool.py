#!/usr/bin/env python
#coding=utf-8
"""
Query_version
__version__="V1.0"
"""
import os
import re
import logging

#apps
def apps_list():
    """
    return all  apps
    :None
    """
    if os.path.exists('haproxy_apps'):
        os.system('rm -rf haproxy_apps')
    with open('haproxy.cfg','r+') as fd:
        for line in fd.readlines():
            with open('haproxy_apps','a+') as fapp:
                f_r=re.search(r'  use_backend .*_[0-9]* if .*$',line)
                print("f_r:",f_r)
                if f_r:
                    back_r=line.split()[1]
                    print(back_r)
                    app=re.sub('_.*$','',back_r)
                    fapp.write(app+'\n')
            """
            r_search=re.search('^backend',line)
            if r_search:
                r_sub=re.sub(r'backend ',"",line)
                r_sub2=re.sub(r'_.*$',"",r_sub)
                if r_sub2=='  use\n':
                    continue
                else:
                    with open('haproxy_apps','a+') as fapp:
                        fapp.write(r_sub2)
            """
#get apps that exposed for service
def apps_exposed():
    with open('haproxy.cfg','r+') as fd:
        apps=[]
        for line in fd.readlines():
            f_r=re.search(r'  use_backend .*_[0-9]* if .*$',line)
            #print("f_r:",f_r)
            if f_r:
                back_r=line.split()[1]
                print(back_r)
                apps.append(back_r)
        return apps
#apps and instances
def apps_instances():
    """
    return all apps and  instances 
    :None
    """
    flag=False
    bflag=False
    apps=apps_exposed()
    if os.path.isfile('haproxy_apps_instances.original'):
        os.system('rm -rf haproxy_apps_instances.original')
    
    for app in apps:
        print("app:",app)
        with open('haproxy.cfg','r+') as fd:
            for line in fd.readlines():
                #print("line:",line)
                backend_r=re.match(r'backend {}'.format(app),line)
                #print("backen_r:",backend_r)
                if backend_r:
                    flag=True
                    bflag=True
                    with open('haproxy_apps_instances.original','a+') as fapp:
                        print(line)
                        r_sub=re.sub(r'_.*$',"",app)
                        #print("r_sub:",r_sub)
                        fapp.write(r_sub+'\n')
                elif flag or bflag:
                    server_r=re.match(r'  server ',line)
                    #print("server_r:",server_r)
                    if server_r:
                        flag=False
                        bflag=True
                        print("server_r line:",line)
                        with open('haproxy_apps_instances.original','a+') as fapp2:
                            fapp2.write(line.split()[1]+' '+line.split()[2]+'\n')
                    else:
                        bflag=False





        
#app instances
def app_instances(app_name):
    """
    return the specified app's name and the respond instances
    :app_name the specified app's name
    """
    apps_instances()
    with open('haproxy_apps_instances.original','r+') as fd:
        flag=False
        next_flag=False
        app_instances=[]
        for line in fd.readlines():
            match_r=re.match(app_name+'\n',line)
            if match_r:
                flag=True
                app_instances.append(app_name)
            elif flag:
                if len(line)>15:
                    split_r=line.split()
                    #print (split_r)
                    if len(split_r)==2:
                        app_instances.append(line.split()[0]+' '+line.split()[1])
                    else:
                        app_instances.append(line.split()[0]+' '+line.split()[1]+' '+line.split()[2])
                else:
                    flag=False
                    next_r=re.match(app_name+'\n',line)
                    if next_r:
                        next_flag=True
            elif next_flag:
                if len(line)>15:
                    if len(line.split())==2:
                        app_instances.append(line.split()[0]+' '+line.split()[1])
                    else:
                        app_instances.append(line.split()[0]+' '+line.split()[1]+' '+line.split()[2])
                else:
                    next_flag=False
                    switch_r=re.match(app_name+'\n',line)
                    if switch_r:
                        flag=True
                    

        #print (app_instances)
        return app_instances
#get_balance
def get_balance():
    """
    get the haproxy's load balance algorithm 
    :None
    """
    flag=False
    result={"app":"","balance":""}
    apps=apps_exposed()
    if os.path.isfile('balance_algorithm'):
        os.system('rm -rf balance_algorithm')
    for app in apps:
        with open('haproxy.cfg','r+') as fd:
            for line in fd.readlines():
                backend_r=re.match(r'backend {}'.format(app),line)
                print("backen_r:",backend_r)
                if backend_r:
                    flag=True
                    #r_sub=re.sub(r'_.*$',"",app)
                    #result["app"]=r_sub
                elif flag:
                    search_r=re.search('  balance \w+',line)
                    if search_r:
                        with open('balance_algorithm','a+') as fb:
                            line=re.sub('^  ',"",line)
                            fb.write(line.split()[1]+'\n')
                        flag=False



#get acl
def get_acl(app):
    """
    get the haproxy's acl rule
    :None
    """
    acl=[]
    if os.path.exists("haproxy_acl"):
        os.system("rm -rf haproxy_acl")

    with open("haproxy.cfg","r+") as fd:
        for line in fd.readlines():
            acl_r=re.match(r'  acl ',line)
            if acl_r:
                print ("acl_r:",line)
                r=re.match(r'[\S\s]*?{}[\s]'.format(app),line)
                print ("r:",r)
                if r:
                    print ("===after===", line)
                    logging.debug(line)
                    acl.append(line.split()[4])
    logging.debug(acl)
    return acl


        



if __name__=='__main__':
    print("Test Module...")
    #acl=get_acl('marathon-user')
    #print(acl)
    #balance=get_balance()
    #print(balance)

    instances=app_instances('marathon-user')
    print(instances)

    #apps=apps_exposed()
    #print (apps)
    #apps_instances()
