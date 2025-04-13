def rotate_list(input):
    return_list = []
    temp = input[0]
    for i in range(1, len(input)):
        return_list.append(input[i])

    return_list.append(temp)

    return return_list

if __name__ == "__main__":
    l = [4, 1, 2, 3]
    print(rotate_list(l))




