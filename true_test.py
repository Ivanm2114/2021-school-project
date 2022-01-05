from requests import get, post


print(post('http://127.0.0.1:5000', json={
    "ShowMessage": True,
    "TextMessage": "LOL",
    "QR": "Тут текст QR кода"
}).json())
