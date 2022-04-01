import utils


# creates a rule that match ssl hello packet containing the host at the specific index
def ssl_sni_filter(host, index=0xb3):
    match_string = ""
    match_parts = utils.split_string_128_bits(host)
    for i in range(0, len(match_parts)):
        index_in_bits = int(index) * 8 + i * 128
        len_in_bits = len(match_parts[i]) * 8
        str_in_hex = match_parts[i].encode("utf-8").hex()
        match_string += f"@nh,{index_in_bits},{len_in_bits} 0x{str_in_hex} "
    match_string += f"drop comment \"drop connections to {host}\""
    print(match_string)
