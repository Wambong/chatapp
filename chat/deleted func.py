import json


async def websocket_receive(self, event):
    print('receive', event)
    received_data = json.loads(event['text'])
    msg = received_data.get('message')
    media_data = received_data.get('media')
    sent_by_id = received_data.get('sent_by')
    send_to_id = received_data.get('send_to')
    thread_id = received_data.get('thread_id')

    sent_by_user = await self.get_user_object(sent_by_id)
    send_to_user = await self.get_user_object(send_to_id)
    thread_obj = await self.get_thread(thread_id)

    if not sent_by_user:
        print('Error: Sent by user is incorrect')
        return False
    if not send_to_user:
        print('Error: Send to user is incorrect')
        return False
    if not thread_obj:
        print('Error: Thread id is incorrect')
        return False

    if msg:
        # Handle text message
        await self.create_chat_message(thread_obj, sent_by_user, msg=msg)

    if media_data:
        # Handle media file upload
        media_file = self.decode_base64_and_save(media_data)
        await self.create_chat_message(thread_obj, sent_by_user, media=media_file)

    other_user_chat_room = f'user_chatroom_{send_to_id}'
    self_user = self.scope['user']
    response = {
        'message': msg,
        'sent_by': self_user.id,
        'thread_id': thread_id
    }

    await self.channel_layer.group_send(
        other_user_chat_room,
        {
            'type': 'chat_message',
            'text': json.dumps(response)
        }
    )

    await self.channel_layer.group_send(
        self.chat_room,
        {
            'type': 'chat_message',
            'text': json.dumps(response)
        }
    )