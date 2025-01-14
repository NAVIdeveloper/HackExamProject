import requests

BASE_URL = "http://127.0.0.1:8000"
API_CREATE_URL = f"{BASE_URL}/api/create/"
API_GET_URL = f"{BASE_URL}/api/get"

def Create_Question(text):
    res = requests.post(
        API_CREATE_URL,{'question':text}
    )
    return res.text

def Get_Answer(query):
    res = requests.get(
        f"{API_GET_URL}/{query}/"
    )
    return res.text
