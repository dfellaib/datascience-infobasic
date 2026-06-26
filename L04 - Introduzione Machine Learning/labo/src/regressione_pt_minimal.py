from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CSV = Path(__file__).resolve().parent.parent / "data" / "leg_day_volumes.csv"

df = pd.read_csv(CSV)
df = df[df["period"] == "with_pt"]

x = df["week_index"].to_numpy(dtype=np.float64)
y = df["volume_kg"].to_numpy(dtype=np.float64)

m, b = np.polyfit(x, y, 1)
r2 = 1 - np.sum((y - (m * x + b)) ** 2) / np.sum((y - y.mean()) ** 2)

x_line = np.linspace(x.min(), x.max(), 100)

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(x, y, color="#27ae60", s=80, edgecolors="black", linewidths=0.7, zorder=5)
ax.plot(x_line, m * x_line + b, color="#e74c3c", linewidth=2.2, linestyle="--")
ax.set_title(
    f"Volume leg day — periodo con PT (sett. 53–58)\nslope = {m:+.0f} kg/sett   R² = {r2:.3f}",
    fontsize=12,
    fontweight="bold",
)
ax.set_xlabel("Settimana progressiva")
ax.set_ylabel("Volume leg day (kg)")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
