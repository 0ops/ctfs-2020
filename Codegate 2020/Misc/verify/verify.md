得到flag需要print一个负数 

在执行前会判断每个数的范围，检测到可能打印负数就退出

While的范围判断有问题

```python
for i in range(3):
    tenv, _ = self.cond.a_interp(env)
    if tenv is not None:
        tenv = self.comm.a_interp(tenv)
    env = env_join(env, tenv)
tenv, _ = self.cond.a_interp(env)
if tenv is not None:
    tenv = self.comm.a_interp(tenv)
env = env_widen(env, tenv)
```

如果有可能，先进行三次执行，三次之后如果还有可能执行，则根据第四次的结果扩展变量范围。

可以在前四次循环时让变量不变化，从而使范围不扩展，在之后的循环中再将变量减为负值

即

```c
a=100;
b=1;
c=100;
while(c!=0)
{
    if(c>=97);
    else a=a-c;
    c--;
}
```

 a=100;b=1;c=100;[c!=0{c >= 97 ?{a = a}:{a = a - c};!a;c = c - 1}] 