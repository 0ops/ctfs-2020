from pwn import *
import re

context.log_level = "error"

def to_byte_16(nonce):
    return hex(nonce)[2:].strip("L").zfill(32)

def encrypt(r, plaintext):
    r.sendline("1")
    r.sendlineafter("plaintext = ", plaintext.encode("hex"))
    
    tmp = r.recvuntil("> ")
    pattern = re.compile(r"ciphertext = ([0-9a-f]+)\ntag = ([0-9a-f]+)")

    ciphertext, tag = re.findall(pattern, tmp)[0]
    return ciphertext, tag

def decrypt(r, nonce, ciphertext, tag):
    r.sendline("2")
    r.sendlineafter("nonce = ", to_byte_16(nonce))
    r.sendlineafter("ciphertext = ", ciphertext)
    r.sendlineafter("tag = ", tag)
    tmp = r.recvuntil("> ")
    pattern = re.compile(r"plaintext = ([0-9a-f]+)\n")
    plaintext = re.findall(pattern, tmp)[0]
    return plaintext.decode("hex")

def execute(r, nonce, ciphertext, tag):
    r.sendline("3")
    r.sendlineafter("nonce = ", to_byte_16(nonce))
    r.sendlineafter("ciphertext = ", ciphertext)
    r.sendlineafter("tag = ", tag)
    print r.recv()


def try_encrypt(data):
    r = remote("110.10.147.44", 7777)
    r.recvuntil("> ")
    c, t = encrypt(r, data)
    r.close()
    return c.decode("hex"), t

def try_decrypt(ciphertext, tag):
    r = remote("110.10.147.44", 7777)
    r.recvuntil("> ")
    tmp = decrypt(r, 0, ciphertext.encode("hex"), tag)
    r.close()
    return tmp
 

def attack():
    p1 = "aaaabbbb;cat flaeeeeffffgggghhhh"
    c0, _ = try_encrypt(p1)
    p2 = "AAAABBBBCCCCDDDD%c%cEEFFFFGGGGHHHH" % (chr(211 ^ ord("g")), chr(186 ^ ord(";")))
    c1, t1 = try_encrypt(p2)
    cc = c0[0:16] + c1[16:24] + xor(c0[24:32], "gggghhhh", "GGGGHHHH")

    print cc.encode("hex"), t1

    r = remote("110.10.147.44", 7777)
    r.recvuntil("> ")
    execute(r, 0, cc.encode("hex"), t1)

attack()