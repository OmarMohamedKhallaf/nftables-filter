# returns the string as arrays of 128 bits
def split_string_128_bits(string):
    strings = []
    while len(string) != 0:
        strings.append(string[0:16])
        string = string[16:]
    return strings
