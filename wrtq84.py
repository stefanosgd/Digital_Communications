from bitarray import bitarray as bt


def encoding(message, w, l):
    window = 2**w - 1
    lookahead = 2**l - 1
    encoded_message = []
    dictionary = ''
    p = message[0]
    for i in range(0, len(message)-1):
        if (dictionary.find(p) != -1) and (len(p) < lookahead):
            p = p+message[i+1]
        else:
            if len(p)-1 == 0:
                encoded_message.append((0, 0, message[i]))
            else:
                if i < window:
                    encoded_message.append(
                        ((i - (len(dictionary) - dictionary[::-1].find(p[:-1][::-1]))), len(p) - 1, message[i]))
                else:
                    encoded_message.append(
                        ((len(p) + dictionary[::-1].find(p[:-1][::-1])), len(p) - 1, message[i]))
            p = message[i+1]
            dictionary = message[0:i+1]
            if len(dictionary) > window:
                dictionary = message[i-window:i]
    dictionary = message[0:len(message) - len(p)]
    if len(dictionary) > window:
        dictionary = message[len(dictionary)-window:len(message)-len(p)]
    if dictionary.find(p) == -1:
        if len(p) - 1 == 0:
            encoded_message.append((0, 0, p))
        else:
            if len(message) < window:
                encoded_message.append(
                    (len(message) - (len(dictionary) - dictionary[::-1].find(p[:-1][::-1])), len(p) - 1, p[-1]))
            else:
                encoded_message.append(
                    ((len(p)-1 + dictionary[::-1].find(p[:-1][::-1])), len(p) - 1, p[-1]))
    else:
        if len(message) < window:
            encoded_message.append((len(message) - (len(dictionary) - dictionary[::-1].find(p[::-1])), len(p), '_'))
        else:
            encoded_message.append(((len(p) + dictionary[::-1].find(p[::-1])), len(p), '_'))
    return encoded_message


def decoding(encoded):
    message = ''
    print("Encoded ", encoded)
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


def read_file(f_name):
    new_file = open(f_name, 'rb')
    bit_file = bt()
    bit_file.fromfile(new_file)
    bit_message = bit_file.to01()
    file_size = len(bit_message)
    return bit_message, file_size


wind = 16
look = 8
# file_message, size = read_file('test3.txt')
# input_encode = encoding(file_message, wind, look)
# output_message = decoding(input_encode)
# compression_rate = size / (len(input_encode)*(wind + look + 1))
# print("Compression rate = ", compression_rate)
# print(file_message == output_message)
# file_message, size = read_file('test2.txt')
# input_encode = encoding(file_message, wind, look)
# output_message = decoding(input_encode)
# compression_rate = size / (len(input_encode)*(wind + look + 1))
# print("Compression rate = ", compression_rate)
# print(file_message == output_message)
file_message, size = read_file('test.txt')
input_encode = encoding(file_message, wind, look)
output_message = decoding(input_encode)
compression_rate = size / (len(input_encode)*(wind + look + 1))

print("Compression rate = ", compression_rate)
# print(bt(output_message).tobytes().decode('utf-8'))
# print("blah blah blah blah blah" == output_message)
print(file_message == output_message)
