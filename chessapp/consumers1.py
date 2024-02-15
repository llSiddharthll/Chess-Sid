import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .chess_logic import ChessLogic  # Make sure you have the appropriate import for ChessLogic

class ChessConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['room_id']
        self.user_id = self.scope['user'].id
        self.chess_logic = ChessLogic()

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
                'message': f'Player {self.user_id} has joined.',
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
                'message': f'Player {self.user_id} has left.'
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        move_type = data['type']
        print(data)
        # Handle different types of messages
        if move_type == 'make_move':
            move = data['move']
            move_uci = move.get('source')+move.get('target')
            on_drop = self.chess_logic.on_drop(move_uci)
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'game_move',
                    'message': f'Player {self.user_id} is dragging a piece.',
                    'on_drop': on_drop
                }
            )
        elif move_type == 'hover':
            hover = data['hover']
            piece = hover.get('piece')
            possible_moves = self.chess_logic.get_possible_moves(piece)
            await self.send(text_data=json.dumps({
            'type': 'possible_moves',
            'possible_moves': possible_moves,
        }))
            
    async def game_message(self, event):
        move_message = event['message']

        # Send move message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'game_move',
            'move_message': move_message,
        }))
    async def game_move(self, event):
        move_message = event['message']
        on_drop = event['on_drop']

        # Send move message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'game_move',
            'move_message': move_message,
            'on_drop': on_drop,
        }))