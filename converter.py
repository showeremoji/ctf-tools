#!/usr/bin/env python2
import base64
import binascii

# Standard form is a hex string without 0x at the start

def b642hex(b):
    return base64.b64decode(b).encode('hex')

def hex2b64(h):
    return h.decode("hex").encode("base64").strip()

def bin2hex(b):
    return hex(int(b, 2))[2:]

def hex2bin(h):
    return bin(int(h, 16))[2:]

def int2hex(i):
    i = int(i)
    return hex(i)[2:]

def hex2int(h):
    return int('0x' + h, 16)

if __name__ == '__main__':
    assert(b642hex('woidjw==') == 'c2889d8f')
    assert(hex2b64('c2889d8f') == 'woidjw==')

    assert(bin2hex('1100000011011110') == 'c0de')
    assert(hex2bin('c0de') == '1100000011011110')

    assert(hex2int('1') == 1)
    assert(int2hex(1) == '1')
    assert(hex2int('f') == 15)
    assert(int2hex(15) == 'f')
    assert(hex2int('ff') == 255)
    assert(int2hex(255) == 'ff')
    assert(hex2int('3e8') == 1000)
    assert(int2hex(1000) == '3e8')

    print('Asserts passed')
