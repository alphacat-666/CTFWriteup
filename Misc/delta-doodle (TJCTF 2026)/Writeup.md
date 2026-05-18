description: i was calibrating the new AR airbrush for our maker faire booth by doodling the flag in midair. the headset, unfortunately, only logged the raw data. can you accumulate the motion trail and figure out what message we were trying to spray-paint?

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("trackpad_deltas.csv")
df["x"] = df["dx"].cumsum()
df["y"] = df["dy"].cumsum()

segments = []
current_segment = []

for idx, row in df.iterrows():
    if row["pen_down"] == 1:
        current_segment.append((row["x"], row["y"]))
    else:
        segments.append(current_segment)
        current_segment = []
if current_segment:
    segments.append(current_segment)

plt.figure()
for seg in segments:
    seg_x = [x[0] for x in seg]
    seg_y = [y[1] for y in seg]
    plt.plot(seg_x, seg_y)
plt.axis("equal")  
plt.show()
```

![](https://github.com/alphacat-666/CTFWriteup/blob/50e7e83bbf9b2a496f14999d62de2d589830d9bc/Misc/delta-doodle%20(TJCTF%202026)/img/2026-05-18%20115308.png)
