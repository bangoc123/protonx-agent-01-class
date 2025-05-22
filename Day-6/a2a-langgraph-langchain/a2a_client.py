import asyncio
import base64
import os
import urllib
import httpx

from uuid import uuid4

import asyncclick as click

from a2a.client import A2AClient, A2ACardResolver
from a2a.types import (
    Part,
    TextPart,
    FilePart,
    FileWithBytes,
    Task,
    TaskState,
    Message,
    MessageSendConfiguration,
    SendMessageRequest,
    MessageSendParams,
    GetTaskRequest,
    TaskQueryParams,
)


@click.command()
@click.option('--agent', default='http://localhost:10000')
@click.option('--session', default=0)
@click.option('--history', default=False)
@click.option('--use_push_notifications', default=False)
@click.option('--push_notification_receiver', default='http://localhost:5000')
async def cli(
    agent,
    session,
    history,
    use_push_notifications: bool,
    push_notification_receiver: str,
):
    async with httpx.AsyncClient(timeout=30) as httpx_client:
        card_resolver = A2ACardResolver(httpx_client, agent)
        card = await card_resolver.get_agent_card()

        print('======= Agent Card ========')
        print(card.model_dump_json(exclude_none=True))

        notif_receiver_parsed = urllib.parse.urlparse(
            push_notification_receiver)
        notification_receiver_host = notif_receiver_parsed.hostname
        notification_receiver_port = notif_receiver_parsed.port

        client = A2AClient(httpx_client, agent_card=card)

        continue_loop = True

        while continue_loop:
            print('=========  starting a new task ======== ')
            continue_loop, contextId, taskId = await completeTask(
                client,
                use_push_notifications,
                notification_receiver_host,
                notification_receiver_port,
                None,
                None,
            )

            if history and continue_loop:
                print('========= history ======== ')
                task_response = await client.get_task(
                    {'id': taskId, 'historyLength': 10}
                )
                print(
                    task_response.model_dump_json(
                        include={'result': {'history': True}}
                    )
                )


async def completeTask(
    client: A2AClient,
    use_push_notifications: bool,
    notification_receiver_host: str,
    notification_receiver_port: int,
    taskId,
    contextId,
):
    prompt = click.prompt(
        '\nWhat do you want to send to the agent? (:q or quit to exit)'
    )
    if prompt == ':q' or prompt == 'quit':
        return False, None, None

    message = Message(
        role='user',
        parts=[TextPart(text=prompt)],
        messageId=str(uuid4()),
        taskId=taskId,
        contextId=contextId,
    )

    file_path = click.prompt(
        'Select a file path to attach? (press enter to skip)',
        default='',
        show_default=False,
    )
    if file_path and file_path.strip() != '':
        with open(file_path, 'rb') as f:
            file_content = base64.b64encode(f.read()).decode('utf-8')
            file_name = os.path.basename(file_path)

        message.parts.append(
            Part(
                root=FilePart(
                    file=FileWithBytes(
                        name=file_name, bytes=file_content
                    )
                )
            )
        )

    payload = MessageSendParams(
        id=str(uuid4()),
        message=message,
        configuration=MessageSendConfiguration(
            acceptedOutputModes=['text'],
        ),
    )

    taskResult = None
    message = None
    
    try:
        # Send message and get response
        event = await client.send_message(
            SendMessageRequest(
                id=str(uuid4()),
                params=payload,
            )
        )
        event = event.root.result
    except Exception as e:
        print("Failed to complete the call", e)
        return False, contextId, taskId
        
    if not contextId:
        contextId = event.contextId
    if isinstance(event, Task):
        if not taskId:
            taskId = event.id
        taskResult = event
    elif isinstance(event, Message):
        message = event

    if message:
        print(f'\n{message.model_dump_json(exclude_none=True)}')
        return True, contextId, taskId
    if taskResult:
        # Don't print the contents of a file.
        task_content = taskResult.model_dump_json(
            exclude={
                "history": {
                    "__all__": {
                        "parts": {
                            "__all__" : {"file"},
                        },
                    },
                },
            },
            exclude_none=True,
        )
        print(f'\n{task_content}')
        ## if the result is that more input is required, loop again.
        state = TaskState(taskResult.status.state)
        if state.name == TaskState.input_required.name:
            return await completeTask(
                client,
                use_push_notifications,
                notification_receiver_host,
                notification_receiver_port,
                taskId,
                contextId,
            )
        ## task is complete
        return True, contextId, taskId
    ## Failure case, shouldn't reach
    return True, contextId, taskId


if __name__ == '__main__':
    asyncio.run(cli())