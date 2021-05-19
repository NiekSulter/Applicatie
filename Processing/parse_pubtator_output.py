



if __name__ == '__main__':
    file = open("test.txt")
    result = file.readlines()

    for line in result:
        if '\t' in line:
            x = line.strip('\n').split('\t')
            print(x)
