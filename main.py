#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import tornado.ioloop
import tornado.web   

import requests,random,json
from pylsy import pylsytable


a=""     
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")
    def post(self,*args,**kwargs):
        name=self.get_argument('username')
        pwd=self.get_argument('pwd')
        print(name)
        
        url ='https://api.bmob.cn/1/classes/_User?where={"username":"%s"}' %(name)

        headers={
    "X-Bmob-Application-Id":"af52ed9648d1561c127a2e30072f247f",
    "X-Bmob-REST-API-Key":"84f679fa3b4efb43314433887adcf103",
    # "Content-Type":"application/json"
        }
        a=requests.get(url,headers=headers)
        su=a.json()
        print(su)
        
        if pwd==su['results'][0]['pwd']:
            url2 ='https://api.bmob.cn/1/classes/_User'
            su2=requests.get(url2,headers=headers).json()
            #self.write(f'<h1>登录成功</h1>{str(su2)}')
            self.render("1.html",name=su['results'][0]['username'],email=su['results'][0]['email'],li=[i['username'] for i in su2['results']])
            
            
            
            
        else:
            self.write('<h1>登录失败,帐号或密码错误</h1>')
class InstallHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("install.html")
    def post(self,*args,**kwargs):
        name=self.get_argument('name')
        pwd=self.get_argument('pwd')
        email=self.get_argument('email')
        print(name)       
        a=f'<h1>用户:{name},注册成功</h1>'
    #    self.redirect("/login")  
        headers={
    "X-Bmob-Application-Id":"af52ed9648d1561c127a2e30072f247f",
    "X-Bmob-REST-API-Key":"84f679fa3b4efb43314433887adcf103",
     "Content-Type":"application/json"
             }
        data=	{
           "username":name,
           "password":pwd,
          	"pwd":pwd,
           "email":email
        	}
        url = 'https://api.bmob.cn/1/classes/_User'
        a=requests.post(url,data=json.dumps(data),headers=headers)
        j=a.json()
        print(j)
        
        if  "error" in [i for i in j.keys()]:
             print(j)
             print("错误")
             self.write(f'<h1>用户:{name},注册失败<br>原因:{str(j["error"])}</h1>')
    
        else:
            self.write(f'<h1>用户:{name},注册成功<br><a href="/login">点击跳转登录</a></h1>')
    
        
        
        
application = tornado.web.Application([
    (r"/login", MainHandler),
    (r"/install", InstallHandler),
    
])
   
   
if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()