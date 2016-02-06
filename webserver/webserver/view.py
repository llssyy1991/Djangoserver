from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId

from pymongo import MongoClient

# Open database connection


client = MongoClient()
db = client.kaoyu


def login(request):
	name=request.GET['username'].encode('utf-8')
	password=request.GET['password'].encode('utf-8')
	cursor.execute('select * from userInfo where name="'+name+'"')
	data=cursor.fetchall()
	if data[0][1]==password:
		return HttpResponse("OK")
	return HttpResponse("NO")

@csrf_exempt
def getmenu(request):
	password=request.POST['password']
	email=request.POST['email']
	user_sign={'password':password,'email':email}
	db.user.insert_one(user_sign)
	result=db.user.find({"_id":ObjectId("56b544ff7217ac2182e0e3ad")})
	print result[0]
	return HttpResponse(str(user_sign))	
