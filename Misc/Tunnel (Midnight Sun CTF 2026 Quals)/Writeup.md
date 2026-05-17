description: 01101001 00100000 01101000 01100101 01100001 01110010 01110100 00100000 01100010 01101001 01101110 01100001 01110010 01111001

Transform binary description into ASCII: `i heart binary`.

The website keep showing two choices, and only one of both is correct.

Wrong choice shows: 'Nope', while correct one leads to another binary choice endlessly...

![](https://github.com/alphacat-666/CTFWriteup/blob/20bdef0781a7a6c74550b2ad89f1ef0cc324b789/Misc/Tunnel%20(Midnight%20Sun%20CTF%202026%20Quals)/img/2026-05-10%20201516.png)

When I clicked on the choice button, I also noticed that the URL parameter `path` is changing, such as `?path=z6qpcm5thexk`.

The first thought is directly brute force the strings, but the length of this path value seems to be generated randomly, sometimes it is short, sometimes it is long. Probably it does not work.

In order to make the choosing operation perform automatically, we can capture the network packet, randomly choose one of both. If it is wrong, then back to choose another one; it is correct, then keep choosing until page shows something related to the flag format, such as `midnight`.

```python
import requests
import re
import time

BASE_URL = "http://tunnel.play.ctf.se:22560/"
FAIL_WORD = "nope"
SUCCESS_WORD = "midnight"
DELAY = 0.3

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def get_page(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=5)
        return resp.text
    except:
        return ""
def parse_two_paths(html):
    paths = re.findall(r"path=([a-zA-Z0-9]+)", html)
    if len(paths) >= 2:
        return paths[0], paths[1]
        
if __name__ == "__main__":
    current_html = get_page(BASE_URL)
    while True:
        opt1, opt2 = parse_two_paths(current_html)
        print(f"Current option: {opt1} | {opt2}")
        url1 = BASE_URL + "?path=" + opt1
        print(f"visit {url1}")
        res1 = get_page(url1)
        if SUCCESS_WORD in res1:
            print(res1)
            break
        if FAIL_WORD in res1.lower():
            print("Option 1 is wrong, change to option 2.")
            url2 = BASE_URL + "?path=" + opt2
            print(f"visit {url2}")
            res2 = get_page(url2)
            if SUCCESS_WORD in res2:
                print(res2)
                break
            current_html = res2
        else:
            current_html = res1
        time.sleep(DELAY)
        print("-"*40)
```

```html
<strong>flag:</strong> <span>midnight{sh0uLD_h4v3_s3T_rob07s.txt}</span>
```

