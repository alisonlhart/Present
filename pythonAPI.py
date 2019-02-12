from flask import Flask, request, jsonify
import psycopg2
import sys
import traceback

try:
	postgreClient = psycopg2.connect(host="localhost", database="studentinfo", user="postgres", password="postgreS")
	cur = postgreClient.cursor()

except psycopg2.Error as e:
	print("Could not connect to postgres!")
	print(e)
	print(e.pgcode)
	print(e.pgerror)
	print(traceback.format_exc())
	sys.exit()

app = Flask(__name__)
@app.route('/', methods=['POST', 'GET', 'DELETE', 'PUT'])		#get connection type
def result():
	if(request.method == 'POST'):
		cur.execute("SELECT MAX(id) FROM studentdata;")
		uData = request.form['data']			#parse data into vars for db upload
		uID, = cur.fetchone()
		if(uID == None):
			uID = 0
		else:
			uID+=1
		uFname = request.form['fname']
		uLname = request.form['lname']
		cur.execute("INSERT INTO studentdata (data, id, fname, lname) VALUES (%s, %s, %s, %s);", (uData, uID, uFname, uLname)) #Place data from post into db
		postgreClient.commit()
		return("Post success. uData = {}, uID = {}, uFname = {}, uLname = {}".format(uData, uID, uFname, uLname))

	elif(request.method == 'GET'):
		cur.execute("SELECT studentdata.fname as FirstName, studentdata.lname as LastName, coalesce(attendance.present, 0) as Present FROM studentdata LEFT JOIN attendance on (studentdata.fname = attendance.fname AND studentdata.lname = attendance.lname);")
		send = []
		for row in cur.fetchall():
			send.append(row)
		return jsonify(send)

	elif(request.method == "DELETE"):
		cur.execute("SELECT id, fname, lname, data FROM studentdata;")
		send = []
		for row in cur.fetchall():
			send.append(row)
		return jsonify(send)
	
	else:	
		cur2 = postgreClient.cursor()
		uData = request.json['data']
		for dick in uData:
			cur.execute("SELECT * FROM attendance WHERE fname = %s AND lname = %s;", (dick['fname'], dick['lname']))
			cur.execute("INSERT INTO attendance (present, fname, lname) VALUES (%s, %s, %s);", (1, dick['fname'], dick['lname']))
			postgreClient.commit()

		return ""

app.debug = True
app.run(port=80, host='0.0.0.0')
