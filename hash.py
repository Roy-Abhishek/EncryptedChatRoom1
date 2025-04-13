def my_hash(string):
    hashed_num = 0
    for char in string:
        hashed_num ^= ord(char)

    return hashed_num % 256

if __name__=="__main__":
    print(my_hash("Hello, World!"))