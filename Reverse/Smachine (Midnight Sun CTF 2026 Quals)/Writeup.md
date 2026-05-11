This challenge does not provide any file, just provide a port service you can interact with.

There are several commands could be used: `add`, `and`, `mul`, `or`, `regs`, `sub`, `xor`, `win`, `EOF`.

The winning condition is to make one register reach `0x1337`.

But after some testing, the easiest way `add` or `sub` is not permitted to reach `0x1337`, which will return `bad result`.

So just use `or` and `xor` can solve this problem:

![](C:\Users\14489\Desktop\CTFWriteup&Notes\CTFWriteup\Reverse\Smachine (Midnight Sun CTF 2026 Quals)\img\2026-05-10 211047.png)