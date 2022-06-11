# LZW Encoder
# Name: Aditya Gupta
# ID: 800966229
# ITCS 6114

import sys
from sys import argv
from struct import *

# taking the input file and the number of bits from command line
# defining the maximum table size
# opening the input file
# reading the input file and storing the file data into data variable
def lzw_encode(data,n):
    maximum_table_size = pow(2,int(n))
    # Building and initializing the dictionary.
    dictionary_size = 128
    dictionary = {chr(i): i for i in range(dictionary_size)}
    string = ""             # String is null.
    compressed_data = []    # variable to store the compressed data.

    # iterating through the input symbols.
    # LZW Compression algorithm
    for symbol in data:
        string_plus_symbol = string + symbol # get input symbol.
        if string_plus_symbol in dictionary:
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if(len(dictionary) <= maximum_table_size):
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            string = symbol

    if string in dictionary:
        compressed_data.append(dictionary[string])

    # storing the compressed string into a file (byte-wise).

    datas = b""
    for data in compressed_data:
        datas+=pack('>H',int(data))
    return datas

