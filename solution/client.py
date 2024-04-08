import requests

url="http://localhost/8000"

url_get=url+"/order" 
response=requests.request(method="GET", url=url_get)
print(response.text)


