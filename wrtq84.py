from bitarray import bitarray as bt


def encoding(message, w, l):
    window = 2**w - 1
    lookahead = 2**l - 1
    encoded_message = []
    dictionary = ''
    encoded_bit_message = ''
    p = message[0]
    for i in range(0, len(message)-1):
        if (dictionary.find(p) != -1) and (len(p) < lookahead):
            p = p+message[i+1]
        else:
            if len(p)-1 == 0:
                encoded_bit_message += "0"*w + "0"*l + message[i]
                encoded_message.append((0, 0, message[i]))
            else:
                if i < window:
                    step_back = i - (len(dictionary) - dictionary[::-1].find(p[:-1][::-1]))
                    step_length = len(p) - 1
                    encoded_message.append(
                        (step_back, step_length, message[i]))
                    encoded_bit_message += "0" * (w - len("{0:b}".format(step_back))) + "{0:b}".format(step_back)
                    encoded_bit_message += "0" * (l - len("{0:b}".format(step_length))) + "{0:b}".format(step_length)
                    encoded_bit_message += message[i]
                else:
                    step_back = len(p) + dictionary[::-1].find(p[:-1][::-1])-1
                    step_length = len(p) - 1
                    encoded_message.append(
                        (step_back, step_length, message[i]))
                    encoded_bit_message += "0" * (w - len("{0:b}".format(step_back))) + "{0:b}".format(step_back)
                    encoded_bit_message += "0" * (l - len("{0:b}".format(step_length))) + "{0:b}".format(step_length)
                    encoded_bit_message += message[i]
            p = message[i+1]
            dictionary = message[0:i+1]
            if len(dictionary) > window:
                dictionary = message[i-window+1:i+1]
    dictionary = message[0:len(message) - len(p)]
    if len(dictionary) > window:
        dictionary = message[len(dictionary)-window:len(message)-len(p)]
    if dictionary.find(p) == -1:
        if len(p) - 1 == 0:
            encoded_message.append((0, 0, p))
        else:
            if len(message) < window:
                step_back = len(message) - (len(dictionary) - dictionary[::-1].find(p[:-1][::-1]))
                step_length = len(p) - 1
                encoded_bit_message += "0" * (w - len("{0:b}".format(step_back))) + "{0:b}".format(step_back)
                encoded_bit_message += "0" * (l - len("{0:b}".format(step_length))) + "{0:b}".format(step_length)
                encoded_bit_message += p[-1]
                encoded_message.append(
                    (step_back, step_length, p[-1]))
            else:
                step_back = len(p)-1 + dictionary[::-1].find(p[:-1][::-1])
                step_length = len(p) - 1
                encoded_bit_message += "0" * (w - len("{0:b}".format(step_back))) + "{0:b}".format(step_back)
                encoded_bit_message += "0" * (l - len("{0:b}".format(step_length))) + "{0:b}".format(step_length)
                encoded_bit_message += p[-1]
                encoded_message.append(
                    (step_back, step_length, p[-1]))
    else:
        if len(message) < window:
            step_back = len(message) - (len(dictionary) - dictionary[::-1].find(p[::-1]))
            step_length = len(p)
            encoded_bit_message += "0" * (w - len("{0:b}".format(step_back))) + "{0:b}".format(step_back)
            encoded_bit_message += "0" * (l - len("{0:b}".format(step_length))) + "{0:b}".format(step_length)
            encoded_message.append((step_back, step_length, '_'))
        else:
            step_back = len(p) + dictionary[::-1].find(p[::-1])
            step_length = len(p)
            encoded_bit_message += "0" * (w - len("{0:b}".format(step_back))) + "{0:b}".format(step_back)
            encoded_bit_message += "0" * (l - len("{0:b}".format(step_length))) + "{0:b}".format(step_length)
            encoded_message.append(((len(p) + dictionary[::-1].find(p[::-1])), len(p), '_'))
    return encoded_message, encoded_bit_message


def decoding(encoded):
    message = ''
    for i in encoded:
        if i[0] == 0:
            message = message + i[2]
        else:
            start = len(message) - i[0]
            end = start + i[1]
            message = message + message[start:end] + i[2]
    if message[-1] == '_':
        message = message[:-1]
    return message


def convert_to_list(bit_message, w, l):
    converted_list = []
    i = 0
    while i < len(bit_message) - (w+l):
        converted_list.append((int(bit_message[i:w+i], 2), int(bit_message[w+i:w+l+i], 2), (bit_message[w+l+i])))
        i += w+l+1
    if (i+w+l) == len(bit_message):
        converted_list.append(
            (int(bit_message[i:w+i], 2), int(bit_message[w + i:w + l + i], 2), '_'))
    elif (i+w+l) > len(bit_message):
        length = len(converted_list)
        converted_list[length-1] = (converted_list[length-1][0], converted_list[length-1][1], '_')
    return converted_list


def read_file(f_name):
    new_file = open(f_name, 'rb')
    bit_file = bt()
    bit_file.fromfile(new_file)
    bit_message = bit_file.to01()
    file_size = len(bit_message)
    return bit_message, file_size


def write_file(f_name, f_extension, output):
    new_file = open(f_name+f_extension, 'wb')
    new_file.write(output)
    new_file.close()


def compress(file_name, window, lookahead):
    file_message, size = read_file(file_name)
    file_name = file_name.split('.')[0]
    input_encode, bit_encode = encoding(file_message, window, lookahead)
    print("Original: ", size)
    print("Compressed: ", len(input_encode)*(window+lookahead+1))
    write_file(file_name+"_out", '', bt(bit_encode).tobytes())


def decompress(file_name, window, lookahead, save_extension):
    input_again, new_input_size = read_file(file_name)
    input_list_convert = convert_to_list(input_again, window, lookahead)
    output_message_new = decoding(input_list_convert)
    write_file(file_name+'_decompressed', save_extension, bt(output_message_new).tobytes())


compress('test.txt', 8, 8)
compress('test2.txt', 16, 8)
compress('test3.txt', 16, 8)
compress('test_image.jpg', 16, 16)

decompress('test_out', 8, 8, '.txt')
decompress('test2_out', 16, 8, '.txt')
decompress('test3_out', 16, 8, '.txt')
decompress('test_image_out', 16, 16, '.jpg')
