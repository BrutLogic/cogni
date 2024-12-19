from typing import Union
from ..entities import Conversation, Message

def llm(conversation: Union[Conversation, str], model: str = "mock_llm") -> Union[Conversation, str]:
    """Process input through an LLM model.
    
    Args:
        conversation: Input conversation or string
        model: Name of LLM model to use
        
    Returns:
        Processed conversation or string
    """
    if model == "mock_llm":
        if isinstance(conversation, str):
            return f"you told {conversation}"
        else:
            last_msg = conversation[-1]
            conversation.add_message("assistant", f"you told {last_msg.content}")
            return conversation
            
    # Add other model implementations here
    raise NotImplementedError(f"Model {model} not implemented")
