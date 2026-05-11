This challenge does not provide any file, just provide a port service you can interact with.

There are several commands could be used: `add`, `and`, `mul`, `or`, `regs`, `sub`, `xor`, `win`, `EOF`.

The winning condition is to make one register reach `0x1337`.

But after some testing, the easiest way `add` or `sub` is not permitted to reach `0x1337`, which will return `bad result`.

So just use `or` and `xor` can solve this problem:

![](https://github.com/alphacat-666/CTFWriteup/blob/ae28d8e6900047e71f8b638a2308790b140d5a9d/Reverse/Smachine%20(Midnight%20Sun%20CTF%202026%20Quals)/img/2026-05-10%20211047.png)