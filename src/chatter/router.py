from os import getenv
from fastapi import APIRouter, Request, WebSocket # HTTPException,
from fastapi.responses import HTMLResponse
from starlette_context import context 
from binance import AsyncClient, BinanceSocketManager
import time

router = APIRouter(
    prefix="/chatter",
    tags=["chatter"],
    responses={404: {"description": "Not found"}},
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/chatter/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/")
async def home(request: Request):
    return HTMLResponse(html)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try :
        client = await AsyncClient.create(getenv("API_KEY", None), getenv("SECRET_KEY", None))
        bm = BinanceSocketManager(client)
        async with bm.kline_socket(symbol='BNBBTC') as stream:
            while True :
                res = await stream.recv()
                await websocket.send_text(str(res))
        
    finally :
        await websocket.close()
    
