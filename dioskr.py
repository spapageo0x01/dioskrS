#!/usr/bin/python

#TODO: create a torrent file for reconstruction purposes!!!

import sys
import argparse
import os
import hashlib

output_dir = "/mnt/shared_volume/dskrs_field"

def init_vars():
    parser = argparse.ArgumentParser(description='dioskr input parameters.')
    parser.add_argument('input_file', help='input file path')
#    parser.add_argument('output_dir', help='output directory')
    parser.add_argument('block_size', help='size of block deduplication in bytes')
    args = parser.parse_args()

    return args.input_file, args.block_size

def main():
    input_file = ''
    block_sz = 4096

    print "=======dioskrS v0.1========"

    input_file, block_sz = init_vars()

    file_sz = os.stat(input_file).st_size
    print "file_sz: %d" % file_sz
    if (file_sz < 10485760):
        print "Please provide a file larger than 10MB!"
        sys.exit(0)

    block_sz = int(block_sz)
    #Check if block size is greater than 512 bytes
    if (block_sz < 4096):
        print "Block size should be > 4096 bytes"
        sys.exit(0)

    #Check if block size is aligned
    if ((block_sz % 4096) != 0):
        print "Block size provided is not 4KB aligned"
        sys.exit(0)

    #file_fp = open(input_file, "rb") #alternate open, built-in, not direct!
    file_fp = os.open(input_file, os.O_DIRECT | os.O_RDONLY)
    
    if not (os.path.isdir(output_dir)):
        print "Output directory \"%s\" does not exist. Will create.." % output_dir
        os.makedirs(output_dir)

    blocks_nr = 0
    while True:
        #block = file_fp.read(block_size)
        block = os.read(file_fp, block_sz)
        blocks_nr += 1

        hash_object = hashlib.sha512(block)
        hex_dig = hash_object.hexdigest()
        #print"%d: %s" % (blocks_nr, hex_dig)

        # Check first 8 characters in output_dir, move one level down
        # Check next 8 characters in output_dir/something, move one level down
        # Check if file exists, if not, create



        if block == "":
            break

    print "Finished reading file! Number of %d blocks: %d" % (block_sz, blocks_nr)




if __name__ == "__main__":
	main()