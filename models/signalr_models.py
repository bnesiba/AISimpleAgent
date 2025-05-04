
class SignalRIdentity(dict):
    def __init__(self, type: str, id: str):
        self.type = type
        self.id = id

    def GetString(self) -> str:
        return self.type + self.id
    
    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "id": self.id
        }
    

class SignalRMessageRequest(dict):

    def __init__(self, identities: list[SignalRIdentity], type: str, payload: str):
        self.identities = identities
        self.type = type
        self.payload = payload

    def to_dict(self) -> dict:
        identities_dict_list = [identity.to_dict() for identity in self.identities]
        return {
            "identities": identities_dict_list,
            "type": self.type,
            "payload": self.payload
        }
