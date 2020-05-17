#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "Michał Kołodziejski <mailto: michal.kolodziejski@gmail.com>"
__copyright__ = "Copyright (C) 2020 Michał Kołodziejski"
__license__ = "GPLv3"
__version__ = "1.0"

# usage:
# -i/input => input filename
# -o/output => output filename
# -a/address => address for $E
# -n/name => BYTE ARRAY variable name

import time, sys
import more_itertools
import argparse

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print(f'{method.__name__} {(te - ts) * 1000} ms')
        return result
    return timed


def querySingleByte(value):
    return (f'${value:02x}')


@timeit
def process(argv):
    print("")
    print('*******************************************')
    print('*** BINARY to BYTE ARRAY Converter v1.0 ***')
    print('*** 2020 © Michał Kołodziejski          ***')
    print('*** updated: 20200517 21:50             ***')
    print('*** GPLv3                               ***')
    print('*******************************************')
    print("")

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input filename", required=True, type=str)
    parser.add_argument("-o", "--output", help="output filename", required=True, type=str)
    parser.add_argument("-a", "--address", help="address for $E", required=True, type=str)
    parser.add_argument("-n", "--name", help="BYTE ARRAY variable name", required=True, type=str)

    args = parser.parse_args()

    dataset_filename = args.input
    dataset_address = args.address
    dataset_name = args.name
    output_filename = args.output

    bytes_in_line = 16

    in_file = open(dataset_filename,'rb')
    contents = in_file.read()
    in_file.close()

    out_file = open(output_filename,'w')

    out_file.write('BYTE ARRAY\n')
    out_file.write(f'SET $E={dataset_address}\n')
    out_file.write(f'{dataset_name}=\n')
    out_file.write('[\n')

    
    for line in more_itertools.windowed(contents, n=bytes_in_line, step=bytes_in_line):
        for byte in line:
            out_file.write(f'{querySingleByte(byte)}')
         
        out_file.write("\n")

    out_file.write(']\n')

    out_file.close()


if __name__ == "__main__":
    process(sys.argv[1:])
