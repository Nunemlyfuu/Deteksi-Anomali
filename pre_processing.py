# ==============================
# 1. LOAD DATA
# ==============================
import pandas as pd
import re

df = pd.read_csv("raw_data.csv")

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

print("Columns:", df.columns)

# ==============================
# 3. DEFINE COLUMN
# ==============================
NAMA_COL = "paket"  # <-- based on your fixed column

# ==============================
# 4. CLEAN TEXT (NAMA PAKET ONLY)
# ==============================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['nama_clean'] = df[NAMA_COL].apply(clean_text)

# remove empty rows
df = df[df['nama_clean'] != ""].reset_index(drop=True)

print("Data after cleaning:", len(df))

# ==============================
# 5. TF-IDF + COSINE SIMILARITY
# ==============================
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['nama_clean'])

# ==============================
# 6. FIND SIMILAR PAIRS (> 0.8)
# (OPTIMIZED - NO FULL O(n²))
# ==============================
from sklearn.neighbors import NearestNeighbors
import numpy as np

threshold = 0.8
top_k = 5

nn = NearestNeighbors(n_neighbors=top_k, metric='cosine')
nn.fit(tfidf_matrix)

distances, indices = nn.kneighbors(tfidf_matrix)

pairs = []

for i in range(len(indices)):
    for j_idx, dist in zip(indices[i], distances[i]):
        if i != j_idx:
            sim = 1 - dist
            if sim > threshold:
                pairs.append((i, j_idx, sim))

pairs_df = pd.DataFrame(pairs, columns=['idx1', 'idx2', 'similarity'])

# remove duplicate pairs
pairs_df['pair_key'] = pairs_df.apply(
    lambda row: tuple(sorted((row['idx1'], row['idx2']))), axis=1
)
pairs_df = pairs_df.drop_duplicates(subset='pair_key').drop(columns='pair_key')

print("Total similar pairs (>0.8):", len(pairs_df))

# ==============================
# 7. MAP BACK TO ORIGINAL DATA
# ==============================
pairs_df['nama_1'] = pairs_df['idx1'].apply(lambda x: df.loc[x, NAMA_COL])
pairs_df['nama_2'] = pairs_df['idx2'].apply(lambda x: df.loc[x, NAMA_COL])

# ==============================
# 8. SEMI-MANUAL LABELING SAMPLE
# ==============================
sample_size = min(30, len(pairs_df))

sample_df = pairs_df.sample(sample_size, random_state=42).copy()
sample_df['label_manual'] = ""  # isi: mirip / tidak

# ==============================
# 9. SAVE OUTPUT
# ==============================
pairs_df.to_csv("similar_pairs_nama.csv", index=False)
sample_df.to_csv("label_sample.csv", index=False)

print("✅ DONE")
print("Generated files:")
print("- similar_pairs_nama.csv")
print("- label_sample.csv")