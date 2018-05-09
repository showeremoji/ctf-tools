#!/usr/bin/env python2
import base64

# Standard form is a hex string without 0x at the start

def b642hex(b):
    return base64.b64decode(b).encode('hex')

def hex2b64(h):
    return h.decode("hex").encode("base64").strip()

if __name__ == '__main__':
    assert(b642hex('woidjw==') == 'c2889d8f')
    assert(hex2b64('c2889d8f') == 'woidjw==')
    print('Asserts passed')