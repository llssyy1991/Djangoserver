import requests
import json


URL='http://127.0.0.1/second/'

payload = {'password':"lisyuan",'email':'lisiyuan199105@gmail.com'}

r = requests.post(URL, data=payload)

print r.text
