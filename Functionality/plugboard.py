class PlugBoard:
    def __init__(self, plugboard_dict):
        self.plugboard_dict = plugboard_dict
    
    def output(self, input):
        string_output = self.plugboard_dict[str(input)]
        return int(string_output)
    

if __name__ == "__main__":
    plugboard = PlugBoard({'1': '2', '2': '5', '3': '7'})
    output = plugboard.output(3)
    print(output, type(output))
