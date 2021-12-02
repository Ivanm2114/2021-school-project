from requests import get, post


print(post('http://127.0.0.1:5000', json={
    "ShowMessage": True,
    "TextMessage": "Тут многострочная строка для выведения на экран",
    "QR": "Тут текст QR кода"
}).json())
