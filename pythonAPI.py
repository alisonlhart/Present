from flask import Flask, request
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
@app.route('/', methods=['POST', 'GET'])                #get connection type
def result():
if(request.method == 'POST'):
    cur.execute("SELECT MAX(id) FROM studentdata")
    uData = request.form['data']                    #parse data into vars for db upload
    uID = cur.fetchone()
    uFname = request.form['fname']
    uLname = request.form['lname']
    cur.execute("INSERT INTO studentdata (chars, id, fname, lname) VALUES (%s, %d, %s, %s)", (uData, uID, uFname, uLname)) #Place data from post into db

else:
    cur.execute("SELECT * FROM attendance")         #get attendance record
    row = cur.fetchone()
    send = ""
    while(True):
        if(row == None):
            break
        for i in range(0, len(row)):                    #compile rows into long string delimited by \n
            send += row[i]
        send+="\n"
    return send

app.run()
