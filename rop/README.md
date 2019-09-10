gets (can-you-gets-me)  ROP
===========================

First, we note that the stack is marked as non-executable, since

`readelf -l gets`

has the following line 

`  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RW  0x10`

in which `RW` shows that the stack is only read/write, not executable (E).

Another way to do this is to have gdb-peda installed, and then run `checksec`
which also prints some various other security measures.

So, we can't do a regular shellcode-on-the-stack-attack, but must instead do a
ROP attack.

By using `file` we can also see that the binary is not position-independent
(there is no PIE in the output). It is also statically linked, so we can look
for gadgets inside it, and also find a suitable gadget to launch.

Looking through radare2 / gdb we notice that there isn't any system or execve
functions within the binary. Probably, since the binary is statically linked,
they have been left out. Instead, we need to construct the syscall manually.

First, we look for a "int 0x80; ret" gadget (the 0x80 interrupt is the interrupt
for an Linux x86 syscall). To make an execve syscall, the registers need to be
set to the following values.

eax = syscall number = (which is 0x0b for execve)
ebx = pointer to filename to execute
ecx = pointer to argv
edx = pointer to envp

We can set ecx and edx to NULL, ebx to /bin/sh, eax to 0x0b and then run
the interrupt.

Step 1. 

Find `int 0x80; ret;` gadget to make a syscall.
```
[linus@ctfpad]$ ropper --file gets --search 'int 0x80;'
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: int 0x80;

[INFO] File: gets
0x0806cd95: int 0x80; 
0x0806f7a0: int 0x80; ret; 
```
so we have a suitable gadget at 0x0806f7a0.

Step 2.

We now need to fill the registers with suitable stuff. We start with ebx which
should contain the filename (/bin/sh) since this is probably the most tricky part.
The idea is to find a suitable writable memory location where we can put data,
then load the string to a memory location.

By launching `gdb ./gets`, run it, then break and look at memory using `vmmap`
we see that there is a nice memory area `0x080e9000-0x080eb000` which is writable.

The idea is then to have two gadgets that perform:
1) pop 32-bit into some register RX
2) mov from RX to memory.

We find the following suitable gadgets using ropper.

```
0x08054b4b: mov dword ptr [edx], eax; ret;
0x080b84d6: pop eax; ret;
0x0806f19a: pop edx; ret;
0x080481c9: pop ebx; ret;
```

So the steps become:
1. Load eax with '/bin' (as int)
2. Load edx with 0x080e9330 (arbitrarily chosen within range)
3. Run mov [edx], eax gadget.
4. Repeat for '/sh\0'
5. Pop value of arbitrary address to ebx

Step 3. We now need to fix so ecx and edx is set to NULL.
We don't have any suitable xor ecx, ecx gadgets, so we need
to fill the register with a value and the add 1.

We use the following gadgets, and first pop 0xffffffff
```
0x080dece1: pop ecx; ret;
0x080d608f: inc ecx; ret;
0x0806f19a: pop edx; ret;
0x0805d207: inc edx; ret; 
```

Step 4. We now want to move 0x0b to eax since this represents execve syscall.
We can do that (without using null bytes) by moving e.g. 0x2222220b
to eax (by popping), and then zero-extend using movzx to get 0x0000000b
```
0x080b84d6: pop eax; ret;
0x08091d09: movzx eax, al; ret; 
```

Step 5. Finally perform the syscall
```
0x0806f7a0: int 0x80; ret; 
```

DONE!

Inspired by the following very nice guide!

http://barrebas.github.io/blog/2015/06/28/rop-primer-level0/
