from requests import get, post


print(post('http://localhost:5000/', json={
    "ShowMessage": False,
    "TextMessage": "Тут многострочная строка для выведения на экран",
    "QR": "Тут текст QR кода"
}).json())
