from random_dictionary import *
from rotor_group import RotorGroup
from reflector import Reflector2
from random import randint
from plugboard import PlugBoard

rotor1_dict = {'1': '23', '2': '12', '3': '16', '4': '4', '5': '19', '6': '22', '7': '6', '8': '21', '9': '9', '10': '26', '11': '13', '12': '10', '13': '20', '14': '2', '15': '24', '16': '5', '17': '8', '18': '18', '19': '15', '20': '11', '21': '25', '22': '7', '23': '17', '24': '1', '25': '3', '26': '14'}
rotor2_dict = {'1': '15', '2': '1', '3': '23', '4': '24', '5': '12', '6': '2', '7': '6', '8': '18', '9': '7', '10': '5', '11': '26', '12': '13', '13': '4', '14': '3', '15': '14', '16': '9', '17': '16', '18': '8', '19': '10', '20': '25', '21': '21', '22': '17', '23': '22', '24': '11', '25': '19', '26': '20'}
rotor3_dict = {'1': '15', '2': '25', '3': '2', '4': '23', '5': '4', '6': '26', '7': '9', '8': '19', '9': '18', '10': '7', '11': '10', '12': '5', '13': '12', '14': '14', '15': '1', '16': '21', '17': '17', '18': '16', '19': '11', '20': '24', '21': '8', '22': '22', '23': '6', '24': '20', '25': '13', '26': '3'}
reflector_dict = {'17': '23', '23': '17', '26': '16', '16': '26', '22': '14', '14': '22', '19': '4', '4': '19', '1': '6', '6': '1', '5': '12', '12': '5', '21': '9', '9': '21', '10': '11', '11': '10', '20': '24', '24': '20', '18': '25', '25': '18', '2': '7', '7': '2', '3': '15', '15': '3', '13': '8', '8': '13'}
rotor1_randomize_list = [6, 1, 11, 2, 22, 19, 0, 18, 23, 24, 3, 7, 12, 21, 15, 17, 10, 25, 9, 4, 20, 8, 13, 14, 16, 5]
rotor2_randomize_list = [17, 12, 0, 21, 11, 14, 9, 24, 22, 8, 6, 10, 13, 2, 5, 3, 1, 4, 23, 15, 18, 20, 19, 16, 7, 25]
rotor3_randomize_list = [2, 6, 13, 7, 18, 15, 4, 19, 1, 8, 3, 20, 17, 16, 5, 21, 11, 14, 23, 25, 9, 24, 22, 12, 0, 10]
reflector_list = [6, 18, 23, 20, 24, 22, 0, 15, 10, 21, 8, 12, 11, 25, 19, 7, 17, 16, 1, 14, 3, 9, 5, 2, 4, 13]
rotor_group = RotorGroup((rotor1_dict, rotor1_randomize_list), (rotor2_dict, rotor2_randomize_list), (rotor3_dict, rotor3_randomize_list), reflector_list)
reflector = Reflector2(reflector_dict)
plugboard_dict = {'7': '3', '3': '7', '6': '17', '17': '6', '8': '14', '14': '8', '25': '11', '11': '25', '2': '18', '18': '2', '16': '16', '5': '5', '12': '12', '4': '4', '20': '20', '21': '21', '19': '19', '9': '9', '13': '13', '24': '24', '22': '22', '10': '10', '23': '23', '26': '26', '15': '15', '1': '1'}
plugboard = PlugBoard(plugboard_dict)

def rotor_group_and_reflector(main_forward_input):
    for i in range(1):
        print()
        print(main_forward_input)

        output1 = rotor_group.forward_output(main_forward_input)
        print(output1)

        output2 = reflector.output(output1)
        print(output2)

        output3 = rotor_group.reverse_output(output2)
        print(output3)

        print()

def rotating_rotor_group_and_reflector(input_list):
    for item in input_list:
        rotor_group_and_reflector(item)

        print(f"*** {rotor_group.index_rotor1}")
        rotor_group.rotate_rotor1_by_one()
        print(f"*** {rotor_group.index_rotor1}")



if __name__ == "__main__":
    rotor_group.increment_rotor3_ring_settings(23)
    rotor_group.set_rotor_index_settings(26, 7, 9)

    l2 = [16, 19, 14, 2, 12, 10, 9, 3, 4, 15, 10, 23, 14, 2, 18, 23, 14, 15, 8, 14, 6, 15, 12, 8, 21, 1, 18, 16, 1, 7]

    # for i in range(30):
    #     l2.append(randint(1, 26))

    print(l2)

    l3 = []

    for i in range(len(l2)):

        main_input = l2[i]
        output = rotor_group.forward_output(main_input)
        output = reflector.output(output)
        output = rotor_group.reverse_output(output)

        l3.append(output)

        # rotor_group.rotate_rotor1_by_one()

    print(l3)

    rotor_group.reset_settings()
    rotor_group.increment_rotor3_ring_settings(23)
    rotor_group.set_rotor_index_settings(26, 7, 9)
    print(rotor_group.index_rotor1, rotor_group.index_rotor2, rotor_group.index_rotor3)

    l4 = []

    for i in range(len(l3)):
        main_input = l3[i]
        output = rotor_group.forward_output(main_input)
        output = reflector.output(output)
        output = rotor_group.reverse_output(output)
        l4.append(output)
        # rotor_group.rotate_rotor1_by_one()

    print(l4)

    print()
    print()
    print("THIS IS THE INPUT:", l2)
    print("THIS IS THE INPUT ENCRYPTED:", l3)
    print("THIS IS THE INPUT DECRYPTED:", l4)
    print()
    print("INPUT == INPUT DECRYPTED:", l2==l4)
    print()

    print("--------------------------------------------------------------------")

    rotor_group.reset_settings()
    rotor_group.set_rotor_index_settings(26, 7, 9)

    l3 = []

    for i in range(len(l2)):

        main_input = l2[i]
        output = rotor_group.forward_output(main_input)

        l3.append(output)

        # rotor_group.rotate_rotor1_by_one()

    print(l3)

    rotor_group.reset_settings()
    rotor_group.set_rotor_index_settings(26, 7, 9)

    l4 = []

    for i in range(len(l3)):
        main_input = l3[i]
        output = rotor_group.forward_output(main_input)
        # output = reflector.output(output)
        # output = rotor_group.reverse_output(output)
        l4.append(output)
        # rotor_group.rotate_rotor1_by_one()

    print(l4)

    print()
    print()
    print("THIS IS THE INPUT:", l2)
    print("THIS IS THE INPUT ENCRYPTED:", l3)
    print("THIS IS THE INPUT DECRYPTED:", l4)
    print()
    print("INPUT == INPUT DECRYPTED:", l2==l4)
    print()    

    print("--------------------------------------------------------------------")

    rotor_group.reset_settings()
    rotor_group.set_rotor_index_settings(26, 7, 9)

    l3 = []

    for i in range(len(l2)):

        main_input = l2[i]
        output = plugboard.output(main_input)
        output = rotor_group.forward_output(output)
        output = plugboard.output(output)

        l3.append(output)

        # rotor_group.rotate_rotor1_by_one()

    rotor_group.reset_settings()
    rotor_group.set_rotor_index_settings(26, 7, 9)

    l4 = []

    for i in range(len(l3)):
        main_input = l3[i]
        output = plugboard.output(main_input)
        output = rotor_group.forward_output(output)
        output = plugboard.output(output)

        l4.append(output)
        # rotor_group.rotate_rotor1_by_one()

    print()
    print()
    print("THIS IS THE INPUT:", l2)
    print("THIS IS THE INPUT ENCRYPTED:", l3)
    print("THIS IS THE INPUT DECRYPTED:", l4)
    print()
    print("INPUT == INPUT DECRYPTED:", l2==l4)
    print()   



