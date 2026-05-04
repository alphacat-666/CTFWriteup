description: Hey, I just can't remember the name of the algorithm, but it's something very similar to Nintendo 3DS. Help me figure out what was written there^^

After recovering and combining the three strings, we got a 24-bytes key: `N1nt3ndoS3cur1tyK3y!2026`.

```python
# 1 = TjFudDNuZG8=
# 2 = 83 51 99 117 114 49 116 121
# 3 = 4b33792132303236

import base64
key1 = base64.b64decode("TjFudDNuZG8=")
key2 = bytes([83, 51, 99, 117, 114, 49, 116, 121])
key3 = bytes.fromhex("4b33792132303236")
print(key1 + key2 + key3, len(key1 + key2 + key3))
```

As for two iv, I have no ideas how to deal with them now. What we know is that they are both 8 bytes, and one is plaintext already.

Then we need to think about the algorithm. Since it does not give us the script of algorithm, we deduce the algorithm itself is widely used. Common algorithm that has `CBC+PKCS5`:

| Algorithm | Block Size/IV Size | Key Size        |
| --------- | ------------------ | --------------- |
| AES       | 16/24/32           | 16/24/32        |
| DES       | 8                  | 8               |
| 3DES      | 8                  | 8\*2=16/8\*3=24 |

It seems to be 3DES, but now we have two IVs. So here I tried to decrypt with two IVs.

```python
import base64
from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad

key1 = base64.b64decode("TjFudDNuZG8=")
key2 = bytes([83, 51, 99, 117, 114, 49, 116, 121])
key3 = bytes.fromhex("4b33792132303236")
key = key1 + key2 + key3

ivx = bytes.fromhex("0a001f0273760054")
ivm = b"M4r10Br0"
ciphertext = "072a8e75459a545679f3aa56a9fafb38871022de0c9bd5d7ef55e8dad7861662eb0fb630d9cdf9dd8c64a3a8ac28b86a"
ciphertext = bytes.fromhex(ciphertext)

plaintext1 = unpad(DES3.new(key, DES3.MODE_CBC, ivx).decrypt(ciphertext), DES3.block_size)
plaintext2 = unpad(DES3.new(key, DES3.MODE_CBC, ivm).decrypt(ciphertext), DES3.block_size)

print(plaintext1.decode('utf-8'), plaintext2.decode('utf-8'))
```

We got two results: 

```
?A?bd? ?d3s_n1nt3nd0_cbc_m0d3_n07_h4rd_3n0ugh}
Au}Q'#{gd3s_n1nt3nd0_cbc_m0d3_n07_h4rd_3n0ugh}
```

Our iv is wrong. For decryption, iv only influences the first block of content, since it is CBC mode.

But we have already know the first 7 bytes are flag format `KubSTU{`, then from the content, it is easy to guess the complete flag is `KubSTU{3d3s_n1nt3nd0_cbc_m0d3_n07_h4rd_3n0ugh}}`.

OK. I still need to know what is the right iv. `ivx` XOR `ivm`= `G4m3C4rd`.

```python
ivx = bytes.fromhex("0a001f0273760054")
ivm = b"M4r10Br0"
iv = bytes(iv1 ^ iv2 for iv1, iv2 in zip(ivx, ivm, len(ivx)))
```

