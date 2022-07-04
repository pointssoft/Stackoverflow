
from datetime import date
from datetime import datetime
import json
from re import T
import random
import requests
from requests import exceptions
from requests.exceptions import ProxyError
try:
    from ps_setup import table
except:
    from housingData.ps_setup import table
import os
import time


class ps_proxy:
    def __init__(self):
        self.country = ""
        self.state = ""
        self.city = ""
        self.zipcode = ""
        self.timezone = ""
        self.isp = ""
        self.org = ""
        self.query = ""
        self.db = table()
        # print('proxy start')
    def __del__(self):
        self.db.__del__()
        # print('proxy end')


    def save(self,host,port,user=None,password=None,type=None):
        return self.db.proxy_insert(host,port,user,password,type)
    
    def update(self, info):
        

        return True

    def delete(self, id):
       return self.db.delete('proxy',id)
        

    def get(self,host,port):
       return self.db.proxy_first(host=host,port=port)
    def getAll(self):
       return self.db.proxy_all()
    def exist(self,host,port):
        print('exist proxy')
        
        try:
            proxy = self.get(host=host,port=port)
           
            if proxy == None:
                proxy_data = {'host':host,'port':port}
                if self.proxy_check(data=proxy_data):
                    # print('proxy good')
                    self.save(host=host,port=port)
                    proxy = self.get(host=host,port=port)
                else:
                    return False
            else:
                print('db proxy',proxy)
                return proxy
        except Exception as e:
            print(e)
            return False

    def proxy_check(self, data,url='http://ip-api.com/json'):
        starttime=datetime.now()
        
        try:
            if 'user' in data:
                d = "{}://{}:{}@{}:{}".format(data['type'],data['user'],data['password'], data['host'], data['port'])
            else:
                d = "{}://{}:{}".format(data['type'],data['host'], data['port'])
            proxie = {"http": d, "https": d}
            # print(proxie)
            r = requests.get(url, timeout=10, proxies=proxie,allow_redirects=True)
            
            # ip = json.loads(r.text)
            # if "success" in ip or 
            # print('status_code', r.status_code)
            if r.status_code==200:
                pass
                # print('proxy good')
                # print(ip)
                # self.country = ip['country']
                # self.state =ip['regionName']
                # self.city = ip['city']
                # self.zipcode = ip['zip']
                # self.timezone = ip['timezone']
                # self.isp = ip['isp']
                # self.org = ip['isp']
                # self.query = ip['query']
                t = (datetime.now()-starttime).total_seconds()
                # print('proxy check time in second: {0}'.format(t))
                return True
            else:
                t = (datetime.now()-starttime).total_seconds()
                # print('proxy error time in second: {0}'.format(t))
                return False
        except Exception as e:
            #print(e)
            # print('proxy error in check')
            return False
    def use(self):
        activeproxy=None
        for i in self.getAll():
            if self.proxy_check(i,url='https://auburn.craigslist.org'):
                if 'user' in i:
                    proxy = "{}://{}:{}@{}:{}".format(i['type'],i['user'],i['password'], i['host'], i['port'])
                else:
                    proxy = "{}://{}:{}".format(i['type'],i['host'], i['port'])
                activeproxy = {"http": proxy, "https": proxy}
                # print(activeproxy)
                break
        return activeproxy
             


if __name__ == "__main__":
    p = ps_proxy()
    print(p.getAll())
    # for i in p.getAll():
    #     check =p.proxy_check(i,url='https://geo.craigslist.org')
        
    #     if not check:
    #         pass
    #         # print('delete proxy')
    #         # p.delete(id=i['id'])
    #     else:
    #         print(check)
    #         print('proxy good')
	
