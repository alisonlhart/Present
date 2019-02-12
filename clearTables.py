import psycopg2
import sys

try:
	postgreClient = psycopg2.connect(host="localhost", database="studentinfo", user="postgres", password="postgreS")
	cur = postgreClient.cursor()

except:
	print("Could not connect to postgres!")
	sys.exit

cur.execute("DROP TABLE studentdata;DROP TABLE attendance;CREATE TABLE studentinfo (id int, data text, fname text, lname text);CREATE TABLE attendance (present int, fname text, lname text);")
