import socket
import threading
import asyncio
import json

FORMAT = "utf-8"
HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
NORMAL_MESSAGE = "!NORMAL_MESSAGE"
DISCONNECT_MESSAGE = "!DISCONNECT"
CONNECT_MESSAGE = "!CONNECT"
START_DIFFIE_HELLMAN = "!START_DIFFIE_HELLMAN"
END_DIFFIE_HELLMAN = "!END_DIFFIE_HELLMAN"

global IM_ACTIVE
IM_ACTIVE = False
global OLD_ROOT_KEY
OLD_ROOT_KEY = "initial"
global IS_FIRST_MESSAGE
IS_FIRST_MESSAGE = True

GENERATOR = 3
PRIME = 11
ORDER = 5
KEY = 3
global SHARED_DIFFIE_KEY
SHARED_DIFFIE_KEY = 0

# Sets up and binds the server that listens for chats from the client
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Sets up the server that sends messages to the client.
# This server is only connected to the client-side server
# when the client wants to connect to the server using the
# CONNECT_MESSAGE.
server_chatter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# Sends the message length, and then the message itself.
def send(message):
    message = message.encode(FORMAT)

    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    try:
        server_chatter.send(send_length)
    except:
        return
    server_chatter.send(message)

# Connects the server that sends the messages to the client.
def connect(addr):
    server_chatter.connect(addr)

# Handles incoming messages from the client through 
# (conn, addr) = server.accept().
def handle_client(conn, addr):
    global SHARED_DIFFIE_KEY
    global IM_ACTIVE
    print(f"[NEW CONNECTION] {addr} connected to client.")

    connected = True
    while connected:
        message = ""
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            message = conn.recv(msg_length).decode(FORMAT)
            # print(f"[{addr}] {message}")

        # if message == CONNECT_MESSAGE:
        #     connect((SERVER, 5051))
        # elif message == DISCONNECT_MESSAGE:
        #     connected = False
        
        message_dict = dict()
        
        try:
            message_dict = json.loads(message)
        except:
            continue


        if message_dict["type"] == NORMAL_MESSAGE:
            IM_ACTIVE = False
            if message_dict["content"]["message"] == CONNECT_MESSAGE:
                connect((SERVER, 5051))
            elif message_dict["content"]["message"] == DISCONNECT_MESSAGE:
                connected = False
                server_chatter.close()

            print(f"[{addr}] {message_dict["content"]["message"]}")
        elif message_dict["type"] == START_DIFFIE_HELLMAN:
            SHARED_DIFFIE_KEY = (int(message_dict["content"]["diffie_value"]) ** KEY ) % int(message_dict["content"]["prime"])
            print(message_dict)

            asyncio.run(handle_receive_diffie_hellman())
        elif message_dict["type"] == END_DIFFIE_HELLMAN:
            SHARED_DIFFIE_KEY = (int(message_dict["content"]["diffie_value"]) ** KEY ) % int(message_dict["content"]["prime"])
            print(message_dict)
            print("DONE WITH THE TRANSACTION")




    conn.close()



async def start_diffie_hellman():
    diffie_hellman_info = dict()
    diffie_hellman_info["type"] = START_DIFFIE_HELLMAN
    diffie_hellman_info["content"] = {"generator": GENERATOR, "prime": PRIME, "order": ORDER, "diffie_value": ((GENERATOR ** KEY) % PRIME)}

    sendMessage = json.dumps(diffie_hellman_info)

    await send_message(sendMessage)

async def handle_receive_diffie_hellman():
    # sends a message with type END_DIFFIE_HELLMAN
    # sends a set of the same generator, prime, order, and diffie_value with my own key
    diffie_hellman_info = dict()
    diffie_hellman_info["type"] = END_DIFFIE_HELLMAN
    diffie_hellman_info["content"] = {"generator": GENERATOR, "prime": PRIME, "order": ORDER, "diffie_value": ((GENERATOR ** KEY) % PRIME)}

    sendMessage = json.dumps(diffie_hellman_info)

    await send_message(sendMessage)



# This is a template for the actual asynchronous function that starts the two 
# threads that run the chat room.
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")



async def async_input(prompt):
    return await asyncio.to_thread(input, prompt)

async def send_message(message):
    await asyncio.to_thread(send, message)

async def keep_inputting():
    global IM_ACTIVE
    while True:
        sendMessage = await async_input("")
        if not IM_ACTIVE:
            IM_ACTIVE = True
            await start_diffie_hellman()

        message_info = dict()
        message_info["type"] = NORMAL_MESSAGE
        message_info["content"] = {"message": sendMessage}

        sendMessage_info = json.dumps(message_info)

        await send_message(sendMessage_info)
        print(SHARED_DIFFIE_KEY)

        if sendMessage == DISCONNECT_MESSAGE:
            break

# This is the asynchronous function that runs the chat room.
# It has two threads, one of which handles incoming messages,
# and the second one of which handles the outgoing messages.
async def run_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        conn, addr = server.accept()

        # handle_client handles the incoming messages.
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # await handle_client(conn, addr)
        # asyncio.run(handle_client(conn, addr))
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

        # keep_inputting handles the sending of messages from the 
        # user of server.py
        await keep_inputting()


print("[STARTING] Server is starting...")
asyncio.run(run_server())


