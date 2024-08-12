import requests

response = requests.post(
    "http://127.0.0.1:5000/users", 
    json={"name": "Flask", "password": "1234558fff", "email": "aaa@ru.ru"}
)

# response = requests.post(
#     "http://127.0.0.1:5000/advertisement/", 
#     json={"title": "Hihi", "description": "Haha", "user_id": 1}
# )

# response = requests.get("http://127.0.0.1:5000/advertisement/1/")

# response = requests.patch(
#     "http://127.0.0.1:5000/advertisement/2/", json={"description": "Hehe"}, headers={"token": "ffdg4df5g4f8g4f5g24sd5"}
# )

# response = requests.get("http://127.0.0.1:5000/advertisement/1/")


# response = requests.delete("http://127.0.0.1:5000/advertisement/1/")

# response = requests.get("http://127.0.0.1:5000/advertisement/1/")


print(response.status_code)
print(response.json())
