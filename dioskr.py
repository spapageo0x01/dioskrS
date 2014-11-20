#!/usr/bin/python

#TODO: create a torrent file for reconstruction purposes!

import sys
import argparse
import os
import hashlib
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

if __name__ == "__main__":
    print '=======dioskrS v0.1========'
    input_file, block_size = init_vars()

    block_eng = BlockStore(input_file, block_size, output_dir)

    blocks_nr = 0
    while True:
        block = block_eng.get_sync()
        blocks_nr += 1
        hash_object = hashlib.sha512(block)
        hex_dig = hash_object.hexdigest()

        if block == "":
            break

    print 'Finished reading file! Number of %d blocks: %d' % (block_size, blocks_nr)


