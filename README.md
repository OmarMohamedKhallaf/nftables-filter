# nftables filter

nftables filter is a python script that generates nftable rules to drop requests to certain websites.
The rules drop SSL hello packet as it contains SNI which allows us to filter traffic by domain and subdomains.
Dropping of SSL hello packet interrupts the SSL handshake, ultimately resulting in dropping the whole connection.

## Installation

Clone the repository

```bash
git clone https://github.com/OmarMohamedKhallaf/nftables-filter.git
```

## Usage
Suppose you want to block Youtube on mobile devices 
```bash
$ sudo tcpdump -nnXS -i any -s 400 '(tcp[((tcp[12:1] & 0xf0) >> 2)+5:1] = 0x01) and (tcp[((tcp[12:1] & 0xf0) >> 2):1] = 0x16)'
...
        0x00b0:  0000 0d6d 2e79 6f75 7475 6265 2e63 6f6d  ...m.youtube.com
                                                             ^
                                                        start index
...
# the index in packet at which the SNI exists is 0xb3
$ python -i main.py
>>> ssl_sni_filter("m.youtube.com", 0xb3)
@nh,1432,104 0x6d2e796f75747562652e636f6d drop comment "drop connections to m.youtube.com"

```
Generally the rule should be in a table similar to the following strucutre:
```
table inet filter {
  chain forward {
    type filter hook forward priority filter
    policy drop

    # packets which start with the following two bytes have SNI (maybe someone with better understanding of the protocol could explain this)
    iif $lan_if oif $wan_if @nh,0,16 0x4500 jump forward_filter_https
    ct state { related, established } accept
    # rules to accept new traffic...
  }

  chain forward_filter_https {
    @nh,1432,104 0x6d2e796f75747562652e636f6d drop comment "drop connections to m.youtube.com"
  }
}
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)