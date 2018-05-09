#!/usr/bin/env python2
import base64

# Standard form is a hex string without 0x at the start

def b642hex(b):
    return base64.b64decode('woidjw==').encode('hex')

def hex2b64(h):
    return poop