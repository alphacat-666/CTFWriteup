description: Unfortunately, our insider trading anonymous tip line has been spammed by people who preferred last year's theme. As a result, our encrypted line now checks to make sure you are of sound mind.

I did not solve this challenge, but thanks to Z4faran's detailed writeup ([no-brainrot-allowed | UMDCTF | Crypto | by Z4faran | Apr, 2026 | Medium](https://medium.com/@mazenmagdy1598/no-brainrot-allowed-umdctf-crypto-0c38205cbc26)). It is very helpful!

During the competition, I know I can utilize Multiplicative Homomorphism, which I learned from Cryptography class. But I don't know how to narrow the scope properly and make it run as fast as possible.

Below is my personal understanding of Z4faran's idea, and also the record of his script. 

![](https://github.com/alphacat-666/CTFWriteup/blob/a7dca5f483c9b1efd057970d12982008385e156a/Cryptography/no-brainrot-allowed%20(UMD%20CTF%202026)/img/Inkodo-2026510_103309.png)

```python
#!/usr/bin/env python3
import socket
import sys

HOST = "challs.umdctf.io"
PORT = 32767

n = 89496838321330017124211425752928111009238414395285545597372895783391482460166014550795440784240669454038164776392492949832230406030665778241454645944939829559549747525412818621247626093163657213524408194055221128159991890855776297338418179985226639927931716465641085590302394062423554511419578835789906477703
e = 65537
ct = 7754782549233547741892262011884269269634473224225227064848605234096464292342695844400918832869742989785685496372442722948589824059885664742180188925993430350247652395812127146595142859972102395302095473677093880196683037670451512853001503582104512714892761518926915267957380484576367984853786495267989619184

# "0x67..." bucket
A = 103 * 16**254
B = 104 * 16**254

# Fixed from the successful run:
# true flag length = 111 bytes, prefix = b"UMDCTF{"
PREFIX = b"UMDCTF{"
FLAG_LEN = 111

ALPHA = 16
NUM_SAMPLES = 32
DENSE_SAMPLES = 48
MAX_BATCHES = 220


def recv_until_prompt(sock: socket.socket) -> str:
    data = b""
    while b"Your messages:" not in data:
        chunk = sock.recv(65536)
        if not chunk:
            raise EOFError("server closed connection")
        data += chunk
    return data.decode(errors="replace")


def connect() -> socket.socket:
    sock = socket.create_connection((HOST, PORT), timeout=10)
    sock.settimeout(30)
    recv_until_prompt(sock)
    return sock


def query_batch(sock: socket.socket, s_values: list[int]) -> list[int]:
    payload_cts = [str((ct * pow(s, e, n)) % n) for s in s_values]
    sock.sendall((",".join(payload_cts) + "\n").encode())

    text = recv_until_prompt(sock)
    responses = []
    for line in text.splitlines():
        if "ERROR: BRAINROT DETECTED" in line:
            responses.append(True)
        elif "thanks you for your message" in line:
            responses.append(False)

    return [s for s, ok in zip(s_values, responses) if ok]


def to_bytes(x: int) -> bytes:
    hx = hex(x)[2:]
    if len(hx) % 2:
        hx = "0" + hx
    return bytes.fromhex(hx)


def main():
    prefix_int = int.from_bytes(PREFIX, "big")
    L = prefix_int * 256 ** (FLAG_LEN - len(PREFIX))
    U = (prefix_int + 1) * 256 ** (FLAG_LEN - len(PREFIX))

    sock = connect()

    for batch in range(1, MAX_BATCHES + 1):
        width = U - L
        if width <= 1:
            break

        mid = (L + U) // 2
        s_target = ALPHA * 16**254 // width
        k = round(s_target * mid / n)

        s_lo = (k * n + A + U - 1) // U
        s_hi = (k * n + B - 1) // L
        if s_hi < s_lo:
            raise RuntimeError(f"empty s-interval at batch {batch}")

        total = s_hi - s_lo
        s_values = [s_lo + (total * i) // (NUM_SAMPLES - 1) for i in range(NUM_SAMPLES)]

        try:
            hits = query_batch(sock, s_values)
        except Exception:
            try:
                sock.close()
            except Exception:
                pass
            sock = connect()
            hits = query_batch(sock, s_values)

        if not hits:
            s_values = [s_lo + (total * i) // (DENSE_SAMPLES - 1) for i in range(DENSE_SAMPLES)]
            try:
                hits = query_batch(sock, s_values)
            except Exception:
                try:
                    sock.close()
                except Exception:
                    pass
                sock = connect()
                hits = query_batch(sock, s_values)

        if not hits:
            raise RuntimeError(f"no positive hits at batch {batch}")

        # Reuse every positive hit from the same batch, exactly like the successful run
        for s in hits:
            k = (s * L) // n
            new_L = max(L, (k * n + A + s - 1) // s)
            new_U = min(U, (k * n + B - 1) // s + 1)
            if not (new_L < new_U):
                raise RuntimeError("interval collapsed")
            L, U = new_L, new_U

        if batch == 1 or batch % 5 == 0:
            print(f"[+] batch={batch:3d} hits={len(hits)} bits={(U - L).bit_length()}")

    try:
        sock.close()
    except Exception:
        pass

    print(f"[+] final width = {U - L}")
    print(f"[+] final bits  = {(U - L).bit_length()}")

    for m in range(L, U):
        if pow(m, e, n) == ct:
            flag = to_bytes(m)
            print(f"[+] FLAG = {flag.decode()}")
            return

    print("[-] flag not found in final interval")
    sys.exit(1)


if __name__ == "__main__":
    main()
```

