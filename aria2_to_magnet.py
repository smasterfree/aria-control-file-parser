#!/usr/bin/env python
import argparse
import os
import glob
"""
Usage:
command line
windows: python aria2_to_magnet.py [path]|[-r --recursive]
bash:    python3 aria2_to_magnet.py [path]|[-r --recursive]
example: python aria2_to_magnet.py ./
"""


def main():
    file_parser(parse_aria_control_file)


def file_parser(handler_func):
    # codes from gist
    # https://gist.github.com/89465127/5273149
    parser = argparse.ArgumentParser(
        description='Read in a file or set of files, and return the result.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('path',
                        nargs='+',
                        help='Path of a file or a folder of files.')
    # no need extension filter for aria2 file
    parser.add_argument('-e',
                        '--extension',
                        default='.aria2',
                        help='File extension to filter by.')

    parser.add_argument('-r',
                        '--recursive',
                        action='store_true',
                        default=False,
                        help='Search through subfolders')

    args = parser.parse_args()

    # Parse paths
    full_paths = [os.path.join(os.getcwd(), path) for path in args.path]
    files = set()
    for path in full_paths:
        if os.path.isfile(path):
            fileName, fileExt = os.path.splitext(path)
            if args.extension == '' or args.extension == fileExt:
                files.add(path)
        else:
            if (args.recursive):
                full_paths += glob.glob(path + '/*')
            else:
                files |= set(glob.glob(path + '/*' + args.extension))

    for f in files:
        handler_func(f)


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
    try:
        with open(file_name, "rb") as f:
            # f.seek(0)  # Go to beginning, read VER
            # version = f.read(2)
            # i = int.from_bytes(version, 'big')
            # print(f'version is {i}')

            # skip  EXT, find info  hash_binary length
            f.seek(6)
            length = f.read(4)
            hash_length = int.from_bytes(length, 'big')
            # print(f"hash length is {hash_length}")

            # read next hash_length
            f.seek(10)  # Go to info hash
            hash_binary = f.read(hash_length)
            info_hash = hash_binary.hex().upper()

            magnet_link = "magnet:?xt=urn:btih:" + info_hash
            print(f'file name: {os.path.basename(file_name)}, {magnet_link}')
    except FileNotFoundError:
        print(f'file not found. {file_name}')


if __name__ == '__main__':
    # version is 1
    # hash length is 20
    # magnet:?xt=urn:btih:959E2ECEB954313D38690EFF7924CA7CD80DE739
    main()
