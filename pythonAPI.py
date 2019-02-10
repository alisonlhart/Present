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
        uID, = cur.fetchone()
        if(uID == None):
            uID = 0
        else:
            uID+=1
        uFname = request.form['fname']
        uLname = request.form['lname']
        cur.execute("INSERT INTO studentdata (data, id, fname, lname) VALUES (%s, %s, %s, %s)", (uData, uID, uFname, uLname)) #Place data from post into db
        postgreClient.commit()
        return("Post success. uData = {}, uID = {}, uFname = {}, uLname = {}".format(uData, uID, uFname, uLname))
    else:
        cur.execute("SELECT * FROM attendance")         #get attendance record
        send = ""
        while(True):
            row = cur.fetchone()
            if(row == None):
                break
            else:
                row = list(row)
                for i in range(0, len(row)):                    #compile rows into long string delimited by \n
                    send += str(row[i])
                if i+1 in range(0, len(row)):
                    send += ','
                send+="\n"
        return send

app.run(debug = True)
