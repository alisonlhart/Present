import requests

#r = requests.post('http://34.73.48.217:80', data = {'data' : 'testdata123', 'fname' : 'Jeremy', 'lname' : 'Eudy'})
#print(r)
r = requests.get('http://34.73.48.217:80')
print(r.text)
