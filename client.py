import requests

test_file = open("my_file.txt", "rb")
test_url = "http://192.168.56.1:80"
data_headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

try:
        post = requests.post(test_url,  files = {"form_field_name": test_file})
        print(post.status_code)
except ConnectionError as e:
        print("CONNECTION ERROR: ")
        print(e)