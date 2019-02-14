from bitarray import bitarray as bt
import timeit
import sys


def main():
    input_file = sys.argv[1]
    input_window = int(sys.argv[2])
    input_lookahead = int(sys.argv[3])
    compress(input_file, input_window, input_lookahead)
    decompress(input_file.split('.')[0] + '_out_' + str(input_window) + '_'
               + str(input_lookahead)+'.bin', '.'+input_file.split('.')[1])


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
        encoded_bit_message += appending_bits((len(dictionary) - dictionary.index(p)), len(p), w, l)
        encoded_bit_message += '11'
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
    bit_list = [bit_message[i:i + w+l+1] for i in range(0, len(bit_message), w+l+1)]
    for i in bit_list:
        if len(i) == w+l+1:
            converted_list.append((int(i[0:w], 2), int(i[w:w+l], 2), (i[-1])))
        elif converted_list[-1][2] == '1' and i[0] == '1':
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
    new_file = open("results.txt", "w+")
    new_file.write(str(size/len(bit_encode)) + "\t" + str(stop-start) + "\t")
    new_file.close()
    write_file(file_name+"_out_"+str(window)+"_"+str(lookahead), '.bin', bit_encode)


def decompress(file_name, save_extension):
    input_again, new_input_size = read_file(file_name)
    file_name = file_name.split('.')[0]
    window = int(file_name.split('_')[2])
    lookahead = int(file_name.split('_')[3])
    start = timeit.default_timer()
    input_list_convert = convert_to_list(input_again, window, lookahead)
    output_message_new = decoding(input_list_convert)
    write_file(file_name+'_decompressed', save_extension, output_message_new)
    stop = timeit.default_timer()
    new_file = open("results.txt", "a+")
    new_file.write(str(stop-start) + "\n")
    new_file.close()
    print("Decompression took", stop - start, "seconds")


if __name__ == '__main__':
    main()
