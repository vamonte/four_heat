"""
async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client('Hello World!'))

"""
import asyncio
import json

class TCPClient:
    READ_CONFIG = '["2WL","0"]'

    def __init__(self, ip: str, port: str):
        self.ip = ip
        self.port = port
    

    async def _send_command(self, command: str) -> str | None:
        reader, writer = await asyncio.open_connection(self.ip, self.port)

        writer.write(command.encode())
        await writer.drain()
        if data := await reader.read(1024):
            return json.loads(data.decode())
        return None
    
    async def read_config(self):
        return await self._send_command(self.READ_CONFIG)
        
