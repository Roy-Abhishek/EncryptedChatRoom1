from .node import Node
from random import randint

rotor1_dict = {'1': '23', '2': '12', '3': '16', '4': '4', '5': '19', '6': '22', '7': '6', '8': '21', '9': '9', '10': '26', '11': '13', '12': '10', '13': '20', '14': '2', '15': '24', '16': '5', '17': '8', '18': '18', '19': '15', '20': '11', '21': '25', '22': '7', '23': '17', '24': '1', '25': '3', '26': '14'}
rotor1_randomize_list = [6, 1, 11, 2, 22, 19, 0, 18, 23, 24, 3, 7, 12, 21, 15, 17, 10, 25, 9, 4, 20, 8, 13, 14, 16, 5]


class Rotor:
    def __init__(self, rotor_dict, rotor_randomize_list):
        self.input_structure = []
        self.output_structure = []
        self.rotor_dict = rotor_dict
        self.rotor_randomize_list = rotor_randomize_list
        self.ring_number = 1
        self.create_input_and_output_structure()
        self.stitch_input_and_output()

    def create_input_and_output_structure(self):
        for key in self.rotor_dict.keys():
            self.input_structure.append(Node(None, key, None))
        
        for value in self.rotor_dict.values():
            self.output_structure.append(Node(None, value, None))

    def stitch_input_and_output(self):
        for i in range(len(self.input_structure)):
            self.input_structure[i].next = self.output_structure[self.rotor_randomize_list[i]]
            self.output_structure[self.rotor_randomize_list[i]].prev = self.input_structure[i]

    def display_rotor_connections(self):
        for i in range(len(self.input_structure)):
            node = self.input_structure[i]
            print(f"{node.value} --> {node.next.value}")

    def increment_ring_setting_by_one(self):
        for i in range(len(self.output_structure)):
            if int(self.output_structure[i].value) <= 25:
                self.output_structure[i].value = str(int(self.output_structure[i].value) + 1)
            else:
                self.output_structure[i].value = str(1)

        if self.ring_number == 26:
            self.ring_number = 1
        else:
            self.ring_number += 1

    def rotate_structures_by_one(self):
        return_list_i = []
        return_list_o = []

        temp_i = self.input_structure[0]
        temp_o = self.output_structure[0]
        for i in range(1, len(self.input_structure)):
            return_list_i.append(self.input_structure[i])
            return_list_o.append(self.output_structure[i])

        return_list_i.append(temp_i)
        return_list_o.append(temp_o)

        self.input_structure = return_list_i
        self.output_structure = return_list_o


        return_list_randomize_list = []

        temp_randomize_list = self.rotor_randomize_list[0]

        for i in range(1, len(self.rotor_randomize_list)):
            return_list_randomize_list.append(self.rotor_randomize_list[i])

        return_list_randomize_list.append(temp_randomize_list)

        self.rotor_randomize_list = return_list_randomize_list

        for i in range(len(self.rotor_randomize_list)):
            if self.rotor_randomize_list[i] == 0:
                self.rotor_randomize_list[i] = 25
                continue
            self.rotor_randomize_list[i] -= 1

        # do something to fix the node connections. they have 
        # to rotate the same way so do something with stitching 
        # the nodes heres instead of using 
        # self.rotor1.stitch_input_and_output() in the 
        # rotor_group file.


if __name__ == "__main__":
    # check for error/do some debugging
    rotor = Rotor(rotor1_dict, rotor1_randomize_list)
    rotor.rotate_structures_by_one()
    rotor.rotate_structures_by_one()
























# class Rotor1:
#     def __init__(self):
#         self.input_structure = self.create_input_and_output_structure()
#         self.output_structure = self.create_input_and_output_structure()

#     def create_input_and_output_structure(self):
#         return_list = []
#         for i in range(26):
#             return_list.append(Node(None, str(i + 1), None))

#         return return_list
    
#     def stitch_input_and_output(self):
#         jumbled_list = []

#         ordered_list = []
#         for i in range(26):
#             ordered_list.append((i + 1))

#         for _ in range(26):
#             index = randint(0, len(ordered_list) - 1)
#             item_to_append = ordered_list[index]
#             jumbled_list.append(item_to_append)
#             ordered_list.remove(item_to_append)

#         for i in range(len(self.input_structure)):
#             node_to_stitch_to = None

#             index_of_node_to_stitch_to = 0

#             for j in range(len(self.output_structure)):
#                 if self.output_structure[j].value == jumbled_list[i]:
#                     index_of_node_to_stitch_to = j

#             node_to_stitch_to = self.output_structure[index_of_node_to_stitch_to]

#             self.input_structure[i].next = node_to_stitch_to

#     def display_rotor_connections(self):
#         for i in range(len(self.input_structure)):
#             node = self.input_structure[i]
#             print(f"{node.value} --> {node.next.value}")

#     def increment_ring_setting(self):
#         for i in range(len(self.output_structure)):
#             if int(self.output_structure[i].value) <=25:
#                 self.output_structure[i].value = str(int(self.output_structure[i].value) + 1)
#             else:
#                 self.output_structure[i].value = str(1)
            
