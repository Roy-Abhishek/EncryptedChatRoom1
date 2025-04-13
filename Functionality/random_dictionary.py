from random import randint

# these methods are to be used in the mother class
# to make universal dictionaries to be used by the 
# rotors, reflector, and plugboard.


# the following two functions are the two parts of 
# the tuple that go into the __init__ argument for 
# the Rotor class.
def random_dictionary_for_rotor(input):
    return_dict = dict()
    final_list = []

    ordered_list = []
    for i in range(input):
        ordered_list.append((i + 1))

    for _ in range(input):
        index = randint(0, len(ordered_list) - 1)
        item_to_append = ordered_list[index]
        final_list.append(item_to_append)
        ordered_list.remove(item_to_append)

    for i in range(input):
        return_dict[str(i + 1)] = str(final_list[i])

    return return_dict

def random_rotor_wiring_list(input):
    jumbled_indeces = []

    ordered_list = []
    for i in range(input):
        ordered_list.append(i)

    for _ in range(input):
        index = randint(0, len(ordered_list) - 1)
        item_to_append = ordered_list[index]
        jumbled_indeces.append(item_to_append)
        ordered_list.remove(item_to_append)

    return jumbled_indeces



def random_dictionary_for_reflector(input):
    # the indices are going to be in pairs
    return_dict = dict()
    jumbled_list = []

    ordered_list = []
    for i in range(input):
        ordered_list.append((i + 1))

    for _ in range(input):
        index = randint(0, len(ordered_list) - 1)
        item_to_append = ordered_list[index]
        jumbled_list.append(item_to_append)
        ordered_list.remove(item_to_append)

    jumbled_half_one = jumbled_list[:int(len(jumbled_list) / 2)]
    jumbled_half_two = jumbled_list[int(len(jumbled_list) / 2):]

    for i in range(len(jumbled_half_one)):
        return_dict[str(jumbled_half_one[i])] = str(jumbled_half_two[i])
        return_dict[str(jumbled_half_two[i])] = str(jumbled_half_one[i])

    return return_dict

# this is the list used by the reflector class to tell 
# the forward output of the three rotors where to go 
# to continue with the reverse output process. this 
# list being random basically tells the forward output 
# to go to a jumbled up place to continue with the 
# reverse output. however, since in a normal reflector 
# there are pairs, the same thing goes for this list.
def random_reflector_wiring_list(input):
    jumbled_list = []

    ordered_list = []
    for i in range(input):
        ordered_list.append(i)

    for _ in range(input):
        index = randint(0, len(ordered_list) - 1)
        item_to_append = ordered_list[index]
        jumbled_list.append(item_to_append)
        ordered_list.remove(item_to_append)

    return_list = []

    for i in range(len(jumbled_list)):
        return_list.append(-1)

    while len(jumbled_list) != 0:
        first_in_pair = jumbled_list[randint(0, len(jumbled_list) - 1)]
        jumbled_list.remove(first_in_pair)
        second_in_pair = jumbled_list[randint(0, len(jumbled_list) - 1)]
        jumbled_list.remove(second_in_pair)

        return_list[first_in_pair] = second_in_pair
        return_list[second_in_pair] = first_in_pair

    return return_list
        



def random_dictionary_for_plugboard(input):
    jumbled_list = []

    ordered_list = []
    for i in range(input):
        ordered_list.append(i + 1)

    for _ in range(input):
        index = randint(0, len(ordered_list) - 1)
        item_to_append = ordered_list[index]
        jumbled_list.append(item_to_append)
        ordered_list.remove(item_to_append)

    return_dict = dict()

    while len(jumbled_list) != (input - 10):
        first_in_pair = jumbled_list[randint(0, len(jumbled_list) - 1)]
        jumbled_list.remove(first_in_pair)
        second_in_pair = jumbled_list[randint(0, len(jumbled_list) - 1)]
        jumbled_list.remove(second_in_pair)

        return_dict[str(first_in_pair)] = str(second_in_pair)
        return_dict[str(second_in_pair)] = str(first_in_pair)

    for item in jumbled_list:
        return_dict[str(item)] = str(item)

    return return_dict


if __name__ == "__main__":
    # dictionary_for_rotor = random_dictionary_for_rotor(26)
    # print(dictionary_for_rotor, type(dictionary_for_rotor), len(dictionary_for_rotor.keys()))

    # print()

    # dictionary_for_reflector = random_dictionary_for_reflector(26)
    # print(dictionary_for_reflector, type(dictionary_for_reflector), len(dictionary_for_reflector.keys()))

    # print()

    # random_list_for_reflector = random_relfector_wiring_list(26)
    # print(random_list_for_reflector, type(random_list_for_reflector), len(random_list_for_reflector))

    # print()

    # random_plugboard_list = random_dictionary_for_plugboard(26)
    # print(random_plugboard_list, type(random_plugboard_list), len(random_plugboard_list))

    # print(random_dictionary_for_rotor(26))
    # print(random_rotor_wiring_list(26))

    print(random_dictionary_for_plugboard(26))




