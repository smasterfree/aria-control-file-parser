#!/usr/bin/env python
import struct
import binascii
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", nargs='+',
                    help="input file XXX.aria2")

args = parser.parse_args()


# ================================================================
#  0                   1                   2                   3
#  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +---+-------+-------+-------------------------------------------+
# |VER|  EXT  |INFO   |INFO HASH ...                              |
# |(2)|  (4)  |HASH   | (INFO HASH LENGTH)                        |
# |   |       |LENGTH |                                           |
# |   |       |  (4)  |                                           |
# +---+---+---+-------+---+---------------+-------+---------------+
# |PIECE  |TOTAL LENGTH   |UPLOAD LENGTH  |BIT-   |BITFIELD ...   |
# |LENGTH |     (8)       |     (8)       |FIELD  | (BITFIELD     |
# |  (4)  |               |               |LENGTH |  LENGTH)      |
# |       |               |               |  (4)  |               |
# +-------+-------+-------+-------+-------+-------+---------------+
# |NUM    |INDEX  |LENGTH |PIECE  |PIECE BITFIELD ...             |
# |IN-    |  (4)  |  (4)  |BIT-   | (PIECE BITFIELD LENGTH)       |
# |FLIGHT |       |       |FIELD  |                               |
# |PIECE  |       |       |LENGTH |                               |
# |  (4)  |       |       |  (4)  |                               |
# +-------+-------+-------+-------+-------------------------------+
#
#         ^                                                       ^
#         |                                                       |
#         +-------------------------------------------------------+
#                 Repeated in (NUM IN-FLIGHT) PIECE times

# more detail
# https://aria2.github.io/manual/en/html/technical-notes.html
# ================================================================

def parse_aria_control_file(file_name):
    with open(file_name, "rb") as f:
        try:

            f.seek(0)  # Go to beginning, read VER
            version = f.read(2)

            i = int(version.encode('hex'), 16)
            # print "version is " + str(i)

            # skip  EXT, find info  hash_binary length
            f.seek(6)

            length = f.read(4)
            hash_length = int(length.encode('hex'), 16)
            # print "hash length is " + str(hash_length)

            # read next hash_length
            f.seek(10)  # Go to info hash
            hash_binary = f.read(hash_length)
            info_hash = ""
            for ch in hash_binary:
                hex_word = hex(ord(ch))[2:].zfill(2)
                # print hex_word

                info_hash += hex_word.upper()

            magnet_link = "magnet:?xt=urn:btih:" + info_hash
            print magnet_link
        except:
            pass
        finally:
            f.close()


if __name__ == '__main__':
    file_list = args.file
    for file_name in file_list:
        parse_aria_control_file(file_name)
    # version is 1
    # hash length is 20
    # magnet:?xt=urn:btih:959E2ECEB954313D38690EFF7924CA7CD80DE739
