import sys
from compression.huffman import EncodeStream

fp = input("what is the full filepath you want to see compression for? ")

f = open(fp)
stream = f.read()
# just dealing with ascii for now
stream = ''.join([i if ord(i) < 128 else ' ' for i in stream])

es = EncodeStream()
es.raw_stream = bytearray(stream, "ascii")
es.encode()
raw_length = sys.getsizeof(es.raw_stream)
encoded_length = sys.getsizeof(es.encoded_stream)

print("""
        The original file was {} bytes long
        The new file is {} bytes long
        The compressed file is {}% of the original
        """.format(raw_length, encoded_length, round(encoded_length/raw_length, 2) * 100))
