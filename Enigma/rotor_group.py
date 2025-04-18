from .rotor import Rotor
from .reflector import Reflector
from .node import Node
from .random_dictionary import random_dictionary_for_rotor

class RotorGroup:
    def __init__(self, rotor1_info, rotor2_info, rotor3_info, reflector_list):
        self.index_rotor1 = 1
        self.index_rotor2 = 1
        self.index_rotor3 = 1
        self.rotor1 = Rotor(rotor1_info[0], rotor1_info[1])
        self.rotor2 = Rotor(rotor2_info[0], rotor2_info[1])
        self.rotor3 = Rotor(rotor3_info[0], rotor3_info[1])
        self.reflector = Reflector(reflector_list)
        self.input_interface_structure = []
        self.output_interface_structure = []
        self.create_input_and_output_interface_structure()
        self.stitch_rotors()

        # save variables for reset
        self.saved_rotor1_info = rotor1_info
        self.saved_rotor2_info = rotor2_info
        self.saved_rotor3_info = rotor3_info
        self.saved_reflector_list = reflector_list

    def reset_settings(self):
        self.__init__(self.saved_rotor1_info, self.saved_rotor2_info, self.saved_rotor3_info, self.saved_reflector_list)

    def set_rotor_index_settings(self, target_index_rotor1, target_index_rotor2, target_index_rotor3):
        self.rotate_rotor1_to_target_index(target_index_rotor1)
        self.rotate_rotor2_to_target_index(target_index_rotor2)
        self.rotate_rotor3_to_target_index(target_index_rotor3)

    def set_rotor_ring_number_settings(self, target_number_rotor1, target_number_rotor2, target_number_rotor3):
        self.increment_rotor1_ring_settings(target_number_rotor1)
        self.increment_rotor2_ring_settings(target_number_rotor2)
        self.increment_rotor3_ring_settings(target_number_rotor3)



    def create_input_and_output_interface_structure(self):
        for i in range(len(self.rotor1.input_structure)):
            self.input_interface_structure.append(Node(None, str(i + 1), None))
            self.output_interface_structure.append(Node(None, str(i + 1), None))

    def stitch_rotors(self):
        for i in range(len(self.input_interface_structure)):
            self.input_interface_structure[i].next = self.rotor1.input_structure[i]
            self.rotor1.input_structure[i].prev = self.input_interface_structure[i]

        for i in range(len(self.rotor1.output_structure)):
            self.rotor1.output_structure[i].next = self.rotor2.input_structure[i]
            self.rotor2.input_structure[i].prev = self.rotor1.output_structure[i]
        
        for i in range(len(self.rotor2.output_structure)):
            self.rotor2.output_structure[i].next = self.rotor3.input_structure[i]
            self.rotor3.input_structure[i].prev = self.rotor2.output_structure[i]

        for i in range(len(self.rotor3.output_structure)):
            self.rotor3.output_structure[i].next = self.output_interface_structure[i]
            self.output_interface_structure[i].prev = self.rotor3.output_structure[i]

        for i in range(len(self.input_interface_structure)):
            self.rotor1.input_structure[i].value = self.input_interface_structure[i].value
            self.rotor2.input_structure[i].value = self.rotor1.output_structure[i].value
            self.rotor3.input_structure[i].value = self.rotor2.output_structure[i].value
            self.output_interface_structure[i].value = self.rotor3.output_structure[i].value



    def rotate_rotor1_to_target_index(self, target_index):
        if target_index < self.index_rotor1:
            while self.index_rotor1 != 26:
                self.rotate_rotor1_individually_by_one()

            for i in range(target_index):
                self.rotate_rotor1_individually_by_one()

            return
        
        increment_number = target_index - self.index_rotor1
        for i in range(increment_number):
            self.rotate_rotor1_individually_by_one()

    def rotate_rotor2_to_target_index(self, target_index):
        if target_index < self.index_rotor2:
            while self.index_rotor2 != 26:
                self.rotate_rotor2_individually_by_one()

            for i in range(target_index):
                self.rotate_rotor2_individually_by_one()

            return
        
        increment_number = target_index - self.index_rotor2
        for i in range(increment_number):
            self.rotate_rotor2_individually_by_one()

    def rotate_rotor3_to_target_index(self, target_index):
        if target_index < self.index_rotor3:
            while self.index_rotor3 != 26:
                self.rotate_rotor3_individually_by_one()

            for i in range(target_index):
                self.rotate_rotor3_individually_by_one()

            return
        
        increment_number = target_index - self.index_rotor3
        for i in range(increment_number):
            self.rotate_rotor3_individually_by_one()

    def rotate_rotor1_individually_by_one(self):
        self.delete_stitches(self.rotor1)
        self.rotor1.rotate_structures_by_one()
        self.rotor1.stitch_input_and_output()
        self.stitch_rotors()
        if self.index_rotor1 == 26:
            self.index_rotor1 = 1
            return
        self.index_rotor1 += 1

    def rotate_rotor2_individually_by_one(self):
        self.delete_stitches(self.rotor2)
        self.rotor2.rotate_structures_by_one()
        self.rotor2.stitch_input_and_output()
        self.stitch_rotors()
        if self.index_rotor2 == 26:
            self.index_rotor2 = 1
            return
        self.index_rotor2 += 1

    def rotate_rotor3_individually_by_one(self):
        self.delete_stitches(self.rotor3)
        self.rotor3.rotate_structures_by_one()
        self.rotor3.stitch_input_and_output()
        self.stitch_rotors()
        if self.index_rotor3 == 26:
            self.index_rotor3 = 1
            return
        self.index_rotor3 += 1



    # the following three methods are to be used when 
    # incrementing the rotors by one when encrypting/decrypting 
    # the code. the above three functions are used when
    # setting the rotor positions when we don't want the 
    # second and third rotors to rotate when rotor1 has 
    # rotated more than 26 turns.
    def rotate_rotor1_by_one(self):
        self.delete_stitches(self.rotor1)
        self.rotor1.rotate_structures_by_one()
        self.rotor1.stitch_input_and_output()
        self.stitch_rotors()
        if self.index_rotor1 == 26:
            self.index_rotor1 = 1
            self.rotate_rotor2_by_one()
            return
        self.index_rotor1 += 1

    def rotate_rotor2_by_one(self):
        self.delete_stitches(self.rotor2)
        self.rotor2.rotate_structures_by_one()
        self.rotor2.stitch_input_and_output()
        self.stitch_rotors()
        if self.index_rotor2 == 26:
            self.index_rotor2 = 1
            self.rotate_rotor3_by_one()
            return
        self.index_rotor2 += 1

    def rotate_rotor3_by_one(self):
        self.delete_stitches(self.rotor3)
        self.rotor3.rotate_structures_by_one()
        self.rotor3.stitch_input_and_output()
        self.stitch_rotors()
        if self.index_rotor3 == 26:
            self.index_rotor3 = 1
            return
        self.index_rotor3 += 1

    def delete_stitches(self, rotor):
        for i in range(len(rotor.input_structure)):
            rotor.input_structure[i].prev = None
            rotor.output_structure[i].next = None




    def increment_rotor1_ring_settings(self, target_setting_number):
        if target_setting_number < self.rotor1.ring_number:
            while self.rotor1.ring_number != 26:
                self.rotor1.increment_ring_setting_by_one()
            
            for i in range(target_setting_number):
                self.rotor1.increment_ring_setting_by_one()

            return
        
        increment_number = target_setting_number - self.rotor1.ring_number
        for i in range(increment_number):
            self.rotor1.increment_ring_setting_by_one()

        self.stitch_rotors()

    def increment_rotor2_ring_settings(self, target_setting_number):
        if target_setting_number < self.rotor2.ring_number:
            while self.rotor2.ring_number != 26:
                self.rotor2.increment_ring_setting_by_one()
            
            for i in range(target_setting_number):
                self.rotor2.increment_ring_setting_by_one()

            return
        
        increment_number = target_setting_number - self.rotor2.ring_number
        for i in range(increment_number):
            self.rotor2.increment_ring_setting_by_one()

        self.stitch_rotors()

    def increment_rotor3_ring_settings(self, target_setting_number):
        if target_setting_number < self.rotor3.ring_number:
            while self.rotor3.ring_number != 26:
                self.rotor3.increment_ring_setting_by_one()
            
            for i in range(target_setting_number):
                self.rotor3.increment_ring_setting_by_one()

            return
        
        increment_number = target_setting_number - self.rotor3.ring_number
        for i in range(increment_number):
            self.rotor3.increment_ring_setting_by_one()

        self.stitch_rotors()



    def display_rotor_group(self):
        for i in range(len(self.rotor1.input_structure)):
            print(f"{self.input_interface_structure[i].value} ---> {self.rotor1.input_structure[i].value}/{self.input_interface_structure[i].next.value} --> {self.rotor1.output_structure[i].value}/{self.rotor1.input_structure[i].next.value} ---> {self.rotor2.input_structure[i].value}/{self.rotor1.output_structure[i].next.value} --> {self.rotor2.output_structure[i].value}/{self.rotor2.input_structure[i].next.value} ---> {self.rotor3.input_structure[i].value}/{self.rotor2.output_structure[i].next.value} --> {self.rotor3.output_structure[i].value}/{self.rotor3.input_structure[i].next.value} ---> {self.output_interface_structure[i].value}/{self.rotor3.output_structure[i].next.value}")

    def display_one_rotor_row(self):
        i = 1
        print(f"{self.input_interface_structure[i].value} ---> {self.rotor1.input_structure[i].value}/{self.input_interface_structure[i].next.value} --> {self.rotor1.output_structure[i].value}/{self.rotor1.input_structure[i].next.value} ---> {self.rotor2.input_structure[i].value}/{self.rotor1.output_structure[i].next.value} --> {self.rotor2.output_structure[i].value}/{self.rotor2.input_structure[i].next.value} ---> {self.rotor3.input_structure[i].value}/{self.rotor2.output_structure[i].next.value} --> {self.rotor3.output_structure[i].value}/{self.rotor3.input_structure[i].next.value} ---> {self.output_interface_structure[i].value}/{self.rotor3.output_structure[i].next.value}")



    # the following functions most likely aren't correctly 
    # made/formatted. be careful as to which ones to use.
    def reverse_output(self, input):
        output_node = None
        for i in range(len(self.output_interface_structure)):
            if self.output_interface_structure[i].value == str(input):
                output_node = self.output_interface_structure[i]

        while output_node.prev != None:
            output_node = output_node.prev

        return int(output_node.value)

    def forward_output(self, input):
        output_node = None
        for i in range(len(self.input_interface_structure)):
            if self.input_interface_structure[i].value == str(input):
                output_node = self.input_interface_structure[i]

        while output_node.next != None:
            output_node = output_node.next

        reflector_input_index = -27  # -27 so I can pinpoint any potential errors better
        for i in range(len(self.output_interface_structure)):
            if self.output_interface_structure[i].value == str(output_node.value):
                reflector_input_index = i

        reflector_output_index = self.reflector.stitched_output_structure_index(reflector_input_index)
        
        output_node = self.output_interface_structure[reflector_output_index]

        while output_node.prev != None:
            output_node = output_node.prev

        self.rotate_rotor1_by_one()

        return int(output_node.value)

    

if __name__ == "__main__":
    # check for error/do some debugging
    input_dict = dict()

    for i in range(26):
        input_dict[str(i + 1)] = str(i + 1)

    rotor_group = RotorGroup(input_dict, input_dict, input_dict)

    # rotor_group.display_rotor_group()

    # forward_output = rotor_group.forward_output(1)
    # reverse_output = rotor_group.reverse_output(2)

    # print()
    # print(forward_output, reverse_output)



    rotor_group.display_one_rotor_row()
    rotor_group.rotate_rotor1_by_one()
    rotor_group.display_one_rotor_row()

