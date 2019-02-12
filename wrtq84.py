from bitarray import bitarray as bt
import timeit


def appending_bits(back, forward, window, lookahead):
    encoded_bits = ''
    encoded_bits += bin(back)[2:].zfill(window)
    encoded_bits += bin(forward)[2:].zfill(lookahead)
    return encoded_bits


def encoding(message, w, l):
    window = 2**w - 1
    lookahead = 2**l - 1
    dictionary = ''
    encoded_bit_message = ''
    p = message[0]
    for i in range(0, len(message)-1):
        if len(p) > len(dictionary):
            check = -1
        elif p[-1] == dictionary[len(p)-1]:
            check = 0
        else:
            check = dictionary.find(p)
        if (check != -1) and (len(p) < lookahead):
            dictionary = dictionary[check:]
            p = p+message[i+1]
        else:
            if len(p)-1 == 0:
                encoded_bit_message += message[i].zfill(w+l+1)
            else:
                encoded_bit_message += appending_bits(len(dictionary), len(p) - 1, w, l)
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
            encoded_bit_message += "0" * w + "0" * l + p
        else:
            encoded_bit_message += appending_bits((len(dictionary) - dictionary.index(p[:-1])), len(p) - 1, w, l)
            encoded_bit_message += p[-1]
    else:
        encoded_bit_message += appending_bits((len(dictionary) - dictionary.index(p[:-1])), len(p), w, l)
    return encoded_bit_message


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
    while i < len(bit_message)-(w+l):
        converted_list.append((int(bit_message[i:w+i], 2), int(bit_message[w+i:w+l+i], 2), (bit_message[w+l+i])))
        i += w+l+1
    if (i+w+l) == len(bit_message):
        converted_list.append((int(bit_message[i:w+i], 2), int(bit_message[w+i:w+l+i], 2), '_'))
    elif (i+w+l) > len(bit_message):
        converted_list[-1] = (converted_list[-1][0], converted_list[-1][1], '_')
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
    bt(output).tofile(new_file)
    new_file.close()


def compress(file_name, window, lookahead):
    start = timeit.default_timer()
    file_message, size = read_file(file_name)
    file_name = file_name.split('.')[0]
    bit_encode = encoding(file_message, window, lookahead)
    stop = timeit.default_timer()
    print("Compression took", stop - start, "seconds")
    print("Original:", size)
    print("Compressed:", len(bit_encode))
    print("Compression rate:", size / len(bit_encode))
    write_file(file_name+"_out", '', bit_encode)


def decompress(file_name, window, lookahead, save_extension):
    start = timeit.default_timer()
    input_again, new_input_size = read_file(file_name)
    input_list_convert = convert_to_list(input_again, window, lookahead)
    output_message_new = decoding(input_list_convert)
    write_file(file_name+'_decompressed', save_extension, output_message_new)
    stop = timeit.default_timer()
    print("Decompression took", stop - start, "seconds")


print("Test 1")
compress('Tests/test1.txt', 12, 7)
decompress('Tests/test1_out', 12, 7, '.txt')
print("Test 2")
compress('Tests/test2.txt', 14, 7)
decompress('Tests/test2_out', 14, 7, '.txt')
print("Test 3")
compress('Tests/test3.txt', 16, 7)
decompress('Tests/test3_out', 16, 7, '.txt')
print("Test 4")
compress('Tests/test4.txt', 17, 7)
decompress('Tests/test4_out', 17, 7, '.txt')
print("Test 5")
compress('Tests/test5.txt', 19, 7)
decompress('Tests/test5_out', 19, 7, '.txt')
# print("Test 6")
# compress('Tests/test6.txt', 16, 7)
# decompress('Tests/test6_out', 16, 7, '.txt')
# print("Test Image")
# compress('Tests/test_image.jpg', 16, 5)
# decompress('Tests/test_image_out', 16, 5, '.jpg')
