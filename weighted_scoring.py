# ==============================
# IMPORT
# ==============================
import pandas as pd
import re

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("raw_data.csv")
pairs_df = pd.read_csv("similar_pairs_nama.csv")

# ==============================
# CLEAN COLUMN NAMES
# ==============================
df.columns = (
    df.columns
    .str.lower()
    .str.strip()
    .str.replace(" ", "_")
    .str.replace("/", "_")
)

pairs_df.columns = pairs_df.columns.str.lower()

print("Columns:", df.columns)

# ==============================
# DEFINE COLUMNS
# ==============================
NAMA_COL = "paket"
KL_COL = "klpd"
SATKER_COL = "satuan_kerja"

# ==============================
# CLEAN TEXT
# ==============================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['nama_clean'] = df[NAMA_COL].apply(clean_text)

# ==============================
# EXACT MATCH FUNCTION
# ==============================
def exact_match(a, b):
    return 1 if str(a) == str(b) else 0

# ==============================
# WEIGHTED SCORING
# ==============================
def calculate_score(row):
    i = int(row['idx1'])
    j = int(row['idx2'])
    
    nama_sim = row['similarity']
    kl = exact_match(df.loc[i, KL_COL], df.loc[j, KL_COL])
    satker = exact_match(df.loc[i, SATKER_COL], df.loc[j, SATKER_COL])
    
    final_score = (
        0.6 * nama_sim +
        0.2 * kl +
        0.2 * satker
    )
    
    return final_score

pairs_df['final_score'] = pairs_df.apply(calculate_score, axis=1)

# ==============================
# CLASSIFICATION
# ==============================
pairs_df['predicted_label'] = pairs_df['final_score'].apply(
    lambda x: "mirip" if x > 0.8 else "tidak"
)

# ==============================
# SAVE
# ==============================
pairs_df.to_csv("final_classification.csv", index=False)

print("✅ DONE")
print(pairs_df[['nama_1', 'nama_2', 'final_score', 'predicted_label']].head())