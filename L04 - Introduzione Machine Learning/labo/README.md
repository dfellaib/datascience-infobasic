# Regressione lineare sul leg day

Mini-progetto didattico che applica la regressione lineare a un dataset reale di
volumi di allenamento (leg day) raccolti su Supabase tra marzo 2025 e marzo 2026.

L'obiettivo è mostrare un caso pratico in cui la **segmentazione del dataset**
cambia radicalmente la qualità del fit: lo stesso modello passa da R² ≈ 0 (sul
dataset completo) a R² ≈ 0.76 (sul solo periodo strutturato con personal trainer).

## Struttura

```
leg-day-regression/
├── data/
│   └── leg_day_volumes.csv       # 40 settimane: week_index, period, volume_kg, n_sessions
├── src/
│   ├── regressione_leg_day.py    # script eseguibile
│   └── regressione_leg_day.ipynb # notebook companion
├── output/                       # generato dallo script (grafico PNG)
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Esecuzione

**Script:**
```bash
python src/regressione_leg_day.py
```

Output atteso:
```
Caricato dataset: 40 settimane tracciate

Risultati della regressione lineare sui tre tagli:
--------------------------------------------------------------------------------
Tutto                | n= 40 | slope=    -23.5 kg/sett | intercept=   11558 | R²=0.0151
Pre-PT (0-41)        | n= 34 | slope=    +23.0 kg/sett | intercept=   10833 | R²=0.0073
Con PT (53-58)       | n=  6 | slope=   +820.3 kg/sett | intercept=  -36514 | R²=0.7584
--------------------------------------------------------------------------------
```

**Notebook:**
```bash
jupyter notebook src/regressione_leg_day.ipynb
```

## Cosa fa lo script, passo passo

1. **Carica** il CSV in un `DataFrame` pandas.
2. **Suddivide** il dataset in tre tagli: globale, pre-PT, con PT.
3. **Applica** `np.polyfit(x, y, 1)` su ciascun taglio e calcola R²:
   - `np.polyfit` usa decomposizione QR — più stabile della formula chiusa dei
     minimi quadrati con `int32`/`int64`, che può overfloware su Σx².
4. **Stampa** una tabella riassuntiva dei tre fit.
5. **Genera** un grafico a 3 pannelli (`output/regressione_leg_day.png`) che
   mostra scatter + retta di regressione per ogni taglio.

## Lettura dei risultati

| Taglio          | n  | Slope (kg/sett) | R²    | Interpretazione |
|-----------------|----|-----------------|-------|---|
| Tutto           | 40 | -23             | 0.015 | Due regimi mescolati → nessun trend |
| Pre-PT          | 34 | +23             | 0.007 | Allenamento autonomo → rumore puro |
| Con PT (6 sett) | 6  | +820            | 0.758 | Trend chiaro: +820 kg/settimana |

La **lezione didattica** è che un R² basso non significa "i dati non
contengono informazione" — può significare "stai chiedendo al modello di
descrivere due fenomeni con una sola retta". Segmentare il dataset secondo
la conoscenza del dominio (qui: il cambio di regime con il PT) è spesso il
passo che fa emergere il pattern.

## Note sul dataset

- Le settimane sono progressive da 0. Il salto tra `week_index=41` e `=53`
  corrisponde al gap di tracciamento di gennaio–marzo 2026: in quel periodo
  l'allenamento è continuato, ma i dati non sono stati registrati.
- `volume_kg = Σ (peso × ripetizioni)` su tutti gli esercizi del leg day di
  quella settimana.
- `n_sessions` è il numero di leg day completati nella settimana (1, 2 o 3).
