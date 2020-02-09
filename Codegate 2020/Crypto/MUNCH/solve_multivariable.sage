class IIter:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.arr = [0 for _ in range(n)]
        self.sum = 0
        self.stop = False
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.stop:
            raise StopIteration
        ret = tuple(self.arr)
        self.stop = True
        for i in range(self.n - 1, -1, -1):
            if self.sum == self.m or self.arr[i] == self.m:
                self.sum -= self.arr[i]
                self.arr[i] = 0
                continue
            
            self.arr[i] += 1
            self.sum += 1
            self.stop = False
            break
        return ret

tttmp = [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3), (0, 0, 4), (0, 0, 5), (0, 0, 6), (0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 1, 3), (0, 1, 4), (0, 1, 5), (0, 2, 0), (0, 2, 1), (0, 2, 2), (0, 2, 3), (0, 2, 4), (0, 3, 0), (0, 3, 1), (0, 3, 2), (0, 3, 3), (0, 4, 0), (0, 4, 1), (0, 4, 2), (0, 5, 0), (0, 5, 1), (0, 6, 0), (1, 0, 0), (1, 0, 1), (1, 0, 2), (1, 0, 3), (1, 0, 4), (1, 0, 5), (1, 1, 0), (1, 1, 1), (1, 1, 2), (1, 1, 3), (1, 1, 4), (1, 2, 0), (1, 2, 1), (1, 2, 2), (1, 2, 3), (1, 3, 0), (1, 3, 1), (1, 3, 2), (1, 4, 0), (1, 4, 1), (1, 5, 0), (2, 0, 0), (2, 0, 1), (2, 0, 2), (2, 0, 3), (2, 0, 4), (2, 1, 0), (2, 1, 1), (2, 1, 2), (2, 1, 3), (2, 2, 0), (2, 2, 1), (2, 2, 2), (2, 3, 0), (2, 3, 1), (2, 4, 0), (3, 0, 0), (3, 0, 1), (3, 0, 2), (3, 0, 3), (3, 1, 0), (3, 1, 1), (3, 1, 2), (3, 2, 0), (3, 2, 1), (3, 3, 0), (4, 0, 0), (4, 0, 1), (4, 0, 2), (4, 1, 0), (4, 1, 1), (4, 2, 0), (5, 0, 0), (5, 0, 1), (5, 1, 0), (6, 0, 0)]

# unknown_ans is for verification
def solve(N, unknown, known, unknown_ans=None, beta=0.4, m=8, t=2):
    assert len(unknown) > 0
    if len(unknown) > 5:
        print("Too many unknown variables!")
        print("This will be much slower")

    n = len(unknown)
    PR = PolynomialRing(Zmod(N), n, var_array=['x'])
    x = PR.objgens()[1]

    # Generate a function for unknown bits
    f = known
    for i in range(n):
        f += x[i] * 2^unknown[i][0]

    # Make function monic
    if 2^unknown[0][0] != 1:
        f = f / 2^unknown[0][0]
    
    f = f.change_ring(ZZ)
    x = f.parent().objgens()[1]

    if unknown_ans is not None:
        v = f(unknown_ans)
        if v != 0:
            g = gcd(N, v)
            print(g,N,v)
            # g must be non-trivial value (p)
            assert g != 1 and g != N

    # d is dimension, sN is sum from the paper
    d = binomial(m + n, m)
    # t = m * tau
    Xbits = beta * t * (d - n + 1)
    Xbits -= d * t
    Xbits += binomial(m + n, m - 1)
    Xbits -= binomial(m - t + n, m - t - 1)
    Xbits *= len(bin(N)[2:]) * (n + 1) / (m * d)

    print("Xbits =", Xbits)
    print("dim =", d)

    Ubits = sum(map(lambda x: x[1], unknown))
    #assert Ubits < Xbits, "Range is too big"

    X = [ 2^v[1] for v in unknown ]

    # Polynomial construction
    g = []
    monomials = []
    Xmul = []

    # g_k,i2,...,in = x2^i2 * x3^i3 * ... * xn^in * f^k * N^max{t-k, 0}
    # for ij in {0,...,m} and sum(ij) <= m - k
    # monomials : x1^k * x2^i2 * x3^i3 * ... * xn^in
    # Xmul : X1^k * X2^i2 * X3^i3 * ... * Xn^in

    #for ii in IIter(m, n):
    for ii in tttmp:
        k = ii[0]
        g_tmp = f^k * N^max(t-k, 0)
        monomial = x[0]^k
        Xmul_tmp = X[0]^k

        for j in range(1, n):
            g_tmp *= x[j]^ii[j]
            monomial *= x[j]^ii[j]
            Xmul_tmp *= X[j]^ii[j]
        
        g.append(g_tmp)
        monomials.append(monomial)
        Xmul.append(Xmul_tmp)

    B = Matrix(ZZ, len(g), len(g))
    for i in range(B.nrows()):
        for j in range(i + 1):
            if j == 0:
                B[i,j] = g[i].constant_coefficient()
            else:
                v = g[i].monomial_coefficient(monomials[j])
                B[i,j] = v * Xmul[j]

    # DO LLL!!!
    B = B.LLL()

    print("LLL finished")

    # Polynomial reconstruction
    h = []
    for i in range(B.nrows()):
        h_tmp = 0
        for j in range(B.ncols()):
            if j == 0:
                h_tmp += B[i, j]
            else:
                assert B[i,j] % Xmul[j] == 0
                v = ZZ(B[i,j] // Xmul[j])
                h_tmp += v * monomials[j]
        h.append(h_tmp)

    if unknown_ans is not None:
        assert h[0](unknown_ans) == 0, "Failed to construct polynomial"
        print(unknown_ans)

    # From https://arxiv.org/pdf/1208.399.pdf
    x_ = [ var('x{}'.format(i)) for i in range(n) ]
    for ii in Combinations(range(len(h)), k=n):
        # It would be nice if there's better way than this :(
        # To use jacobian, we need symbolic variables
        f = symbolic_expression([ h[i](x) for i in ii ]).function(x_)
        jac = jacobian(f, x_)
        v = vector([ t // 2 for t in X ])

        for _ in range(1000):
            kwargs = {'x{}'.format(i): v[i] for i in range(n)}
            tmp = v - jac(**kwargs).inverse() * f(**kwargs)
            # Precision is 150-bit now. If it's not enough, give bigger number
            v = vector((numerical_approx(d, prec=150) for d in tmp))

        v = [ int(_.round()) for _ in v ]
        if h[0](v) == 0:
            print("NICE", v)
            return v
        else:
            print("NO", i, j, v)


kbits = 35

N = 123850820426090063939750639461336535800888872303996740868393788108622197265459429269747101462736954752274429639803614452794471290719054376275608856319222801843407104278834963103014930163521479153822223511859077469170499658852892275556238914610902748238728617276564375256445353397161395711740355127024574224311
p0 = 10571149853133522431404264421866395513173821523643894835630672288391956736188404880335540994971314013670900609488503094055472955457681524945615744534010765

ans = solve(N, [(111, kbits),(111+146, kbits), (111+146*2, kbits)], p0, unknown_ans=None, m=6, t=1)

print ans