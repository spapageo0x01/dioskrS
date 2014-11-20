import os
import inspect
import sys

class BlockStore:
    def __init__(self, input_file, block_size, output_dir):
        self.input_file = input_file
        self.block_size = block_size

        file_size = os.stat(input_file).st_size
        print 'file_size: %d' % file_size

        #Should handle this later on.
        if (file_size < block_size):
            print 'File provided is smaller than the deduplication block size.'
            sys.exit(0)

        if not (os.path.isdir(output_dir)):
            print 'Output directory "%s" does not exist. Will create..' % output_dir
            os.makedirs(output_dir)

        try:
		    self.file_fp = os.open(self.input_file, os.O_DIRECT | os.O_RDONLY)
        except Exception as e:
            frame = inspect.currentframe()
            info = inspect.getframeinfo(frame)
            print '\t[fopen: an %s exception occured | line: %d]' % (type(e).__name__, info.lineno)
            sys.exit(0)


    def get_sync(self, byte_offset=0):
    	block = ''
        try: 
            block = os.read(self.file_fp, self.block_size)
        except Exception as e:
            frame = inspect.currentframe()
            info = inspect.getframeinfo(frame)
            print '\t[read: an %s exception occured | line: %d]' % (type(e).__name__, info.lineno)
            sys.exit(0);

        return block