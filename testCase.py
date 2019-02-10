import requests

r = requests.post('http://34.73.48.217:5000', data = {'data' : 'testdata123', 'fname' : 'Jeremy', 'lname' : 'Eudy'})
print(r)
