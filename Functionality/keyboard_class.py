class KeyBoard:
    def output(self, input):
        return input
    

if __name__ == "__main__":
    keyboard = KeyBoard()
    output = keyboard.output(3)
    print(output, type(output))