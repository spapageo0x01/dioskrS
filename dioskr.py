#!/usr/bin/python

#TODO: create a torrent file for reconstruction purposes!

import sys
import argparse
import os
import hashlib
import inspect
from layer_block import BlockStore


output_dir = "/mnt/shared_volume/dskrs_field"

def input_check(arg):
    #check if file exists
    if os.path.isfile(arg) is False:
        raise argparse.ArgumentTypeError('Input file does not exist')

    return arg


def block_check(arg):
    value = int(arg)
    if value <= 0:
        raise argparse.ArgumentTypeError('Block size should be a positive value')

    if ((value % 4096) != 0):
        raise argparse.ArgumentTypeError('Block size should be 4K aligned')

    return value

def init_vars():
    parser = argparse.ArgumentParser(description='dioskr input parameters.')
    parser.add_argument('input_file', default='', type=input_check, help='input file path')
    parser.add_argument('block_size', default='4096', type=block_check, help='size of block deduplication in bytes')
    #parser.add_argument('output_dir', help='output directory')
    args = parser.parse_args()

    return args.input_file, args.block_size

def main():
    print '=======dioskrS v0.1========'
    input_file, block_size = init_vars()

    file_size = os.stat(input_file).st_size
    print 'file_size: %d' % file_size

    #Should handle this later on.
    if (file_size < block_size):
        print 'File provided is smaller than the deduplication block size.'
        sys.exit(0)

    #file_fp = open(input_file, "rb") #alternate open, built-in, not direct!
    try: 
        file_fp = os.open(input_file, os.O_DIRECT | os.O_RDONLY)
    except Exception as e:
        frame = inspect.currentframe()
        info = inspect.getframeinfo(frame)
        print '\t[fopen: an %s exception occured | line: %d]' % (type(e).__name__, info.lineno)
        sys.exit(0)

    if not (os.path.isdir(output_dir)):
        print 'Output directory "%s" does not exist. Will create..' % output_dir
        os.makedirs(output_dir)


    blocks_nr = 0
    while True:
        #block = file_fp.read(block_size)
        try: 
            block = os.read(file_fp, block_size)
            blocks_nr += 1
            hash_object = hashlib.sha512(block)
            hex_dig = hash_object.hexdigest()
        except Exception as e:
            frame = inspect.currentframe()
            info = inspect.getframeinfo(frame)
            print '\t[read: an %s exception occured | line: %d]' % (type(e).__name__, info.lineno)
            break

        #print"%d: %s" % (blocks_nr, hex_dig)


        if block == "":
            break

    print 'Finished reading file! Number of %d blocks: %d' % (block_size, blocks_nr)



if __name__ == "__main__":
	main()


