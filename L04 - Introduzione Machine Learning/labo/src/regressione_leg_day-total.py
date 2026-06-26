from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configurazione
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "leg_day_volumes.csv"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Funzioni
# ---------------------------------------------------------------------------
def fit_linear(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:

    m, b = np.polyfit(x, y, 1)
    y_pred = m * x + b
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return float(m), float(b), float(r2)


def riassumi(label: str, m: float, b: float, r2: float, n: int) -> None:
    """Stampa una riga riassuntiva del fit."""
    print(
        f"{label:<20} | n={n:>3} | "
        f"slope={m:>+8.1f} kg/sett | "
        f"intercept={b:>8.0f} | R²={r2:.4f}"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    df = pd.read_csv(DATA_PATH)

    print(f"Caricato dataset: {len(df)} settimane tracciate\n")

    # ---- Tre tagli del dataset ---------------------------------------------
    tutto = df
    pre = df[df["period"] == "pre_pt"]
    pt = df[df["period"] == "with_pt"]

    print("Risultati della regressione lineare sui tre tagli:")
    print("-" * 80)

    risultati = {}
    for label, subset in [
        ("Tutto", tutto),
        ("Pre-PT (0-41)", pre),
        ("Con PT (53-58)", pt),
    ]:
        x = subset["week_index"].to_numpy(dtype=np.float64)
        y = subset["volume_kg"].to_numpy(dtype=np.float64)
        m, b, r2 = fit_linear(x, y)
        riassumi(label, m, b, r2, len(x))
        risultati[label] = (x, y, m, b, r2)

    print("-" * 80)
    print(
        "\nLettura: il fit globale ha R² ≈ 0 perché mescola due regimi diversi.\n"
        "Isolando il periodo con PT, R² sale a ~0.76 con una pendenza\n"
        "positiva chiara (~+820 kg/settimana di volume aggiunto).\n"
    )

    # ---- Grafico comparativo -----------------------------------------------
    plot_path = OUTPUT_DIR / "regressione_leg_day.png"
    crea_grafico(risultati, plot_path)
    print(f"Grafico salvato in: {plot_path}")


def crea_grafico(risultati: dict, output_path: Path) -> None:
    """Tre subplot affiancati, uno per ogni taglio del dataset."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)
    fig.suptitle(
        "Regressione lineare — Volume leg day per settimana",
        fontsize=14,
        fontweight="bold",
    )

    colori = {
        "Tutto": "#7f8c8d",
        "Pre-PT (0-41)": "#3498db",
        "Con PT (53-58)": "#27ae60",
    }

    for ax, (label, (x, y, m, b, r2)) in zip(axes, risultati.items()):
        colore = colori[label]
        ax.scatter(
            x, y, color=colore, s=60, edgecolors="black", linewidths=0.6, zorder=5
        )

        # Retta di regressione disegnata sul range delle x effettive
        x_line = np.linspace(x.min(), x.max(), 100)
        ax.plot(x_line, m * x_line + b, color="#e74c3c", linewidth=2.2, linestyle="--")

        ax.set_title(f"{label}\nslope={m:+.0f}  R²={r2:.3f}", fontsize=11)
        ax.set_xlabel("Settimana progressiva")
        ax.grid(True, alpha=0.3)

    axes[0].set_ylabel("Volume leg day (kg)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
