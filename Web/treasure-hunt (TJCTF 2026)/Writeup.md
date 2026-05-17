description: Let's go hunt down some treasure! The flag is split into 4 parts. I'll give you the first one right here: tjctf

We need to find three parts of flag hidden in the website.

This is the website page, very clean with a learn more button. Click the button, we get into another very clean page with a penguin image.

![2026-05-17 211826](https://github.com/alphacat-666/CTFWriteup/blob/6c028c677b356fc0ea431d47bb44eb12ebeaf44a/Web/treasure-hunt%20(TJCTF%202026)/img/2026-05-17%20211826.png)

![](https://github.com/alphacat-666/CTFWriteup/blob/6c028c677b356fc0ea431d47bb44eb12ebeaf44a/Web/treasure-hunt%20(TJCTF%202026)/img/2026-05-17%20212257.png)

## FLAG PART 1

Check the first page source code, we can see a hidden `<p>`. 

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/styles.css">
    <title>Pirates!</title>
</head>

<body>
    <h1>Learn about pirates!</h1>
    <h2>Wow!</h2>
    <form method="POST">
        <input type="submit" value="Learn More">
    </form>
    <img src="/static/ship.png" alt="ship">
    <p hidden>_and_</p>
</body>
</html>
```

Then, also check the second page source code, including `html`, `css`, `js` file, nothing useful.

Because there is a penguin in the page, try to visit `/penguin`, also try to use dot to divide `penguin`, nothing useful.

```python
import requests
from requests.exceptions import RequestException

base_url = "http://treasure-hunt.tjc.tf"
word = "penguin"

urls = []
for i in range(1, len(word) + 1):
    part1 = word[:i]
    part2 = word[i:]
    url = f"{base_url}{part1}.{part2}"
    urls.append(url)
for url in urls:
    print(f"Visiting: {url}")
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        print(f"status_code: {resp.status_code}, resp_len: {len(resp.text)}")
    except RequestException as e:
        print(e)
```

## FLAG PART 2

Check the cookie. 

![](https://github.com/alphacat-666/CTFWriteup/blob/6c028c677b356fc0ea431d47bb44eb12ebeaf44a/Web/treasure-hunt%20(TJCTF%202026)/img/2026-05-15%20231730.png)

## FLAG PART 3

Check `/robots.txt`. Obviously, `not allowed` means something inside.

![](https://github.com/alphacat-666/CTFWriteup/blob/6c028c677b356fc0ea431d47bb44eb12ebeaf44a/Web/treasure-hunt%20(TJCTF%202026)/img/2026-05-15%20230742%20(1).png)

![](https://github.com/alphacat-666/CTFWriteup/blob/6c028c677b356fc0ea431d47bb44eb12ebeaf44a/Web/treasure-hunt%20(TJCTF%202026)/img/2026-05-15%20230742%20(2).png)

`tjctf{{s1lv3r_and_g0ld}`