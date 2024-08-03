from fastapi import APIRouter, HTTPException, Body
from typing import List, Union, Dict, Optional
from typing_extensions import Annotated
from pydantic import BaseModel, validator, Field

from langchain_community.llms.moonshot import Moonshot
from langchain.memory import ChatMessageHistory
from langchain.schema import messages_from_dict
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


moonshot_api = APIRouter()

class Basedata(BaseModel):
    """Base abstract message class.

    Messages are the inputs and outputs of ChatModels.
    """

    content: Union[str, List[Union[str, Dict]]] = Field(title="具体的聊天记录，用str类型输入", examples=["A very nice Item"])
    """The string contents of the message."""

    additional_kwargs: dict = Field(default_factory=dict, description="为与信息相关的附加有效载荷数据预留，默认是空字典")
    """Reserved for additional payload data associated with the message.
    
    For example, for a message from an AI, this could include tool calls as
    encoded by the model provider.
    """

    type: str = Field(description="该条聊天记录所属的角色，str类型,用户:human, 大模型: ai ")
    """The type of the message. Must be a string that is unique to the message type.
    
    The purpose of this field is to allow for easy identification of the message type
    when deserializing messages.
    """

    name: Optional[str] =Field(None, description="This can be used to provide a human-readable name for the message. 默认值为None")
    """An optional name for the message. 
    
    This can be used to provide a human-readable name for the message.
    
    Usage of this field is optional, and whether it's used or not is up to the
    model implementation.
    """

    id: Optional[str] = Field(None, description="An optional unique identifier for the message. 默认为None")
    """An optional unique identifier for the message. This should ideally be
    provided by the provider/model which created the message."""

    example: bool = False

class BaseMessage(BaseModel):
    type: str
    data: Basedata

class InfoModel(BaseModel):
    memory:  List[BaseMessage] = None
    model_api: str
    question: str
    with_memory: bool
    
    
########### 测试记忆功能 #######
# {
#   "memory": [
#     {
#       "type": "human",
#       "data": {
#         "content": "你是谁",
#         "additional_kwargs": {},
#         "type": "human",
#         "name": "",
#         "id": "",
#         "example": false
#       }
#     }
#   ],
#   "model_api": "sk-4BHsQGMl5LT1YozusMlPesj3AN1cn4pyPDmdsWbeBKy84nyF",
#   "question": "我回来了",
#   "with_memory": true
# }


    
@moonshot_api.post("/moonshot/{ueser_id}")
async def request_api(ueser_id:str, 
                      info: Annotated[
                          InfoModel,
                          Body(
                              examples = [
                               {"memory": [
                                    {
                                    "type": "该条信息来源, 属于人:human, 属于大模型:ai", ##是人就填入human 
                                    "data": {
                                        "content": "消息的具体内容",
                                        "additional_kwargs": {"默认为空，无需填写"},
                                        "type": "该条信息来源, 属于人:human, 属于大模型:ai",
                                        "name": "默认为空，无需填写",
                                        "id": "默认为空，无需填写",
                                        "example": False
                                    }
                                    }
                                ],
                                "model_api": "传入模型的api key",
                                "question": "传入当前问题",
                                "with_memory": True
                                }
                               ],
                          ),
                      ],
                      ):
    moonshot_model = Moonshot(api_key=info.model_api, model="moonshot-v1-8k")

    if(info.with_memory is True):
        infos = [i.dict() for i in info.memory]
        new_message = messages_from_dict(messages=infos)
        retrieved_chat_history = ChatMessageHistory(messages=new_message)
        retrieved_memory = ConversationBufferMemory(chat_memory=retrieved_chat_history)
        messages_from_dict
        conversation_reload = ConversationChain(
            llm=moonshot_model, 
            verbose=True, 
            memory=retrieved_memory
        )
        try:
            response = conversation_reload.predict(input=info.question)
        except Exception as e:
            raise HTTPException(code="404", detail=e)
    else:    
        response = moonshot_model.invoke(info.question)

   

    return {"type": "ai", "content": response}