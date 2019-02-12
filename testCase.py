import requests                                                                                                                                                     


#r = requests.post('http://localhost:5000', data = {'data' : 'testdata123', 'fname' : 'Jeremy', 'lname' : 'Eudy'})
r = requests.get('http://localhost:5000')
print(r.text)
