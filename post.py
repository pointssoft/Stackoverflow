
from datetime import datetime
import json
import requests
from requests import exceptions
from requests.exceptions import ProxyError
try:
    from ps_setup import table
except:
    from housingData.ps_setup import table
import time


class ps_post:
    def __init__(self):
        self.site = ''
        self.location = ''
        self.price = ''
        self.housing = ''
        self.extra = ''
        self.images = ''
        self.body = ''
        self.post_time = ''
        self.url = ''
        self.title = ''
        self.db = table()
        # print('post obj start')

    def __del__(self):
        # print('post obj end')
        self.db.__del__()

    def set_data(self, site=None, location=None, price=None, housing=None, extra=None, images=None, body=None, post_time=None, url=None, title=None):
        self.site = site
        self.location = location
        self.price = price
        self.housing = housing
        self.extra = extra
        self.images = images
        self.body = body
        self.post_time = post_time
        self.title = title
        self.url = url

    def save_q(self,title,url):

        sql = ("INSERT INTO questions "
               "(title, url, status) "
               "VALUES (%s,%s, %s)")

        data = (title, url,1)
        # data = (self.title, self.site, self.location, self.price, self.housing,
                # self.extra, self.images, self.body, self.post_time, self.url)

        self.id = self.db.save(cols=sql, velus=data)
        return self.id

    def update(self, info):
        return True

    def delete(self, id):
        return self.db.delete('proxy', id)

    def check_url(self, url):
        return self.db.where(tbl='post', column='url', value=url)

    def getLink(self, limit=1):
        post = self.db.orderBy(
            tbl='sitelist', column='time', value='ASC', all=True)
        l = []
        for i in range(limit):
            post[i]
            now = datetime.now()
            ftime = now.strftime('%Y-%m-%d %H:%M:%S')
            self.db.update(tbl='sitelist', column='time',
                           value=ftime, id=post[i]['id'])
            l.append(post[i]['url'])

        return l

    def getAll(self):
        return self.db.where(tbl='post', column='status', value=0, all=True)

    def getAll_with_urls(self, urls):
        return self.db.whereIn(tbl='post', column='url', value=urls, all=True)

    def exist(self, host, port):

        try:
            proxy = self.get(host=host, port=port)

            if proxy == None:
                proxy_data = {'host': host, 'port': port}
                if self.proxy_check(data=proxy_data):
                    print('proxy good')
                    self.save(host=host, port=port)
                    proxy = self.get(host=host, port=port)
                else:
                    return False
            else:
                print('db proxy', proxy)
                return proxy
        except Exception as e:
            print(e)
            return False

    def use(self):
        activeproxy = None
        for i in self.getAll():
            if not self.proxy_check(i, url='https://auburn.craigslist.org'):
                self.delete(id=i['id'])
            else:
                activeproxy = i['host']+":"+i['port']
                break
        return activeproxy


if __name__ == "__main__":

    #  p = ps_post()
    #  print(p.getLink())
    # checkpost = p.getAll()
    # if checkpost == None:
    #     pass

    # else:
    #     print('post have')
    #     # print(checkpost)
    # pass
    import json
    from base64 import b64encode
    from Crypto.Cipher import ChaCha20
    from Crypto.Random import get_random_bytes
    plaintext = b'BpqhU0J566CU:jVjPbpO3ULB'
    key = get_random_bytes(32)
    cipher = ChaCha20.new(key=key)
    ciphertext = cipher.encrypt(plaintext)
    nonce = b64encode(cipher.nonce).decode('utf-8')
    ct = b64encode(ciphertext).decode('utf-8')
    result = json.dumps({'nonce': nonce, 'ciphertext': ct})
    print(result)
