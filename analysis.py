# ==============================
# 1. LOAD DATA
# ==============================
import pandas as pd

df = pd.read_csv("raw_data.csv")
pairs_df = pd.read_csv("final_classification.csv")

# ==============================
# 2. CLEAN COLUMN NAMES
# ==============================
df.columns = (
    df.columns
    .str.lower()
    .str.strip()
    .str.replace(" ", "_")
    .str.replace("/", "_")
)

pairs_df.columns = pairs_df.columns.str.lower()

# ==============================
# 3. DEFINE COLUMNS
# ==============================
PAGU_COL = "pagu"
KL_COL = "klpd"
SATKER_COL = "satuan_kerja"
LOKASI_COL = "lokasi"

# ==============================
# 4. CLEAN PAGU
# ==============================
def clean_rupiah(x):
    x = str(x)
    x = x.replace("Rp", "").replace(".", "").replace(",", "")
    try:
        return float(x)
    except:
        return None

df[PAGU_COL] = df[PAGU_COL].apply(clean_rupiah)

# ==============================
# 5. CALCULATE BUDGET DIFFERENCE
# ==============================
def budget_diff(i, j):
    a = df.loc[i, PAGU_COL]
    b = df.loc[j, PAGU_COL]
    
    if a is None or b is None or a == 0 or b == 0:
        return 0
    
    return abs(a - b) / max(a, b)

pairs_df['budget_diff'] = pairs_df.apply(
    lambda row: budget_diff(int(row['idx1']), int(row['idx2'])),
    axis=1
)

# ==============================
# 6. ATTRIBUTE DIFFERENCE
# ==============================
def diff(a, b):
    return 1 if str(a) != str(b) else 0

pairs_df['kl_diff'] = pairs_df.apply(
    lambda row: diff(
        df.loc[row['idx1'], KL_COL],
        df.loc[row['idx2'], KL_COL]
    ),
    axis=1
)

pairs_df['satker_diff'] = pairs_df.apply(
    lambda row: diff(
        df.loc[row['idx1'], SATKER_COL],
        df.loc[row['idx2'], SATKER_COL]
    ),
    axis=1
)

pairs_df['lokasi_diff'] = pairs_df.apply(
    lambda row: diff(
        df.loc[row['idx1'], LOKASI_COL],
        df.loc[row['idx2'], LOKASI_COL]
    ),
    axis=1
)

# ==============================
# 7. FILTER ANOMALY
# ==============================
anomaly = pairs_df[
    (pairs_df['final_score'] > 0.8) &
    (
        (pairs_df['budget_diff'] > 0.5) |
        (pairs_df['kl_diff'] == 1) |
        (pairs_df['satker_diff'] == 1)
    )
]

print("Total anomaly:", len(anomaly))

# ==============================
# 8. SAVE RESULT
# ==============================
anomaly.to_csv("anomaly_cases.csv", index=False)

# ==============================
# 9. SIMPLE VISUALIZATION
# ==============================
import matplotlib.pyplot as plt

plt.figure()
anomaly['budget_diff'].hist(bins=20)
plt.title("Distribusi Perbedaan Anggaran")
plt.xlabel("Budget Difference")
plt.ylabel("Jumlah Kasus")
plt.show()