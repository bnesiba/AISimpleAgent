
class AgentMessageReference(dict):
    def __init__(self, title:str, url: str ):
        self.title = title
        self.url = url

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url
        }
    
class AgentMessageMetadata(dict):
    def __init__(self, metadataType: str, payload: dict):
        self.metadataType = metadataType
        self.payload = payload


@staticmethod
def ref_to_dict(ref: AgentMessageReference) -> dict:
        return {
            "title": ref["title"],
            "url": ref["url"]
        }

@staticmethod
def metadata_to_dict(metadata: AgentMessageMetadata) -> dict:
    return {
        "metadataType": metadata["metadataType"],
        "payload": metadata["payload"]
    }

class AgentMessage(dict):
    def __init__(self, message: str, sessionId: str, chatReferences: list[AgentMessageReference] = [], metadata: list[AgentMessageMetadata] = []):
        self.message = message
        self.sessionId = sessionId
        self.chatReferences = chatReferences
        self.metadata = metadata

    
    def to_dict(self) -> dict:
        return {
            "message": self.message,
            "sessionId": self.sessionId,
            "chatReferences": [ref_to_dict(ref) for ref in self.chatReferences],
            "metadata": [metadata_to_dict(meta) for meta in self.metadata]
        }

@staticmethod
def merge_ref_lists(list1: list[AgentMessageReference], list2: list[AgentMessageReference]) -> list[AgentMessageReference]:
    """Merge two lists into a single list. Clear out when list2 is empty."""
    if(list2 == []):
          return []
    
    return list1 + list2