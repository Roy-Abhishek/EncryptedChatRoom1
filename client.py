import socket
import threading
import asyncio
import json

FORMAT = "utf-8"
HEADER = 1024
PORT = 5051
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
KEY = 4
SHARED_DIFFIE_KEY = 0

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind(ADDR)
client_chatter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_chatter.connect((SERVER, 5050))



def send(message):
    message = message.encode(FORMAT)

    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    try:
        client_chatter.send(send_length)
    except:
        return
    client_chatter.send(message)


def handle_server(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected to server.")

    connected = True
    while connected:
        message = ""
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            message = conn.recv(msg_length).decode(FORMAT)
            # print(f"[{addr}] {message}")

        # if message == DISCONNECT_MESSAGE:
        #     connected = False

        message_dict = dict()

        IM_ACTIVE = False
        
        try:
            message_dict = json.loads(message)
        except:
            continue

        if message_dict["type"] == NORMAL_MESSAGE:
            if message_dict["content"]["message"] == DISCONNECT_MESSAGE:
                connected = False
                client_chatter.close()

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







def start():
    send(CONNECT_MESSAGE)

    client.listen()
    print(f"[LISTENING] Client is listening on {SERVER}")

    while True:
        conn, addr = client.accept()
        thread = threading.Thread(target=handle_server, args=(conn, addr))
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

        if sendMessage == DISCONNECT_MESSAGE:
            break

async def run_client():
    message_info = dict()
    message_info["type"] = NORMAL_MESSAGE
    message_info["content"] = {"message": CONNECT_MESSAGE}

    sendMessage_info = json.dumps(message_info)
    send(sendMessage_info)

    client.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        conn, addr = client.accept()

        thread = threading.Thread(target=handle_server, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

        await keep_inputting()


print("[STARTING] Client is starting...")
asyncio.run(run_client())
