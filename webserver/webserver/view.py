from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId

from pymongo import MongoClient

import json

import ast

from datetime import datetime

# Open database connection


client = MongoClient()
db = client.kaoyu
@csrf_exempt
def get_order(request):
	order=request.body
	order_in=ast.literal_eval(order)
	email=order_in['email']
	date_time=datetime(int(order_in['year']),int(order_in['month']),int(order_in['day']),23,59,59)
	ordering=db.order_number.find_one()
	order_num=ordering["ord_n"]
	order_in['order']['ord_n']=order_num
	order_in['order']['date']=date_time
	order_in['order']['status']="INITIAL"
	plan=db.order_plan.find_one()
	BSKY=0
	PJNW=0
	ZTG=0
	if 'BSKY' in order_in['order']:
		if int(plan['plan']['BSKY'])==plan['plan']['BSKY_sold']:
			return HttpResponse('{"errorcode":"1"}')
		BSKY=1
	if 'PJNW' in order_in['order']:
		if int(plan['plan']['PJNW']) == plan['plan']['PJNW_sold']:
			return HttpResponse('{"errorcode":"2"}')
		PJNW=1
	if 'ZTG' in order_in['order']:
		if int(plan['plan']['ZTG']) == plan['plan']['ZTG_sold']:
			return HttpResponse('{"errorcode":"3"}')
		ZTG=1
	db.user.update({'email':email},{"$addToSet":{'order':order_in['order']}})	
	db.order_plan.update({},{"$inc":{"plan.BSKY_sold":BSKY,"plan.PJNW_sold":PJNW,"plan.ZTG_sold":ZTG}})
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

	user_data={"email":email,"password":password,"identity":"customer"}
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
	if password!=user_found['password']:
		return HttpResponse('{"errorcode":"2"}')
	if user_found['identity']=="chief":
		return HttpResponse('{"errorcode":"3"}')
	return HttpResponse('{"errorcode":"0"}')

@csrf_exempt

def setplan(request):
	req=request.body
	plan=ast.literal_eval(req)
	plan["BSKY_sold"]=0
	plan["PJNW_sold"]=0
	plan["ZTG_sold"]=0
	date_time=datetime(int(plan['year']),int(plan['month']),int(plan['day']),23,59,59)
	#date_time=datetime(1991,1,1,0,0,0)
	plan2=json.dumps(plan)
	print plan2
	plan["id"]="order_plan"
	db.order_plan.update({},{"$set":{"date_time":date_time,"plan":plan}})

	return HttpResponse(plan2)


@csrf_exempt
def show_menu(request):

	req=request.body
	plan=db.order_plan.find_one()
	start=datetime.now()
	if start>plan["date_time"]:
		return HttpResponse('{"result":"no plan"}')
		
	plan_return=json.dumps(plan["plan"])
	return HttpResponse(plan_return)

@csrf_exempt
def show_all_order_unfinished(request):
	plan=db.order_plan.find_one()
	start=datetime.now()
	if start>plan["date_time"]:
		return HttpResponse('{"result":"no plan setted"}')
	order_results=db.user.find({"order.date":plan["date_time"]})
	result=[]
	for orders in order_results:
		for order in orders["order"]:
			if order["date"]==plan["date_time"]:
				del order["date"]
				result.append(order)
	if not result:
		return HttpResponse('{"result":"No order sold"}')
	results=json.dumps(result)
	return HttpResponse('{"result":'+results+'}')

@csrf_exempt
def show_user_order(request):

	req = request.body
	email=ast.literal_eval(req)
	user=db.user.find_one({"email":email["email"]})
	result=[]
	for order in user["order"]:
		if "date" in order:
			order["year"]=order["date"].year
			order["month"]=order["date"].month
			order["day"]=order["date"].day
			del order["date"]
		result.append(order)
	results=json.dumps(result)
	return HttpResponse('{"result":'+results+'}')

@csrf_exempt
def change_order_status(request):
	req = request.body
	status = ast.literal_eval(req)
	order_num=status["order_num"]
	if status["status"] == "reject":
		order_delete=db.user.find_one({"order.ord_n":int(order_num)},{"order.$":1})
		print order_delete
		BSKY=0
		PJNW=0
		ZTG=0
		if 'BSKY' in order_delete["order"][0]:
			BSKY = -1
		if 'PJNW' in order_delete["order"][0]:
			PJNW = -1
		if 'ZTG' in order_delete["order"][0]:
			ZTG = -1
		db.order_plan.update({}, {"$inc": {"plan.BSKY_sold": BSKY, "plan.PJNW_sold": PJNW, "plan.ZTG_sold": ZTG}})
	db.user.update({'order.ord_n':int(order_num) }, {"$set": {'order.$.status': status["status"]}})
	return HttpResponse('{"result":"success"}')
