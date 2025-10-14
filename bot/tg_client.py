import json
import urllib.request
import os
from dotenv import load_dotenv

load_dotenv()

def makeRequest(method: str, **param) -> dict:
    json_data = json.dumps(param).encode('utf-8')

    request = urllib.request.Request(
        method='POST',
        url= f"{os.getenv('TELEGRAM_BASE_URI')}/{method}",
        data=json_data,
        headers={
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode('utf-8')
        response_json = json.loads(response_body)
        assert response_json["ok"] == True
        return response_json["result"]


def getUpdates(offset: int) -> dict:
    return makeRequest('getUpdates', offset=offset)
    
def sendMessage(chat_id: int, text: str) -> dict:
    return makeRequest('sendMessage', chat_id=chat_id, text=text)
    
def getMe() -> dict:
    return makeRequest('getMe')
