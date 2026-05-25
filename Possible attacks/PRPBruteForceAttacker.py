import requests

url = "http://127.0.0.1:5000/secure_with_logging/login"

passwords = [
    "123456",
    "password",
    "welcome",
    "admin",
    "secret123",
    "admin1234",
    "admin123"
]

for password in passwords:
    response = requests.post(url, json={
        "email": "admin@test.com",
        "password": password
    })

    print(f"Trying: {password}")
    print(response.text)
