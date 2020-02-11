from copy import deepcopy
from domain import Interval
from random import randint


loop_count = 0


def env_join(env1, env2):
    if env1 is None:
        return env2
    if env2 is None:
        return env1

    env = {}
    for var in (env1.keys() | env2.keys()):
        if var in env1:
            env[var] = env1[var]
        if var in env2:
            env[var] = env.setdefault(var, env2[var]) | env2[var]
    return env


def env_widen(env1, env2):
    if env1 is None:
        return env2
    if env2 is None:
        return env1

    env = {}
    for var in (env1.keys() | env2.keys()):
        if var in env1:
            env[var] = env1[var]
        if var in env2:
            env[var] = env.setdefault(var, env2[var]).widen(env2[var])
    return env


class Ast(object):
    pass


class Comm(Ast):
    pass


class Skip(Comm):
    def __init__(self):
        pass

    def a_interp(self, env):
        return env

    def interp(self, env):
        return env


class Assign(Comm):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def a_interp(self, env):
        env[self.var.name] = self.expr.a_interp(env)
        return env

    def interp(self, env):
        env[self.var.name] = self.expr.interp(env)
        return env


class Seq(Comm):
    def __init__(self, comm1, comm2):
        self.comm1 = comm1
        self.comm2 = comm2

    def a_interp(self, env):
        env = self.comm1.a_interp(env)
        env = self.comm2.a_interp(env)
        return env

    def interp(self, env):
        env = self.comm1.interp(env)
        env = self.comm2.interp(env)
        return env


class IfElse(Comm):
    def __init__(self, cond, comm1, comm2):
        self.cond = cond
        self.comm1 = comm1
        self.comm2 = comm2

    def a_interp(self, env):
        tenv, fenv = self.cond.a_interp(env)

        if tenv is not None:
            tenv = self.comm1.a_interp(tenv)
        if fenv is not None:
            fenv = self.comm2.a_interp(fenv)

        return env_join(tenv, fenv)

    def interp(self, env):
        cond = self.cond.interp(env)

        if cond:
            env = self.comm1.interp(env)
        else:
            env = self.comm2.interp(env)

        return env


class While(Comm):
    def __init__(self, cond, comm):
        self.cond = cond
        self.comm = comm

    def a_interp(self, env):
        init_env = deepcopy(env)

        for i in range(3):
            tenv, _ = self.cond.a_interp(env)
            if tenv is not None:
                tenv = self.comm.a_interp(tenv)
            env = env_join(env, tenv)

        tenv, _ = self.cond.a_interp(env)
        if tenv is not None:
            tenv = self.comm.a_interp(tenv)
        env = env_widen(env, tenv)

        tenv, _ = self.cond.a_interp(env)
        if tenv is not None:
            tenv = self.comm.a_interp(tenv)
        env = env_join(init_env, tenv)
        _, fenv = self.cond.a_interp(env)

        if fenv is None:
            raise RuntimeError("loop analysis error")

        return fenv

    def interp(self, env):
        global loop_count
        cond = self.cond.interp(env)

        while cond:
            env = self.comm.interp(env)
            cond = self.cond.interp(env)
            loop_count += 1
            if loop_count > 10000:
                raise RuntimeError("infinite loop error")
        loop_count = 0

        return env


class Print(Comm):
    def __init__(self, expr):
        self.expr = expr

    def a_interp(self, env):
        a_val = self.expr.a_interp(env)
        if a_val.infimum < 0:
            raise ValueError("print domain error")
        return env

    def interp(self, env):
        value = self.expr.interp(env)

        if value < 0:
            with open('./flag') as f:
                print(f.read())
        print(value)
        return env


class Cond(Ast):
    def __init__(self, var, num):
        self.var = var
        self.num = num

    def a_interp(self, env):
        tenv, fenv = None, None
        if self.var.name in env:
            tdomain, fdomain = self.filter(env[self.var.name])
            if tdomain is not None:
                tenv = deepcopy(env)
                tenv[self.var.name] = tdomain
            if fdomain is not None:
                fenv = deepcopy(env)
                fenv[self.var.name] = fdomain
            return tenv, fenv

        raise NameError("name '{}' is not defined".format(self.var.name))

    def interp(self, env):
        lvalue = self.var.interp(env)
        rvalue = self.num.interp(env)

        return self.func(lvalue, rvalue)


class Lt(Cond):
    opname = '<'

    def func(self, x, y):
        return x < y

    def filter(self, interval):
        t_infimum = interval.infimum
        t_supremum = min(interval.supremum, self.num.value - 1)
        t = Interval(t_infimum, t_supremum) if t_infimum <= t_supremum else None
        f_infimum = max(interval.infimum, self.num.value)
        f_supremum = interval.supremum
        f = Interval(f_infimum, f_supremum) if f_infimum <= f_supremum else None
        return t, f


class Le(Cond):
    opname = '<='

    def func(self, x, y):
        return x <= y

    def filter(self, interval):
        t_infimum = interval.infimum
        t_supremum = min(interval.supremum, self.num.value)
        t = Interval(t_infimum, t_supremum) if t_infimum <= t_supremum else None
        f_infimum = max(interval.infimum, self.num.value + 1)
        f_supremum = interval.supremum
        f = Interval(f_infimum, f_supremum) if f_infimum <= f_supremum else None
        return t, f


class Eq(Cond):
    opname = '=='

    def func(self, x, y):
        return x == y

    def filter(self, interval):
        t_infimum = max(interval.infimum, self.num.value)
        t_supremum = min(interval.supremum, self.num.value)
        t = Interval(t_infimum, t_supremum) if t_infimum <= t_supremum else None
        return t, interval


class Ne(Cond):
    opname = '!='

    def func(self, x, y):
        return x != y

    def filter(self, interval):
        f_infimum = max(interval.infimum, self.num.value)
        f_supremum = min(interval.supremum, self.num.value)
        f = Interval(f_infimum, f_supremum) if f_infimum <= f_supremum else None
        return interval, f


class Gt(Cond):
    opname = '>'

    def func(self, x, y):
        return x > y

    def filter(self, interval):
        t_infimum = max(interval.infimum, self.num.value + 1)
        t_supremum = interval.supremum
        t = Interval(t_infimum, t_supremum) if t_infimum <= t_supremum else None
        f_infimum = interval.infimum
        f_supremum = min(interval.supremum, self.num.value)
        f = Interval(f_infimum, f_supremum) if f_infimum <= f_supremum else None
        return t, f


class Ge(Cond):
    opname = '>='

    def func(self, x, y):
        return x >= y

    def filter(self, interval):
        t_infimum = max(interval.infimum, self.num.value)
        t_supremum = interval.supremum
        t = Interval(t_infimum, t_supremum) if t_infimum <= t_supremum else None
        f_infimum = interval.infimum
        f_supremum = min(interval.supremum, self.num.value - 1)
        f = Interval(f_infimum, f_supremum) if f_infimum <= f_supremum else None
        return t, f


class Expr(Ast):
    pass


class Num(Expr):
    def __init__(self, value):
        self.value = value

    def a_interp(self, env):
        return Interval(self.value, self.value)

    def interp(self, env):
        return self.value


class Random(Expr):
    def __init__(self, infimum, supremum):
        self.infimum = infimum
        self.supremum = supremum

    def a_interp(self, env):
        if self.infimum > self.supremum:
            raise ValueError("empty range for '{} ~ {}'".format(self.infimum, self.supremum))

        return Interval(self.infimum, self.supremum)

    def interp(self, env):
        if self.infimum > self.supremum:
            raise ValueError("empty range for '{} ~ {}'".format(self.infimum, self.supremum))

        return randint(self.infimum, self.supremum)


class Var(Expr):
    def __init__(self, name):
        self.name = name

    def a_interp(self, env):
        if self.name in env:
            return env[self.name]
        raise NameError("name '{}' is not defined".format(self.name))

    def interp(self, env):
        if self.name in env:
            return env[self.name]
        raise NameError("name '{}' is not defined".format(self.name))


class BinOp(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def a_interp(self, env):
        lvalue = self.left.a_interp(env)
        rvalue = self.right.a_interp(env)

        return self.func(lvalue, rvalue)

    def interp(self, env):
        lvalue = self.left.interp(env)
        rvalue = self.right.interp(env)

        return self.func(lvalue, rvalue)


class Add(BinOp):
    opname = '+'

    def func(self, x, y):
        return x + y


class Sub(BinOp):
    opname = '-'

    def func(self, x, y):
        return x - y


class Mul(BinOp):
    opname = '*'

    def func(self, x, y):
        return x * y
