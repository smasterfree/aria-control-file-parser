# aria-control-file-parser

Parse aria2c control file from cmd line.

When use aria2c to download magnet, use ctrl+c to kill aria2c process, or system reboot or shutdown, then if you need to continue the download process, you have to find what the original magnet link.

See this issue(https://github.com/aria2/aria2/issues/792). 

From the aria technical notes, the .aria2 (Control File) contain the hash info of
the magnet link, so  parse the file we could get the original magnet link.

Also @alphatr write a tool transform .aria2 file to a magnet link use javascript.


```
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
```

## how to run

```bash
python aria2_to_magnet.py dahufa.aria2
```

output
```
magnet:?xt=urn:btih:959E2ECEB954313D3869EFF7924CA7CD8DE739
```

with multiple files
```bash
python aria2_to_magnet.py *.aria2
```

