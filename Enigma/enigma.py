from .rotor_group import RotorGroup
from .plugboard import PlugBoard
from .keyboard_class import KeyBoard
from .constants import *

class Enigma:
    def __init__(self):
        self.plugboard_dict = PLUGBOARD_CONFIGS["a"]
        self.rotor1_info = ROTOR_INFOS["a"]
        self.rotor2_info = ROTOR_INFOS["b"]
        self.rotor3_info = ROTOR_INFOS["c"]
        self.rotor1_starting_index = 1
        self.rotor2_starting_index = 1
        self.rotor3_starting_index = 1
        self.reflector_randomize_list = REFLECTOR_RANDOMIZE_LIST

        self.keyboard = KeyBoard()
        self.plugboard = PlugBoard(PLUGBOARD_CONFIGS["a"])
        self.rotor_group = RotorGroup(ROTOR_INFOS["a"], 
                                      ROTOR_INFOS["b"], 
                                      ROTOR_INFOS["c"], 
                                      REFLECTOR_RANDOMIZE_LIST)

    def change_rotors(self, rotor1_info, rotor2_info, rotor3_info):
        self.rotor1_info = rotor1_info
        self.rotor2_info = rotor2_info
        self.rotor3_info = rotor3_info
        self.rotor_group = RotorGroup(rotor1_info, rotor2_info, rotor3_info, REFLECTOR_RANDOMIZE_LIST)

    def change_plugboard(self, plugboard_dict):
        self.plugboard_dict = plugboard_dict
        self.plugboard = PlugBoard(plugboard_dict)

    def set_rotor_index_settings(self, target_rotor1_index, target_rotor2_index, target_rotor3_index):
        self.rotor1_starting_index = target_rotor1_index
        self.rotor2_starting_index = target_rotor2_index
        self.rotor3_starting_index = target_rotor3_index
        self.rotor_group.set_rotor_index_settings(target_rotor1_index, target_rotor2_index, target_rotor3_index)

    def change_reflector_settings(self, reflector_randomize_list):
        self.reflector_randomize_list = reflector_randomize_list
        self.rotor_group = RotorGroup(self.rotor1_info, self.rotor2_info, self.rotor3_info, reflector_randomize_list)
        self.set_rotor_index_settings(self.rotor1_starting_index, self.rotor2_starting_index, self.rotor3_starting_index)

    def reset_to_prev_setting(self):
        self.keyboard = KeyBoard()
        self.plugboard = PlugBoard(self.plugboard_dict)
        self.rotor_group = RotorGroup(self.rotor1_info, self.rotor2_info, self.rotor3_info, self.reflector_randomize_list)
        self.set_rotor_index_settings(self.rotor1_starting_index, self.rotor2_starting_index, self.rotor3_starting_index)

    def reset_defaults(self):
        self.__init__()



    # the next two methods, when used outside of this class, should 
    # be used with this class' rotor1/2/3_starting_index variables.
    # it'll go something like
    # enigma1.encode("hello world", 
    #                enigma.rotor1_starting_index, 
    #                enigma.rotor2_starting_index, 
    #                enigma.rotor3_starting_index)
    def encode(self, input, target_rotor1_index, target_rotor2_index, target_rotor3_index):
        self.set_rotor_index_settings(target_rotor1_index, target_rotor2_index, target_rotor3_index)

        input_list_words = input.split()
        output_list_words = []

        for i in range(len(input_list_words)):
            output_list_words.append("")
            for j in range(len(input_list_words[i])):
                input_number = int(LETTERS_TO_NUMBERS[input_list_words[i][j].lower()])

                output = self.keyboard.output(input_number)
                output = self.plugboard.output(output)
                output = self.rotor_group.forward_output(output)
                output = self.plugboard.output(output)
                output = output

                output_letter = NUMBERS_TO_LETTERS[str(output)]
                output_list_words[len(output_list_words) - 1] += output_letter

        return " ".join(output_list_words)
    
    def decode(self, input, target_rotor1_index, target_rotor2_index, target_rotor3_index):
        self.set_rotor_index_settings(target_rotor1_index, target_rotor2_index, target_rotor3_index)

        input_list_words = input.split()
        output_list_words = []

        for i in range(len(input_list_words)):
            output_list_words.append("")
            for j in range(len(input_list_words[i])):
                input_number = int(LETTERS_TO_NUMBERS[input_list_words[i][j].lower()])

                output = self.keyboard.output(input_number)
                output = self.plugboard.output(output)
                output = self.rotor_group.forward_output(output)
                output = self.plugboard.output(output)
                output = output

                output_letter = NUMBERS_TO_LETTERS[str(output)]
                output_list_words[len(output_list_words) - 1] += output_letter

        return " ".join(output_list_words)
    


    def interactive_enigma(self):
        default_or_custom_settings = input("Deafault or custom settings (d/c): ")

        if default_or_custom_settings == "c":
            print("\nRotor Settings")
            rotor1_info = input("Rotor 1: ")
            rotor2_info = input("Rotor 2: ")
            rotor3_info = input("Rotor 3: ")

        for i in range(2):
            decode_or_encode = input("Do you want to decode or encode: ")
            if decode_or_encode == "decode":
                input_phrase = input("Phrase to decode: ")

                encoded_phrase = self.decode(input_phrase, self.rotor1_starting_index, self.rotor2_starting_index, self.rotor3_starting_index)

                print()
                print("Decoded phrase:", encoded_phrase)
                print()
            else:
                input_phrase = input("Phrase to encode: ")

                encoded_phrase = self.encode(input_phrase, self.rotor1_starting_index, self.rotor2_starting_index, self.rotor3_starting_index)

                print()
                print("Encoded phrase:", encoded_phrase)
                print()
            




            

    

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

                




