#!/usr/bin/env python3
from Crypto.PublicKey import RSA
from Crypto.Util.number import getPrime, bytes_to_long as b2l
from itertools import cycle
from random import randint


class reveal:
    def __init__(self, info, bitlen):   # info是p分成4段的数组，有3段少35个bit，bitlen是p的bit长度（应该是512）
        self.coeff = cycle(info)        # 循环 info
        self.prime = getPrime(bitlen)   # 得到一个与p长度相同的素数
        self.bitlen = bitlen            # 应该是512
        self.seed = randint(1, self.prime)  
        print("[*] Revealing...")
        print(self.prime, self.seed)
        print([chunk.bit_length() for chunk in info])   # info里每一段的长度，上面推测的应该正确

    def __iter__(self):
        return self

    def __next__(self):
        temp = next(self.coeff) * self.seed % self.prime
        self.seed = self.seed ** 2 % self.prime
        return Chall.munch(temp, self.bitlen * 9 // 10, self.bitlen)


class Chall:
    def __init__(self, size, n, cutoff):    # size = 1024, n = 3, cutoff = 200
        self.key = RSA.generate(size)       # 加密flag的密钥
        self.cutoff = cutoff                #
        self.p, self.nchunks = self.key.p, 2 * n + 1    # 素数p，nchunks = 7
        self.info = []                      # 存放泄露信息
        print(self.key.n)

    def munchprime(self):
        bitlen = self.p.bit_length()    # bitlen为p的比特长度
        for i in range(0, bitlen, 2 * bitlen // self.nchunks):  # 步长约为 1024 / 7 = 146
            bite = self.munch(self.p, i, 2 * bitlen // self.nchunks - 35)   # 每隔一个步长泄露p的一些bit，每次泄露146 - 35 = 111 bit。 总共少105bit
            self.info.append(bite)

    def expose(self):
        leak = reveal(self.info, self.p.bit_length())
        print("[*] Leaking...")
        for i in range(self.cutoff):
            print(next(leak))

    def getflag(self):
        flag = b2l(open("flag.txt", "rb").read())
        c = pow(flag, self.key.e, self.key.n)
        return c

    @staticmethod
    def munch(target, start, length):   # 返回target从第start位的高length位数字
        return (target >> start) & ((1 << length) - 1)


if __name__ == "__main__":
    chall = Chall(1024, 3, 200)
    print("[*] Here is your challenge:")
    print(chall.getflag())
    chall.munchprime()
    chall.expose()
