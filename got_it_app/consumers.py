from channels.generic.websocket import AsyncWebsocketConsumer
import json

class RoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'reset_message',
                'tester': 'hello world'
            }
        )

    async def tester_message(self, event):
        tester = event['tester']

        await self.send(text_data=json.dumps({
            'tester': tester,
        }))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'text1' in text_data_json:
            text1 = text_data_json['text1']
            # text2 = text_data_json['text2']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'text1_message',
                    'text1': text1,
                    # 'text2': text2
                }
            )
        elif 'text2' in text_data_json:
            text2 = text_data_json['text2']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'text2_message',
                    'text2': text2,
                }
            )
        elif 'reset' in text_data_json:

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'reset_message',
                    'reset': 'reset_msg'
                }
            )
        
    async def text1_message(self, event):
        text1 = event['text1']
        # text2 = event['text2']

        await self.send(text_data=json.dumps({
            'text1': text1,
            # 'text2': text2
        }))

    async def text2_message(self, event):
        text2 = event['text2']

        await self.send(text_data=json.dumps({
            'text2': text2,
        }))

    async def reset_message(self, event):
        # text2 = event['text2']

        await self.send(text_data=json.dumps({
            'reset': None,
            'text1': None,
            'text2': None
        }))

    pass