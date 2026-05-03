Description: I was scrolling through my email and saw a message from FurryHater_2009) asking to decrypt some strange message, and he also attached two files. Flag format: KubSTU()

P.S. `Weird_Furry_text.txt` should be 1GB large with many random characters like the following format. But I don't want to upload 1GB file, so it is empty.

![](C:\Users\14489\Desktop\CTFWriteup&Notes\CTFWriteup\Cryptography\Furry Cipher (KubSTU CTF 2026)\img\屏幕截图 2026-05-02 224439.png)

We go back to the script, this logic is really simple:

+ use key = [n1, n2, n3] to encrypt the plaintext

+ encryption: substitute alphabet(`A-Za-z0-9`) with alphabet, don't change other characters(especially `()_`). and also we know n1, n2, n3 are all integer in [0, 61], because of mod operation.
+ ciphertext is `Weird_Furry_text.txt`, flag must be hidden inside plaintext.

```python
import string

def encrypt_custom(plaintext, key_values):
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
    char_map = {ch: i for i, ch in enumerate(alphabet)}
    num_map = {i: ch for i, ch in enumerate(alphabet)}

    result = []
# substitute alphabet(A-Za-z0-9) with alphabet, don't change other characters(especially ()_)
    for i, char in enumerate(plaintext):
        if char in '()_':
            result.append(char)
        elif char in char_map:
            num = char_map[char]
            key_val = key_values[i % 3]

            if i % 3 == 0:
                encrypted = (num * 13 + key_val * 7) % 62
            elif i % 3 == 1:
                encrypted = (num * 17 + key_val * 3 + 11) % 62
            else:
                encrypted = (num * 19 + (key_val ^ 42) + 23) % 62

            result.append(num_map[encrypted])
        else:
            result.append(char)

    return ''.join(result)

if __name__ == "__main__":
    example_text = "Test123"
# key = [n1, n2, n3] unknown
# from encryption, mod 62, so n1, n2, n3 range [0, 61]
    example_key = [1, 2, 3]
    encrypted_example = encrypt_custom(example_text, example_key)
    print(f"'{example_text}' -> '{encrypted_example}'")
```

Trying 62×62×62=238,328 possibilities of key combination is possible, but we face two problems: **how can we know decryption is successful? (indicator)** and **how can we decrypt this 1GB text?**

My thought is to firstly extract part of the useful text which could contain flag, then we only analyze or decrypt the smaller text with key trials.

## Extract

I read that description mentioned about email thing, I tried to filter out 100 characters around `@` (because this character is not encrypted and must appear in email address), but got nothing useful. 

Maybe email address does not appear inside...

The flag contains `A-Za-z0-9_()` for sure, so just try to extract them.

```python
import string
import re

def extract_all_chars(large_file_path, output_file="all_chars.txt"):
    print(f"Start to extract all a-z A-Z 0-9 characters...")
    with open(large_file_path, 'r', encoding='utf-8', errors='ignore') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        total_chars = 0
        for line in f_in:
            chars = re.findall(r'[a-zA-Z0-9()_]', line)
            total_chars += len(chars)
            f_out.write(''.join(chars))
    print(f"Extract completed! Extract {total_chars} characters, save to {output_file}")
    return output_file

if __name__ == "__main__":
    char_file = extract_all_chars("./Weird_Furry_text.txt")
```

After running the script, we got a `all_chars.txt` with `XiEDJ5(9tV_qY3_v43_t9B3_o9vo_ESM_YR_YA_t_S5t8v_XYL4jt)`.

## Decrypt

Obviously, the first fix characters are encrypted from `KubSTF`. We can use this to reverse the key = [n1, n2, n3]. Then write decryption function (reverse of encryption) to decrypt the above string.

```python
import string
alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
char_map = {ch: i for i, ch in enumerate(alphabet)}
num_map = {i: ch for i, ch in enumerate(alphabet)}
def decrypt_custom(ciphertext, key_values):
    result = []
    inv13 = pow(13, -1, 62)
    inv17 = pow(17, -1, 62)
    inv19 = pow(19, -1, 62)
    for i, char in enumerate(ciphertext):
        if char in '()_':
            result.append(char)
        elif char in char_map:
            num = char_map[char]
            key_val = key_values[i % 3]
            if i % 3 == 0:
                decrypted = (num - 7 * key_val) * inv13 % 62
            elif i % 3 == 1:
                decrypted = (num - 3 * key_val - 11) * inv17 % 62
            else:
                decrypted = (num - (key_val ^ 42) - 23) * inv19 % 62 
            result.append(num_map[decrypted])
        else:
            result.append(char)
    return ''.join(result)

def get_key():
    key = []
    inv7 = pow(7, -1, 62)
    inv3 = pow(3, -1, 62)
    # K -> X, calculate n1
    n1 = inv7 * (char_map['X'] - char_map['K'] * 13) % 62
    # u -> i, calculate n2
    n2 = inv3 * (char_map['i'] - char_map['u'] * 17 - 11) % 62
    # b -> E, calculate n3
    n3 = (char_map['E'] - char_map['b'] * 19 - 23) ^ 42 % 62
    key.append(n1)
    key.append(n2)
    key.append(n3)
    return key

ciphertext = 'XiEDJ5(9tV_qY3_v43_t9B3_o9vo_ESM_YR_YA_t_S5t8v_XYL4jt)'
key = get_key()
decrypt_custom(ciphertext, key)
```

`KubSTU(h0w_d1d_you_re4d_7ha7_br0_1t_1s_a_furry_c1pher)`
