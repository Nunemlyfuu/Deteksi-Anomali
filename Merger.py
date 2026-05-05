import pandas as pd
import glob
import os

print("Current directory:", os.getcwd())

# path to your folder
path = "A:/Campus Life/ITS/Sem 2/ID/Sirup Data_Belanja Perjalanan Dinas/*.xlsx"

# get all files
files = glob.glob(path)

print(f"Found {len(files)} files")

# combine all
df_list = []

for file in files:
    print(f"Reading {file}")
    temp_df = pd.read_excel(file)
    df_list.append(temp_df)

# safety check
if not df_list:
    raise ValueError("No files found. Check your path.")

# merge
df = pd.concat(df_list, ignore_index=True)

# save merged file
output_path = "A:\Campus Life\ITS\Sem 2\ID\sirup_merged.csv"
df.to_csv(output_path, index=False)

print(f"✅ Saved to: {output_path}")
print("📊 Total rows:", len(df))