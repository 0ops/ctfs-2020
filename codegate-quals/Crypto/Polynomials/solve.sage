class Chall:
    def __init__(self, N, p, q):
        self.N, self.p, self.q = N, p, q
        self.R = PolynomialRing(Integers(q), "x")
        self.x = self.R.gen()
        self.S = self.R.quotient(self.x ^ N - 1, "x")
        self.h, self.f = None, None

    def random(self):
        return self.S([randint(-1, 1) for _ in range(self.N)])

    def keygen(self):
        while True:
            self.F = self.random()
            self.f = self.p * self.F + 1
            try:
                self.z = self.f ^ -1
            except:
                continue
            break
        while True:
            self.g = self.random()
            try:
                self.g ^ -1
            except:
                continue
            break
        self.h = self.p * self.z * self.g

    def getPublicKey(self):
        return list(self.h)

    def getPrivateKey(self):
        return list(self.f)

    def encrypt(self, m):
        m_encoded = self.encode(m)
        e = self.random() * self.h + self.S(m_encoded)
        return list(e)

    def decrypt(self, e, privkey):
        e, privkey = self.S(e), self.S(privkey)
        temp = map(Integer, list(privkey * e))
        temp = [t - self.q if t > self.q // 2 else t for t in temp]
        temp = [t % self.p for t in temp]
        pt_encoded = [t - self.p if t > self.p // 2 else t for t in temp]
        pt = self.decode(pt_encoded)
        return pt

    def encode(self, value):
        assert 0 <= value < 3 ^ self.N
        out = []
        for _ in range(self.N):
            out.append(value % 3 - 1)
            value -= value % 3
            value /= 3
        return out

    def decode(self, value):
        out = sum([(value[i] + 1) * 3 ^ i for i in range(len(value))])
        return out

    def count(self, row):
        p = sum([e == 1 for e in row])
        n = sum([e == self.q - 1 for e in row])
        return p, len(row) - p - n, n

def find_priv_key(c, hs, cnt, idx):
    # Guess f[i] == 0 for all i in idx(list)
    d = 1/3
    n = c.N
    m = []
    for i in range(n):
        if i in idx:
            continue
        tmp = [0] * n + hs[n-i:n] + hs[:n-i]
        tmp[i] = d
        m.append(tmp)
    for i in range(n):
        tmp = [0] * (n*2)
        tmp[n+i] = c.q
        m.append(tmp)
    mm = matrix(m)
    b = mm.LLL()

    ans = [i for i in b if i[0] in (1*d, -2*d, 4*d)]
    if ans:
        tmp = list(ans[0])
        g = c.S(tmp[n:])
        fs = [i*3 for i in tmp[:n]]
        f = c.S(fs)
        F = (f-1)/3
        if c.count(list(F)) == cnt:
            print "Found it!!!"
            return fs
    return None

def solve(n, p, q, pub_key, ct, cnt):
    chall = Chall(n, p, q)
    hs = [(i/Mod(chall.p, chall.q)).lift() for i in pub_key]
    for i in range(n):
        print i
        if i == 0:
            idx = []
        else:
            idx = [i]
        priv_key = find_priv_key(chall, hs, cnt, idx)
        if priv_key:
            plain = chall.decrypt(ct, priv_key)
            return plain

if __name__ == '__main__':
    pub1 = [3627, 1889, 3460, 2627, 3545, 1478, 2307, 3378, 3350, 1272, 2445, 3881, 3110, 1628, 1798, 1826, 259, 1983, 453, 52, 2650, 834, 3307, 907, 2762, 3452, 1085, 3059, 3544, 1136, 3767, 2346, 1952, 699, 3023, 531, 1208, 1449, 3636, 1742, 2692, 1128, 1683, 1152, 2584, 637, 3053, 2072, 2687, 1811, 2981, 3288, 2324, 3632, 1813]
    ct1 = [426, 3379, 3985, 160, 2502, 3592, 55, 1753, 3599, 2656, 2380, 582, 1038, 1028, 791, 1695, 1783, 3814, 3687, 3742, 1892, 1053, 2728, 3946, 801, 238, 3766, 1355, 1219, 528, 3560, 9, 3737, 1975, 1469, 85, 1373, 3717, 195, 3252, 2020, 1087, 201, 2536, 1655, 3380, 2322, 2438, 803, 2838, 1034, 457, 3050, 4010, 231]
    cnt1 = (22, 18, 15)
    pub2 = [314, 1325, 1386, 176, 369, 1029, 877, 1255, 111, 1226, 117, 0, 210, 761, 938, 273, 525, 751, 1085, 372, 1333, 898, 780, 44, 649, 1463, 326, 354, 116, 1080, 1065, 1109, 358, 275, 1209, 964, 101, 950, 415, 1492, 1197, 921, 1000, 1028, 1400, 43, 1003, 914, 447, 360, 1171, 1109, 223, 1134, 1157, 1383, 784, 189, 870, 565]
    ct2 = [378, 753, 466, 825, 320, 658, 630, 288, 16, 576, 134, 914, 549, 489, 197, 1392, 328, 361, 1241, 50, 710, 315, 526, 1250, 977, 453, 225, 433, 1342, 1005, 1432, 143, 1326, 1426, 1251, 1397, 237, 1202, 555, 83, 994, 446, 1406, 356, 1127, 1469, 485, 1034, 1224, 230, 1445, 825, 630, 1158, 815, 807, 837, 747, 423, 184]
    cnt2 = (20, 20, 20)

    pt1 = solve(55, 3, 4027, pub1, ct1, cnt1)
    pt2 = solve(60, 3, 1499, pub2, ct2, cnt2)
    print pt1, pt2
