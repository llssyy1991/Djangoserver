from django.http import HttpResponse

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","lsylsy2008","test" )
cursor=db.cursor()


def hello(request):
	name=request.GET['username'].encode('utf-8')
	password=request.GET['password'].encode('utf-8')
	cursor.execute('select * from userInfo where name="'+name+'"')
	data=cursor.fetchall()
	if data[0][1]==password:
		return HttpResponse("OK")
	return HttpResponse("NO")
