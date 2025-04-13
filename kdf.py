from hash import my_hash

def kdf(message, salt, iterations=5):
    combined_string = message + str(salt)

    for _ in range(iterations):
        combined_string = str(my_hash(combined_string))
    
    root_key = my_hash(combined_string + "root_key")
    chain_key = my_hash(combined_string + "chain_key")
    setting1_key = my_hash(combined_string + "setting1_key")
    setting2_key = my_hash(combined_string + "setting2_key")
    setting3_key = my_hash(combined_string + "setting3_key")

    return (root_key, chain_key,
            setting1_key, setting2_key, setting3_key)

if __name__=="__main__":
    print(kdf("Hello, World!", 7))