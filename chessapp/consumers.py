# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from channels.db import database_sync_to_async
import logging
from django.db.models import F


logger = logging.getLogger(__name__)

class ChessConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['room_id']
        self.user_id = self.scope['user'].id

        # Generate the game group name based on the game_id
        self.game_group_name = f'game_{self.game_id}'

        # Join the game group
        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )
        
        await self.accept()

        # Notify the group when someone joins
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'game_message',
                'message': f'A Player has joined.',
            }
        )
        
    async def disconnect(self, close_code):
        # Leave the game group
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

        # Notify the group when someone leaves
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'game_message',
                'message': f'A Player has left.'
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        move_type = data['type']

        # Handle different types of messages
        if move_type == 'on_Drag':
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'game_message',
                    'message': f'Player {self.user_id} is dragging a piece.'
                }
            )
        elif move_type == 'on_Drop':
            source, target = data['sum'][:2], data['sum'][2:]
            self.move_message = f'{source}-{target}'
            print(self.move_message)
            
            # Send move to game group
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'game_move',
                    'move_message': f'Player {self.user_id} moved {self.move_message}',
                    'movement': source + target,
                }
            )
        elif move_type == 'fen':
            await self.handle_fen(data)
        
        elif move_type == 'result':
            instance = await database_sync_to_async(Game.objects.get)(id=self.game_id)
            result = data.get('msg')

            if result == 'black' and instance.creator.userprofile.selected_side == result:
                instance.creator.userprofile.matches_won = F('matches_won') + 1
            elif result == 'white' and instance.creator.userprofile.selected_side == result:
                instance.creator.userprofile.matches_won = F('matches_won') + 1

            instance.creator.userprofile.matches_played = F('matches_played') + 1

            if result == 'draw':
                instance.creator.userprofile.matches_draw = F('matches_draw') + 1

            await database_sync_to_async(instance.creator.userprofile.save)()
            await database_sync_to_async(instance.opponent.userprofile.save)()
            

    async def game_move(self, event):
        move_message = event['move_message']
        movement = event['movement']

        # Send move message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'game_move',
            'move_message': move_message,
            'movement': movement
        }))

    async def game_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'game_message',
            'message': message
        }))
        
    async def handle_fen(self, data):
        try:
            fen = data.get('fen')
            instance = await database_sync_to_async(Game.objects.get)(id=self.game_id)
            instance.fen = fen
            await database_sync_to_async(instance.save)()
        except Game.DoesNotExist:
            logger.error(f"Game with id {self.game_id} does not exist.")
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
        
