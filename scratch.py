from Functionality.enigma import Enigma

string = "Hello my name is"

list = string.split()

print(list)

if __name__ == "__main__":
    enigma1 = Enigma()
    
    phrase_to_encode = "hello world"
    encoded_code = enigma1.encode(phrase_to_encode, 1, 1, 1)
    print(encoded_code)
    decoded_code = enigma1.decode(encoded_code, 1, 1, 1)
    print(decoded_code)

    print()
    print()

    enigma1.interactive_enigma()
