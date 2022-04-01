from __init__ import *

if __name__ == '__main__':
    print("To see SSL packets containing SNI:\n\t"
          "tcpdump -nnXS -i any -s 400 '(tcp[((tcp[12:1] & 0xf0) >> 2)+5:1] = 0x01) and (tcp[((tcp[12:1] & 0xf0) >> "
          "2):1] = 0x16)'\n"
          "Search for the index at which the domain starts in the hex dump")
