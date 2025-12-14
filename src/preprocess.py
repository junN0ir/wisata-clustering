import re

# Stopwords Bahasa Indonesia (tambahkan sesuai kebutuhan)
STOPWORDS_ID = {
    'yang', 'untuk', 'pada', 'ke', 'para', 'namun', 'menurut', 'antara', 'dia',
    'dua', 'ia', 'seperti', 'jika', 'jika', 'sehingga', 'kembali', 'dan', 'tidak',
    'ini', 'karena', 'oleh', 'itu', 'dalam', 'dari', 'tersebut', 'bahwa', 'akan',
    'dengan', 'di', 'ada', 'adalah', 'atau', 'juga', 'sudah', 'bisa', 'dapat',
    'saya', 'kita', 'kami', 'mereka', 'anda', 'nya', 'kok', 'sih', 'deh', 'dong',
    'aja', 'yg', 'dgn', 'utk', 'gak', 'ga', 'si', 'ke', 'dr', 'sama'
}

def clean_text(text: str) -> str:
    """Membersihkan teks dari noise dan normalisasi"""
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    # Hapus URL
    text = re.sub(r"http\S+|www\S+", " ", text)
    # Hapus mention/hashtag jika ada
    text = re.sub(r"@\w+|#\w+", " ", text)
    # Hapus angka dan karakter khusus, tapi pertahankan huruf
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    # Hapus whitespace berlebih
    text = re.sub(r"\s+", " ", text).strip()
    
    # Hapus stopwords
    words = text.split()
    words = [w for w in words if w not in STOPWORDS_ID and len(w) > 2]
    
    return " ".join(words)

def preprocess_series(series):
    """Apply cleaning ke seluruh series"""
    return series.fillna("").apply(clean_text)