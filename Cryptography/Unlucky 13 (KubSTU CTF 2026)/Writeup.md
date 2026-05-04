description: 13 is an unlucky number. Three layers of encryption, thirteen reasons not to try to decrypt this. Something leaked — hopefully it will help you.

Firstly, I read the script and found that the encryption has three layers:

+ Layer 1: flag ^ pseudo random bytes => layer1
+ Layer 2: RC4(key, layer1) => layer2
+ Layer 3: RSA(layer2, e, n) => c

```python
import hashlib
FLAG = open("flag.txt", "rb").read().strip()
def cursed_prng(seed, length):
    state = seed
    stream = []
    for _ in range(length):
        state = (state * 1313 + 131313) % (2**32)
        stream.append(state & 0xFF)
    return bytes(stream)

UNLUCKY_NUMBER = 13

# layer1: FLAG ^ pseudo-random bytes
layer1 = bytes(a ^ b for a, b in zip(
    FLAG,
    cursed_prng(UNLUCKY_NUMBER, len(FLAG))
))

# RC4
def forgotten_cipher(key, data):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    out = []
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(byte ^ S[(S[i] + S[j]) % 256])
    return bytes(out)

secret = b"Unlucky" + str(UNLUCKY_NUMBER).encode()
fc_key = hashlib.sha256(secret).digest()[:16]

# layer2: RC4(key2, layer1)
# key2 = SHA-256(b'Unlucky13')[0-15]
layer2 = forgotten_cipher(fc_key, layer1)


# layer3: RSA(layer2 ** e mod n)
n = 13658633037131788032351618427072247476717954542396408633560773884364554559070511401338131167308785959562652843354491812218130569318378376258845006015571936307529619165627684367938035500689095197148634390329808425228615805061358885887601807910577877331466810636357076781023936730357996997258012513541846157478488478454563307821991031194437503266795021183758263745762989760240683361817082008819321416765453826690538816962208131444601183340450621147225799934380535423737829891317625290259915071423282523846993193854126576514135696151799274710837198613476445017109884172011540789567531049972285279517155764888481047450059
e = 3

m = int.from_bytes(layer2, "big")
c = pow(m, e, n)

with open("output.txt", "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"e = {e}\n")
    f.write(f"c = {c}\n")
```

Like peeling the onions, we can decrypt one by one, since they are not hard to reverse.

## Layer 3: RSA (small e)

e = 3, very small integer, so we can calculate the cube root of `c` to get `m`.

But c is too large, we can not use the function in library. Instead, we use binary search to get the cube root.

``` python
def cal_cube_root(x):
    low = 0
    high = x
    while low <= high:
        mid = (low + high) // 2
        mid_cube = mid ** 3
        if mid_cube == x:
            return mid
        elif mid_cube < x:
            low = mid + 1
        else:
            high = mid - 1

if __name__ == '__main__':
    with open("output.txt", "r", encoding="utf-8") as f:
        rsa = {}
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if "=" in line:
                k, v = line.split("=", 1)
                rsa[k.strip()] = int(v.strip())
        m = cal_cube_root(rsa['c'])
```

## Layer 2: RC4 

RC4 is a stream cipher, using the same function for both encryption and decryption:

+ S-box initialization (Key Scheduling Algorithm): S[0...255] with values from 0 to 255, shuffle the order of it with the given key.
+ Encryption/Decryption: continuously swap S, extract one byte of key stream k each round, and XOR the plaintext/ciphertext.

$$
plaintext \oplus keystream=ciphertext\\
ciphertext \oplus keystream=plaintext
$$

```python
import hashlib
def forgotten_cipher(key, data):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    out = []
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(byte ^ S[(S[i] + S[j]) % 256])
    return bytes(out)
    
if __name__ == '__main__':
        layer2 = m.to_bytes((m.bit_length() + 7) // 8,"big")
        UNLUCKY_NUMBER = 13
        secret = b"Unlucky" + str(UNLUCKY_NUMBER).encode()
        fc_key = hashlib.sha256(secret).digest()[:16]
        layer1 = forgotten_cipher(fc_key, layer2)
```

## Layer 1: Pseudo Random Bytes 

```python
def cursed_prng(seed, length):
    state = seed
    stream = []
    for _ in range(length):
        state = (state * 1313 + 131313) % (2**32)
        stream.append(state & 0xFF)
    return bytes(stream)

if __name__ == '__main__':
        plaintext = bytes(a ^ b for a, b in zip(layer1, cursed_prng(UNLUCKY_NUMBER, len(layer1))))
```

So our complete code is like this:

```python
import hashlib
def cal_cube_root(x):
    low = 0
    high = x
    while low <= high:
        mid = (low + high) // 2
        mid_cube = mid ** 3
        if mid_cube == x:
            return mid
        elif mid_cube < x:
            low = mid + 1
        else:
            high = mid - 1
def forgotten_cipher(key, data):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    out = []
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(byte ^ S[(S[i] + S[j]) % 256])
    return bytes(out)
def cursed_prng(seed, length):
    state = seed
    stream = []
    for _ in range(length):
        state = (state * 1313 + 131313) % (2**32)
        stream.append(state & 0xFF)
    return bytes(stream)

if __name__ == '__main__':
    with open("output.txt", "r", encoding="utf-8") as f:
        rsa = {}
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if "=" in line:
                k, v = line.split("=", 1)
                rsa[k.strip()] = int(v.strip())
        m = cal_cube_root(rsa['c'])

        layer2 = m.to_bytes((m.bit_length() + 7) // 8,"big")
        UNLUCKY_NUMBER = 13
        secret = b"Unlucky" + str(UNLUCKY_NUMBER).encode()
        fc_key = hashlib.sha256(secret).digest()[:16]
        layer1 = forgotten_cipher(fc_key, layer2)
        plaintext = bytes(a ^ b for a, b in zip(layer1, cursed_prng(UNLUCKY_NUMBER, len(layer1))))
        print(plaintext)
```

`KubSTU{unLucky_13_l4y3r5_0f_encrypt10n_n0_luck_h3r3}`

Though the whole encryption procedure has three layers, every layer can be reversed easily.