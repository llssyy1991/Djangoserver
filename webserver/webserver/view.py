from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId

from pymongo import MongoClient

import json

import ast

# Open database connection


client = MongoClient()
db = client.kaoyu
@csrf_exempt
def get_order(request):
	order=request.body
	order_in=ast.literal_eval(order)
	email=order_in['email']
	ordering=db.order_number.find_one()
	order_num=ordering["ord_n"]
	db.user.update({'email':email},{"$addToSet":{'order':order_in['order']}})	
	db.order_number.update({},{"$inc":{'ord_n':1}})
	
	return HttpResponse('{"errorcode":"0","order_num":'+str(order_num)+'}')

@csrf_exempt
def login(request):
	user=request.body
        user_in=ast.literal_eval(user)
        password=user_in['password']
        email=user_in['email']
	if db.user.find_one({"email":email}) is not  None:

		
		return HttpResponse('{"errorcode":"1"}')

	user_data={"email":email,"password":password}
	
	db.user.insert_one(user_data)
	return HttpResponse('{"errorcode":"0"}')

@csrf_exempt
def getmenu(request):
	user=request.body
	user_in=ast.literal_eval(user)
	password=user_in['password']
	email=user_in['email']
	user_found=db.user.find_one({"email":email})
	if user_found is None:
		return HttpResponse('{"errorcode":"1"}')
	#user_info=ast.literal_eval(user_found)
	if password!=user_found['password']:
		return HttpResponse('{"errorcode":"2"}')
	return HttpResponse('{"errorcode":"0"}')
