from enum import Enum
import json
from pydantic import BaseModel
import requests
import urllib3

from models.signalr_models import SignalRIdentity, SignalRMessageRequest

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class MessageChunk(BaseModel):
    message_id: str
    content: str
    fullContent: str
    metadata: list[str] = []
    is_complete: bool

class SignalREvents(Enum):
    Message_Start = "message-start"
    MESSAGE_UPDATE = "message-update"
    MESSAGE_METADATA = "message-metadata"
    MESSAGE_COMPLETE = "message-complete"
    

class SignalRService:

    @staticmethod
    def send(sessionId, data, msgType =SignalREvents.MESSAGE_UPDATE.value):
        broadcastUrl = "https://localhost:7240/broadcastToGroup"
        # identity = SignalRIdentity(type="Testy", id="Test") #TODO: use sessionId instead of test data
        identity = SignalRIdentity(type="Session", id=sessionId) 
        message = SignalRMessageRequest(identities=[identity], type=msgType, payload=data)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        try:
            result = requests.post(broadcastUrl, data=json.dumps(message.to_dict()), headers=headers, verify=False)
            return result.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error sending message to SignalR server: {e}")
            return True