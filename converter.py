#!/usr/bin/env python2
import base64
import binascii

# Standard form is a hex string without 0x at the start

def b642hex(b):
    return base64.b64decode(b).encode('hex')

def hex2b64(h):
    return h.decode("hex").encode("base64").strip()

def bin2hex(b):
    o = hex(int(b, 2))[2:]
    return o[:-1] if o[-1] == 'L' else o

def hex2bin(h):
    return bin(int(h, 16))[2:]

def int2hex(i):
    i = int(i)
    return hex(i)[2:]

def hex2int(h):
    return int('0x' + h, 16)

def convert(src, dst, s):
    srcf = {'hex': lambda x: x,
            'int': int2hex,
            'bin': bin2hex,
            'b64': b642hex}
    dstf = {'hex': lambda x: x,
            'int': hex2int,
            'bin': hex2bin,
            'b64': hex2b64}
    if src not in srcf:
        raise 'src format {} not supported'.format(src)
    if dst not in dstf:
        raise 'dst format {} not supported'.format(dst)
    return dstf[dst](srcf[src](s))

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
    
    assert(bin2hex('0111010101010100000000101010100101010101010010101010101010010101010101010010101010101001110101010101000000001010101001010101010100101010101010100101010101010100101010101010011101010101010000000010101010010101010101001010101010101001010101010101001010101010100111010101010100000000101010100101010101010010101010101010010101010101010010101010101001110101010101000000001010101001010101010100101010101010100101010101010100101010101010011101010101010000000010101010010101010101001010101010101001010101010101001010101010100111010101010100000000101010100101010101010010101010101010010101010101010010101010101001110101010101000000001010101001010101010100101010101010100101010101010100101010101010011101010101010000000010101010010101010101001010101010101001010101010101001010101010100111010101010100000000101010100101010101010010101010101010010101010101010010101010101001110101010101000000001010101001010101010100101010101010100101010101010100101010101010011101010101010000000010101010010101010101001010101010101001010101010101001010101010100111010101010100000000101010100101010101010010101010101010010101010101010010101010101001110101010101000000001010101001010101010100101010101010100101010101010100101010101010') == '755402a9554aaa95552aa9d5500aa5552aaa5554aaa755402a9554aaa95552aa9d5500aa5552aaa5554aaa755402a9554aaa95552aa9d5500aa5552aaa5554aaa755402a9554aaa95552aa9d5500aa5552aaa5554aaa755402a9554aaa95552aa9d5500aa5552aaa5554aaa755402a9554aaa95552aa9d5500aa5552aaa5554aaa755402a9554aaa95552aa9d5500aa5552aaa5554aaa')

    assert convert('int', 'int', 100) == 100
    assert convert('hex', 'hex', "14d") == "14d"

    print('Asserts passed')
