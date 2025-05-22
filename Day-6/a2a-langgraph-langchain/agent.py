from dotenv import load_dotenv
from langchain_core.tools import tool
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from collections.abc import AsyncIterable
from typing import Any, Literal, Dict
from pydantic import BaseModel
import httpx
import os
from langchain_core.messages import AIMessage, ToolMessage

load_dotenv()

memory = MemorySaver()

class ResponseFormat(BaseModel):
    """Respond to the user in this format."""

    status: Literal['input_required', 'completed', 'error'] = 'input_required'
    message: str


@tool
def rag(query: str) -> str:
    """
    Use this tool to search for product information.
    """
    if "iphone" in query.lower():
        return "iPhone is a smartphone brand owned by Apple Inc. It is known for its innovative design, high-quality hardware, and user-friendly interface."
    else:
        return "I'm sorry, I don't have information about that product."

@tool
def shop_information_rag():
    """
    Use this tool to search for shop information.
    """
    return [
        {
        "address": "89 Đ. Tam Trinh, Mai Động, Hoàng Mai, Hà Nội 100000, Vietnam",
        "maps_url": "https://maps.app.goo.gl/SitTbiYwUpu8jpeRA",
        "opening_hours": "8:30 AM–9:30 PM"
        },
        {
        "address": "27A Nguyễn Công Trứ, Phạm Đình Hổ, Hai Bà Trưng, Hà Nội 100000, Vietnam",
        "maps_url": "https://maps.app.goo.gl/3L7iSHpbHawsEaTx9",
        "opening_hours": "8:30 AM–9:30 PM"
        },
        {
        "address": "392 Đ. Trương Định, Tương Mai, Hoàng Mai, Hà Nội, Vietnam",
        "maps_url": "https://maps.app.goo.gl/torAE2bHddW6nMPq9",
        "opening_hours": "8:30 AM–9:30 PM"
        }
    ]


class LangGraphAgent:
    SYSTEM_INSTRUCTION = (
        'You are a helpful assistant that can search for product information and provide shop details. '
        "Your purpose is to use the 'rag' tool to search for product information and the 'shop_information_rag' tool to provide shop locations and details. "
        'You can help users find product information, shop addresses, opening hours, and location maps. '
        'Use the rag tool when users ask about products or need to search for specific information. '
        'Use the shop_information_rag tool when users ask about shop locations, addresses, opening hours, or directions. '
        'Set response status to input_required if the user needs to provide more information. '
        'Set response status to error if there is an error while processing the request. '
        'Set response status to completed if the request is complete.'
    )
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model='gemini-2.0-flash',
            google_api_key=os.getenv('GOOGLE_API_KEY')
        )
        self.tools = [rag, shop_information_rag]

        self.graph = create_react_agent(
            self.model,
            tools=self.tools,
            checkpointer=memory,
            prompt=self.SYSTEM_INSTRUCTION,
            response_format=ResponseFormat,
        )

    def invoke(self, query, sessionId) -> str:
        config = {'configurable': {'thread_id': sessionId}}
        self.graph.invoke({'messages': [('user', query)]}, config)
        return self.get_agent_response(config)
    
    async def stream(self, query, sessionId) -> AsyncIterable[Dict[str, Any]]:
        inputs = {'messages': [('user', query)]}
        config = {'configurable': {'thread_id': sessionId}}

        for item in self.graph.stream(inputs, config, stream_mode='values'):
            message = item['messages'][-1]
            if (
                isinstance(message, AIMessage)
                and message.tool_calls
                and len(message.tool_calls) > 0
            ):
                yield {
                    'is_task_complete': False,
                    'require_user_input': False,
                    'content': 'Looking up product or shop information...',
                }
            elif isinstance(message, ToolMessage):
                yield {
                    'is_task_complete': False,
                    'require_user_input': False,
                    'content': 'Processing product or shop information...',
                }

        yield self.get_agent_response(config)

    def get_agent_response(self, config):
        current_state = self.graph.get_state(config)
        structured_response = current_state.values.get('structured_response')
        if structured_response and isinstance(
            structured_response, ResponseFormat
        ):
            if structured_response.status == 'input_required':
                return {
                    'is_task_complete': False,
                    'require_user_input': True,
                    'content': structured_response.message,
                }
            elif structured_response.status == 'error':
                return {
                    'is_task_complete': False,
                    'require_user_input': True,
                    'content': structured_response.message,
                }
            elif structured_response.status == 'completed':
                return {
                    'is_task_complete': True,
                    'require_user_input': False,
                    'content': structured_response.message,
                }

        return {
            'is_task_complete': False,
            'require_user_input': True,
            'content': 'We are unable to process your request at the moment. Please try again.',
        }

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']
