description: Listen, this is a strange archive, and the name is weird too?? Deal with this as soon as you can, please. 

I did not solve this one, but I tried during the process.

Thanks to Abdelkader Belcaid's detailed writeup ([KubSTU CTF 2026 Writeups: Five Challenges, Saturday | by Abdelkader Belcaid | May, 2026 | InfoSec Write-ups](https://infosecwriteups.com/kubstu-ctf-2026-writeups-five-challenges-saturday-43d7f2bec403)), I finally know the right solution. And here I only summarize my failed trials and some personal understanding.

There are some single-character directories, and each directory contains some pictures with different 16-bit hex value as names. Also, we get a cipher text.

My idea is to establish a mapping between hex names and corresponding single character, such as N -> `0e9af0ca9979c56a`. Then, we just need to segment the cipher text and search from this mapping relation.

But I failed, because the picture names did not appear in the cipher text. I also tried CRC64, which can also output 16-bit hex values. No result.

Then I tried to compare the images, is it possible to use specific look of the cat girl images? The combinations of cat girls' appearance seem to be very random. No result.

## SHA-256

Actually my first part of thought about establishing a mapping and searching strings is correct. Another half should be use image data as the input of SHA256, then search the mapping of the 64-bit hex value and single-character. Why it is SHA-256? It has hints.

One is from the directory name `64_what_could_this_mean`, telling us to segment the ciphertext into several 64-bit blocks.

Another is that commonly used hash function which can output fixed 64-bit hex values is SHA-256, SHA3-256.

```python
import hashlib
import os

FOLDER = "./64_what_could_this_mean"

hash_map = {}
flag = ""
for char_folder in os.listdir(FOLDER):
    folder_path = os.path.join(FOLDER, char_folder)
    if not os.path.isdir(folder_path):
        continue
    for jpg in os.listdir(folder_path):
        jpg_path = os.path.join(folder_path, jpg)
        with open(jpg_path, "rb") as f:
            jpg_data = f.read()
        jpg_hash = hashlib.sha256(jpg_data).hexdigest()
        hash_map[jpg_hash] = char_folder
print(f"Adding {len(hash_map)} records.")
with open("./64_what_could_this_mean/what_could_this_mean.txt", "rb") as f:
    ciphertext = f.read().decode('utf-8').strip()
for i in range(0, len(ciphertext), 64):
    chunk = ciphertext[i:i+64]
    flag += hash_map[chunk]
print(flag)
```

`KUBSTU{A7_LE4ST_N0W_Y0U_H4V3_A_BUNCH_0F_P1CTUR3S_OF_C4T_GIRL5}`

 

