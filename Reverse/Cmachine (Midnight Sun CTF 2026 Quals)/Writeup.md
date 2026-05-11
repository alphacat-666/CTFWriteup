This is another black box, which contains more commands.

Except for `and`, `or`, `sub`, `add`, `mul`, `xor`, it also has `load`, `store`, `mem`, `readstr`, `login`, `call`.

If using `login` command, it needs to provide valid password.

And `readstr` has restriction of the writing boundary of memory space.

Then I also find that when using `login`, it will write the input password into memory space, which can cause buffer overflow problem, since it does not have restriction of boundary.

![](C:\Users\14489\Desktop\CTFWriteup&Notes\CTFWriteup\Reverse\Cmachine (Midnight Sun CTF 2026 Quals)\img\2026-05-11 232139.png)

But then I am stuck. My thought is that I only can get the flag after successful login, then I need to make the validation become `True`, even if I input the wrong password.

How could I know where I should modify to bypass...

Okay, after competition, I read writeup from z68d: [cmashine | saad Writeups](https://z68d.github.io/midnight-sun-ctf-2026-quals/ch/cmashine/index.html).

It shows that we don't really need to login successfully, but just replace the function name of `echo` with `flag`. Then `call flag`.