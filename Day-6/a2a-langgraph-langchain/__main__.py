import logging
import os

import click
import httpx

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore, InMemoryPushNotifier
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent import LangGraphAgent
from agent_executor import RAGAgentExecutor
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""

    pass


@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=10000)
def main(host, port):
    """Starts the Currency Agent server."""
    try:
        if not os.getenv('GOOGLE_API_KEY'):
            raise MissingAPIKeyError(
                'GOOGLE_API_KEY environment variable not set.'
            )

        capabilities = AgentCapabilities(streaming=True, pushNotifications=True)
        product_search_skill = AgentSkill(
            id='search_product',
            name='Search Product',
            description='Helps with search product information',
            tags=['search product', 'product information'],
            examples=['Cho tôi thông tin điện thoại?'],
        )

        shop_information_skill = AgentSkill(
            id='shop_information',
            name='Shop Information',
            description='Helps with search shop information',
            tags=['shop information', 'shop information'],
            examples=['Cho tôi thông tin cửa hàng?'],
        )

        agent_card = AgentCard(
            name='RAG Agent',
            description='Helps with search product information and shop information',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            defaultInputModes=LangGraphAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=LangGraphAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[product_search_skill, shop_information_skill],
        )

        httpx_client = httpx.AsyncClient()
        request_handler = DefaultRequestHandler(
            agent_executor=RAGAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_notifier=InMemoryPushNotifier(httpx_client),
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )
        import uvicorn

        uvicorn.run(server.build(), host=host, port=port)
    except MissingAPIKeyError as e:
        logger.error(f'Error: {e}')
        exit(1)
    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        exit(1)


if __name__ == '__main__':
    main()