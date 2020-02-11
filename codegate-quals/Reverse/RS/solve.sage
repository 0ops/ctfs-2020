'''
By debugging, we know that the core function is at 0x97F0 as below:
void __fastcall enc(Str *out, Str *key, char *in, size_t in_size)
It uses addition and multiplication on GF(2^8).
I didn't dive into Rust so Str struct may be wrong:
struct Str
{
  char *buf;
  unsigned __int64 capacity;
  unsigned __int64 size;
};
'''
M.<a> = GF(2)[]
P.<x> = GF(256,modulus=a^8 + a^4 + a^3 + a^2 + 1)
res = [239, 67, 75, 63, 94, 185, 240, 208, 140, 181, 126, 111, 123, 200, 166, 123, 9, 226, 97, 157, 152, 3, 95, 86, 93, 102, 130, 11, 158, 43, 118, 146, 91, 195, 220, 242, 60, 208, 182, 129, 96, 52, 165, 102, 202, 189, 125, 106, 0, 254, 228, 11, 68, 225, 186, 129, 203, 174, 139, 36, 11, 165, 31, 109, 186, 14, 97, 26, 48, 167, 119, 81, 35, 65, 166, 26, 192, 127, 113, 113, 159, 213, 147, 229, 56, 206, 82, 139, 37, 134, 179, 18, 183, 167, 28, 67, 180, 8, 129, 71, 174, 214, 24, 70, 197, 107, 105, 99, 11, 204, 149, 171, 73, 83, 111, 222, 190, 47, 46, 217, 155, 220, 221, 118, 105, 164, 240, 88]
raw_key = [1, 116, 64, 52, 174, 54, 126, 16, 194, 162, 33, 33, 157, 176, 197, 225, 12, 59, 55, 253, 228, 148, 47, 179, 185, 24, 138, 253, 20, 142, 55, 172, 88]
key = [P.fetch_int(i) for i in raw_key]

PP.<x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15> = P[]
vs = [x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15]
tmp = vs+[0]*32
for i in range(16):
    for j in range(32):
        tmp[i+j+1] += tmp[i]*key[j+1]
p2v = lambda x:vector(x.coefficients())
m = matrix(map(p2v,tmp[-32:]))

def solve(r):
    tmp = m.solve_right(vector([P.fetch_int(i) for i in r]))
    tmp = bytearray([i.integer_representation() for i in tmp])
    return tmp

flag=bytearray()
for i in range(0,128,32):
    flag += solve(res[i:i+32])
print flag
