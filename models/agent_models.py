
class AgentMessageReference(dict):
    def __init__(self, title:str, url: str ):
        self.title = title
        self.url = url

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url
        }

@staticmethod
def ref_to_dict(ref: AgentMessageReference) -> dict:
        return {
            "title": ref["title"],
            "url": ref["url"]
        }

class AgentMessage(dict):
    def __init__(self, message: str, sessionId: str, chatReferences: list[AgentMessageReference] = []):
        self.message = message
        self.sessionId = sessionId
        self.chatReferences = chatReferences

    
    def to_dict(self) -> dict:
        return {
            "message": self.message,
            "sessionId": self.sessionId,
            "chatReferences": [ref_to_dict(ref) for ref in self.chatReferences]
        }

@staticmethod
def merge_ref_lists(list1: list[AgentMessageReference], list2: list[AgentMessageReference]) -> list[AgentMessageReference]:
    """Merge two lists into a single list. Clear out when list2 is empty."""
    if(list2 == []):
          return []
    
    return list1 + list2