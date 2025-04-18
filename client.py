import socket
import threading
import asyncio
import json
from kdf import kdf
from Enigma.enigma import Enigma

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

# global IM_ACTIVE
IM_ACTIVE = False
# global OLD_ROOT_KEY
OLD_ROOT_KEY = "initial_root"
OLD_CHAIN_KEY = "initial_chain"
# global IS_FIRST_MESSAGE
IS_FIRST_MESSAGE = True
USER_CHANGED = False

GENERATOR = 3
PRIME = 11
ORDER = 5
KEY = 4
# global SHARED_DIFFIE_KEY
SHARED_DIFFIE_KEY = 0

MAIN_MESSAGE = ""

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
    global SHARED_DIFFIE_KEY
    global IM_ACTIVE
    global USER_CHANGED
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
        
        try:
            message_dict = json.loads(message)
        except:
            continue

        if message_dict["type"] == NORMAL_MESSAGE:
            IM_ACTIVE = False
            if message_dict["content"]["message"] == DISCONNECT_MESSAGE:
                connected = False
                client_chatter.close()

            try:
                main_message = " ".join(decrypt(message_dict["content"]["message"]).split(" ")[3:]) # removes the "try breaking this" at the start
            except:
                main_message = message_dict["content"]["message"]

            print(f"[{addr}] {message_dict["content"]["message"]} :: {main_message}")
            USER_CHANGED = False
        elif message_dict["type"] == START_DIFFIE_HELLMAN:
            USER_CHANGED = True
            SHARED_DIFFIE_KEY = (int(message_dict["content"]["diffie_value"]) ** KEY ) % int(message_dict["content"]["prime"])
            print(message_dict)

            asyncio.run(handle_receive_diffie_hellman())
        elif message_dict["type"] == END_DIFFIE_HELLMAN:
            SHARED_DIFFIE_KEY = (int(message_dict["content"]["diffie_value"]) ** KEY ) % int(message_dict["content"]["prime"])
            print(message_dict)
            print("DONE WITH THE TRANSACTION")
            print("This is the message: ", MAIN_MESSAGE)

            asyncio.run(send_encrypted_message())

    conn.close()


def encrypt():
    global IM_ACTIVE
    global OLD_ROOT_KEY
    global OLD_CHAIN_KEY
    global SHARED_DIFFIE_KEY
    global USER_CHANGED
    global MAIN_MESSAGE

    enigma = Enigma()

    if USER_CHANGED:
        (root_key, chain_key, setting1_key, setting2_key, setting3_key) = kdf(OLD_ROOT_KEY, SHARED_DIFFIE_KEY)
        OLD_ROOT_KEY = root_key
        OLD_CHAIN_KEY = chain_key

        code = enigma.encode("try breaking this " + MAIN_MESSAGE, setting1_key % 26 + 1, setting2_key % 26 + 1, setting3_key % 26 + 1)

        return code
    
    else:
        (root_key, chain_key, setting1_key, setting2_key, setting3_key) = kdf(OLD_CHAIN_KEY, SHARED_DIFFIE_KEY)

        OLD_CHAIN_KEY = chain_key

        code = enigma.encode("try breaking this " + MAIN_MESSAGE, setting1_key % 26 + 1, setting2_key % 26 + 1, setting3_key % 26 + 1)

        return code

def decrypt(message):
    global IM_ACTIVE
    global OLD_ROOT_KEY
    global OLD_CHAIN_KEY
    global SHARED_DIFFIE_KEY
    global USER_CHANGED
    global MAIN_MESSAGE

    enigma = Enigma()

    if USER_CHANGED:
        (root_key, chain_key, setting1_key, setting2_key, setting3_key) = kdf(OLD_ROOT_KEY, SHARED_DIFFIE_KEY)
        OLD_ROOT_KEY = root_key
        OLD_CHAIN_KEY = chain_key

        code = enigma.encode(message, setting1_key % 26 + 1, setting2_key % 26 + 1, setting3_key % 26 + 1)

        return code
    
    else:
        (root_key, chain_key, setting1_key, setting2_key, setting3_key) = kdf(OLD_CHAIN_KEY, SHARED_DIFFIE_KEY)

        OLD_CHAIN_KEY = chain_key

        code = enigma.encode(message, setting1_key % 26 + 1, setting2_key % 26 + 1, setting3_key % 26 + 1)

        return code



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

async def send_encrypted_message():
    encrypted_message = encrypt()

    message_info = dict()
    message_info["type"] = NORMAL_MESSAGE
    message_info["content"] = {"message": encrypted_message}

    sendMessage_info = json.dumps(message_info)

    await send_message(sendMessage_info)


async def keep_inputting():
    global IM_ACTIVE
    global MAIN_MESSAGE
    global USER_CHANGED
    while True:
        MAIN_MESSAGE = await async_input("")
        if not IM_ACTIVE:
            IM_ACTIVE = True
            USER_CHANGED = True
            await start_diffie_hellman()

        else:
            USER_CHANGED = False

            await send_encrypted_message()

        # message_info = dict()
        # message_info["type"] = NORMAL_MESSAGE
        # message_info["content"] = {"message": MAIN_MESSAGE}

        # sendMessage_info = json.dumps(message_info)

        # await send_message(sendMessage_info)

        if MAIN_MESSAGE == DISCONNECT_MESSAGE:
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
