"""
working file
"""


import os, sys
import binascii


# Don't think I'll need this...
# class PNGChunk(object):
#     def __init__(self):
#         self._length = int()
#         self._hex_data = str()
#         self._bin_data = str()
#         self._crc = str()
#
#     @property
#     def length(self):
#         return self._length
#
#     @length.setter
#     def length(self, val):
#         self.check_type(val, int)
#         self._length = val
#
#     @property
#     def hex_data(self):
#         return self._hex_data
#
#     @hex_data.setter
#     def hex_data(self, val):
#         self.check_type(val, str)
#         self._hex_data = val
#
#     @property
#     def bin_data(self):
#         return self._bin_data
#
#     @bin_data.setter
#     def bin_data(self, val):
#         check_type(val, str)
#         self._bin_data = val
#
#     @property
#     def crc(self):
#         return self._crc
#
#     @crc.setter
#     def crc(self, val):
#         check_type(val, str)
#         self._crc = val
#
#     def check_type(self, val, ought):
#         if (isinstance(val, ought)):
#             return True
#
#         raise TypeError("""
#                             Required type : {}
#                             You passed type : {}
#                             You passed value : {}
#                         """.format(ought, val, type(val))
#
# class IHDRChunk(PNGChunk):
#     def __init__(self):
#
#
#
# class PNGFile(object):
#     def __init__(self):
#         self._filepath = str()
#         self._width = int()
#         self._height = int()
#         self._bit_depth = int()
#         self._color_type = int()
#         self._compression_method = int()
#


def open_file(filepath):
    if (os.path.isfile(filepath) is False): raise ValueError()

    return open(filepath, "r+").read()

def is_png(data):
    first_eight = data[:8]
    PNG_id = "89 50 4e 47 0d 0a 1a 0a".replace("0x", "").lower()
    if (binascii.hexlify(first_eight) == PNG_id):
        return True
    return False

def type_to_eng(type_hex):
    try:
        int(type_hex, 16)
    except ValueError:
        raise TypeError("type_to_eng requires hex, you pass : {}".format(type_hex))

    type_hex = type_hex.replace("0x", "").lower()

    mapping = {
        "49484452" : "IHDR",
        "504c5445" : "PLTE",
        "49444154" : "IDAT",
        "49454e44" : "IEND",
        "74524e53" : "tRNS",
        "8348524d" : "cHRM",
        "67414d41" : "gAMA",
        "69434350" : "iCCP",
        "73424954" : "sBIT",
        "73524742" : "sRGB",
        "74455874" : "tEXt",
        "7a545874" : "zTXt",
        "69545874" : "iTXt",
        "624b4744" : "bKGD",
        "68495354" : "hIST",
        "70485973" : "pHYs",
        "73504c54" : "sPLT",
        "74494d45" : "tIME",
    }

    return mapping.get(type_hex, None)


def break_into_chunks(data):
    # TODO : consider using a buffer or StringIO

    # PNG's begin with an identifier. If this has not yet been stripped,
    # we should remove it
    PNG_id = "89 50 4e 47 0d 0a 1a 0a".replace(" " , "")
    if (binascii.hexlify(data[:8]) == PNG_id):
        data = data[8:]

    png = {}

    while data:

        # CHUNK LENGTH
        # First four bytes of a chunk are the length of its data (so excludes
        # name and CRC)
        chunk_len = data[:4]
        chunk_len = int(binascii.hexlify(chunk_len), 16)
        data = data[4:]

        # CHUNK TYPE
        # Second four bytes specify the type of chunk_len
        chunk_type = data[:4]
        chunk_type = binascii.hexlify(chunk_type)
        data = data[4:]

        # CHUNK DATA
        # the next n bytes (where n = chunk_len) are the actual data of the
        # chunk. If chunk_len = 0, this doesn't exist
        raw_chunk_data = data[:chunk_len]
        hex_chunk_data = binascii.hexlify(raw_chunk_data)
        data = data[chunk_len:]

        # CHUNK CRC
        # the next 4 bytes are the cyclic redundancy code (CRC)
        chunk_CRC = data[:4]
        chunk_CRC = binascii.hexlify(chunk_CRC)
        data = data[4:]

        png[chunk_type] = {
            "length" : chunk_len,
            "data" : hex_chunk_data,
            "raw_data" : raw_chunk_data,
            "crc" : chunk_CRC,
            "type" : type_to_eng(chunk_type)
        }

    return png

def process_IHDR(hex_str):
    hex_str = hex_str.replace(" ", "").strip()

    # Image Width (px)
    # four bytes
    width = hex_str[:8]
    hex_str = hex_str[8:]

    # Image Height (px)
    # four bytes
    height = hex_str[:8]
    hex_str = hex_str[8:]

    # Bit Depth
    # 1 bytes
    bit_depth = hex_str[:2]
    hex_str = hex_str[2:]

    # Color Type
    # 1 byte
    # e.g. Greyscale, TrueColor, TrueColor w/ alpha
    color_type = hex_str[:2]
    hex_str = hex_str[2:]

    # Compression Method
    # 1 byte
    compression_method = hex_str[:2]
    hex_str = hex_str[2:]

    # Filter Method
    # 1 byte
    filter_method = hex_str[:2]
    hex_str = hex_str[2:]

    # Interlace method
    # 1 byte
    interlace_method = hex_str[:2]
    hex_str = hex_str[2:]

    return {
        "width" : int(width, 16),
        "height" : int(height, 16),
        "bit_depth" : int(bit_depth, 16),
        "color_type" : int(color_type, 16),
        "compression_method" : int(compression_method, 16),
        "filter_method" : int(filter_method, 16),
        "interlace_method" : int(interlace_method, 16),
    }

def process_IDAT(hex_str):

    # Compression Method
    # 1 byte
    # "8" indicates "DEFLATE" compression
    compression_method = hex_str[:2]
    hex_str[2:]

    # Additional Flag
    # 1 byte
    # for compression_method = 8:
    # addl_flag = log2(LZ77 window size) - 8
    addl_flag = hex_str[:2]
    hex_str[2:]

    # Compressed Data Blocks
    # n bytes
    data_blocks = hex_str[:-4]
    hex_str = [-4:]

    # Check Value
    # 4 bytes
    check_value = hex_str[:4]
    hex_str = hex_str[4:]

    return {
        "compression_method" : int(compression_method, 16),
        "addl_flag" : int(addl_flag, 16),
        "data_blocks" : data_blocks,
        "check_value" : check_value
    }

if __name__ == "__main__":
    fp = "/Users/LukeGilson/misc_scripts/png/test_png_1px.png"
    data = open_file(fp)
    k = break_into_chunks(data)
    k["49484452"].update(process_IHDR(k["49484452"]["data"]))
    for i in k:
        print "=== {} ===".format(i)
        for j in k[i]:
            print "{} : {}".format(j, k[i][j])
