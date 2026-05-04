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

layer1 = bytes(a ^ b for a, b in zip(
    FLAG,
    cursed_prng(UNLUCKY_NUMBER, len(FLAG))
))


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

layer2 = forgotten_cipher(fc_key, layer1)



n = 13658633037131788032351618427072247476717954542396408633560773884364554559070511401338131167308785959562652843354491812218130569318378376258845006015571936307529619165627684367938035500689095197148634390329808425228615805061358885887601807910577877331466810636357076781023936730357996997258012513541846157478488478454563307821991031194437503266795021183758263745762989760240683361817082008819321416765453826690538816962208131444601183340450621147225799934380535423737829891317625290259915071423282523846993193854126576514135696151799274710837198613476445017109884172011540789567531049972285279517155764888481047450059
e = 3

m = int.from_bytes(layer2, "big")
c = pow(m, e, n)


with open("output.txt", "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"e = {e}\n")
    f.write(f"c = {c}\n")
