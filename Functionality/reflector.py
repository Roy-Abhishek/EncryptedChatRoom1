from .node import Node

class Reflector:
    def __init__(self, reflector_randomize_list):
        self.reflector_randomize_list = reflector_randomize_list

    def stitched_output_structure_index(self, index):
        return self.reflector_randomize_list[index]




class Reflector2:
    def __init__(self, reflector_dict):
        self.reflector_dict = reflector_dict

    def output(self, input):
        string_output = self.reflector_dict[str(input)]
        return int(string_output)
    

if __name__ == "__main__":
    reflector = Reflector2({'1': '2', '2': '5', '3': '7'})
    output = reflector.output(3)
    print(output, type(output))
