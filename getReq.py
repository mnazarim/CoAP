import logging
import asyncio

from aiocoap import *
from random import *
logging.basicConfig(level=logging.INFO)

async def client_node(label):
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri='coap://localhost/time')
    while (True):
        delay = randint(2000,4000)/1000
        await asyncio.sleep(delay)
        try:
            start_time = asyncio.get_event_loop().time()
            response = await asyncio.wait_for(protocol.request(request).response, timeout = 0.0021)
            end_time = asyncio.get_event_loop().time()
        except asyncio.TimeoutError as e:
            print("An asyncio.TimeoutError occurred.")
            print(f"Exception message: {str(e)}")
            print(f"Exception traceback: {e.__traceback__}")
        else:
            print("----" *10)
            print(label)
            rtt = end_time - start_time
            print(f"RTT: {rtt} seconds")
            print('Result: %s\n%r'%(response.code, response.payload))

# Define the number of client nodes
num_nodes = 1000

# Create and run the CoAP clients concurrently
async def main():
    tasks = []
    for node_id in range(num_nodes):
        task = asyncio.create_task(client_node(node_id))
        tasks.append(task)

    # Wait for all clients to finish
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
