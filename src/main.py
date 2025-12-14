import pandas as pd
from preprocess import preprocess_series
from vectorize import vectorize_text
from cluster import run_kmeans
from summarize import top_words_per_cluster
from analyzer import analyze_sentiment, detect_tema, get_cluster_label, extract_top_keywords

print("="*60)
print("CLUSTERING WISATA BALIKPAPAN - TF-IDF & K-MEANS")
print("="*60)

# ===============================
# 1. LOAD DATA
# ===============================
print("\n[1/7] Loading data...")
df = pd.read_csv("../data/raw/wisata_balikpapan.csv")
print(f"   Total reviews: {len(df)}")
print(f"   Total tempat wisata: {df['wisata'].nunique()}")

# ===============================
# 2. PREPROCESS REVIEW
# ===============================
print("\n[2/7] Preprocessing reviews...")
df["clean_review"] = preprocess_series(df["review"])

# ===============================
# 3. GABUNG REVIEW PER TEMPAT
# ===============================
print("\n[3/7] Menggabungkan review per tempat...")
grouped = (
    df.groupby("wisata")["clean_review"]
    .apply(lambda x: " ".join(x))
    .reset_index()
)
grouped.rename(columns={"clean_review": "all_reviews"}, inplace=True)

# ===============================
# 4. TF-IDF (PER TEMPAT)
# ===============================
print("\n[4/7] Melakukan TF-IDF vectorization...")
vectorizer, X = vectorize_text(grouped["all_reviews"])
print(f"   Shape matrix: {X.shape}")

# ===============================
# 5. K-MEANS CLUSTERING
# ===============================
K = 3  # jumlah cluster
print(f"\n[5/7] Running K-Means (k={K})...")
model, labels = run_kmeans(X, k=K)
grouped["cluster"] = labels

# ===============================
# 6. ANALISIS TAMBAHAN
# ===============================
print("\n[6/7] Menganalisis sentimen dan tema...")

# Analisis per tempat
grouped[["kategori", "sentimen_score"]] = grouped["all_reviews"].apply(
    lambda x: pd.Series(analyze_sentiment(x))
)

grouped[["tema_utama", "tema_terkait"]] = grouped["all_reviews"].apply(
    lambda x: pd.Series(detect_tema(x))
)

grouped["kata_kunci"] = grouped["all_reviews"].apply(
    lambda x: ", ".join(extract_top_keywords(x, top_n=5))
)

# Analisis per cluster
cluster_summary = top_words_per_cluster(vectorizer, model, top_n=10)
cluster_labels = {c: get_cluster_label(words) for c, words in cluster_summary.items()}

grouped["cluster_label"] = grouped["cluster"].map(cluster_labels)

# ===============================
# 7. SIMPAN HASIL
# ===============================
print("\n[7/7] Menyimpan hasil...")

# Pilih kolom yang relevan untuk output
output_df = grouped[[
    "wisata", 
    "cluster", 
    "cluster_label",
    "kategori",
    "tema_utama",
    "kata_kunci",
    "tema_terkait"
]]

output_df.to_csv("../outputs/hasil_cluster_per_tempat.csv", index=False)

# Simpan juga detail cluster
cluster_detail = pd.DataFrame([
    {"cluster": c, "label": cluster_labels[c], "kata_dominan": ", ".join(words[:10])}
    for c, words in cluster_summary.items()
])
cluster_detail.to_csv("../outputs/detail_cluster.csv", index=False)

print("   ✓ Hasil disimpan ke '../outputs/hasil_cluster_per_tempat.csv'")
print("   ✓ Detail cluster disimpan ke '../outputs/detail_cluster.csv'")

# ===============================
# 8. CETAK HASIL
# ===============================
print("\n" + "="*60)
print("HASIL CLUSTERING")
print("="*60)

for cluster_id in sorted(grouped["cluster"].unique()):
    cluster_data = grouped[grouped["cluster"] == cluster_id]
    print(f"\n{'═'*60}")
    print(f"CLUSTER {cluster_id}: {cluster_labels[cluster_id]}")
    print(f"{'═'*60}")
    print(f"Jumlah tempat: {len(cluster_data)}")
    print(f"Kata dominan : {', '.join(cluster_summary[cluster_id][:8])}")
    print(f"\nDaftar tempat wisata:")
    
    for idx, (_, row) in enumerate(cluster_data.iterrows(), 1):
        print(f"\n  {idx}. {row['wisata']}")
        print(f"     • Kategori    : {row['kategori']}")
        print(f"     • Tema        : {row['tema_utama']}")
        print(f"     • Kata Kunci  : {row['kata_kunci']}")

print("\n" + "="*60)
print("CLUSTERING SELESAI!")
print("="*60)

# Statistik tambahan
print(f"\nStatistik:")
print(f"- Total tempat wisata   : {len(grouped)}")
print(f"- Jumlah cluster        : {K}")
print(f"- Kategori 'Sangat Baik': {len(grouped[grouped['kategori'] == 'Sangat Baik'])}")
print(f"- Kategori 'Baik'       : {len(grouped[grouped['kategori'] == 'Baik'])}")
print(f"- Kategori 'Kurang Baik': {len(grouped[grouped['kategori'] == 'Kurang Baik'])}")
print(f"- Kategori 'Netral'     : {len(grouped[grouped['kategori'] == 'Netral'])}")