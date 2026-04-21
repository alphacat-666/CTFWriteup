description: I feel CHAINED to my desk, looking for some positive FEEDBACK.

The question is related to `XOR Encryption/Decryption`. Good thing is that both the key and algorithm for encryption and decryption are symmetric.

But we still need to figure out:

+ What is the key for XOR? A string or a single value?
+ What is the proper decryption content? The whole image or part of it?
+ What is the mode for `XOR Encryption/Decryption`?

At first, I thought the key is a string, which is also the flag of this question. And utilize `PNG` images' stable headers may help to recover the key.

```
0x89 0x50 0x4E 0x47 0x0D 0x0A 0x1A 0x0A
```

Soon I gave it up, because these stable headers' length is too short, `UDCTF{}` has occupied 7 positions already.

Maybe the key is a single value, but this value can be 0-255. Should I brute force all possible values in this range?

Then I noticed the picture name is `0x67`, maybe the right key. But if using this value to XOR all pixel values of this image one by one, we get nothing useful.

## XOR + CBC

I returned back to the hint itself, "CHAINED" and "FEEDBACK" suggests its mode should be `CBC mode`.

```python
from PIL import Image

IV = 0x67
ENCRYPTED_IMG_PATH = "0x67.png"
DECRYPTED_IMG_PATH = "result.png"

img = Image.open(ENCRYPTED_IMG_PATH).convert("RGB")
pixels = list(img.getdata())  
flat_pixels = []
for r, g, b in pixels:
    flat_pixels.extend([r, g, b]) 

decrypted_flat = []
prev_cipher = IV  
for cipher_val in flat_pixels:
    plain_val = cipher_val ^ prev_cipher
    decrypted_flat.append(plain_val)
    prev_cipher = cipher_val

decrypted_pixels = []
for i in range(0, len(decrypted_flat), 3):
    r = decrypted_flat[i]
    g = decrypted_flat[i+1]
    b = decrypted_flat[i+2]
    decrypted_pixels.append((r, g, b))

new_img = Image.new("RGB", img.size)
new_img.putdata(decrypted_pixels)
new_img.save(DECRYPTED_IMG_PATH)
```

![]()