import numpy as np
from collections import Counter

# ===============================
# KEYWORD UNTUK SENTIMEN
# ===============================
POSITIVE_WORDS = {
    'bagus', 'indah', 'cantik', 'bersih', 'nyaman', 'asri', 'sejuk', 'tenang',
    'recommended', 'mantap', 'keren', 'amazing', 'spectacular', 'beautiful',
    'great', 'excellent', 'wonderful', 'nice', 'good', 'best', 'love', 'enjoy',
    'menyenangkan', 'menakjubkan', 'luar', 'biasa', 'sempurna', 'favorit',
    'suka', 'puas', 'top', 'oke', 'istimewa', 'elok', 'adem', 'fresh',
    'jernih', 'terawat', 'rapi', 'strategis', 'lengkap', 'terjangkau'
}

NEGATIVE_WORDS = {
    'kotor', 'jorok', 'bau', 'rusak', 'buruk', 'jelek', 'tidak', 'kurang',
    'kecewa', 'mengecewakan', 'bad', 'poor', 'dirty', 'terrible', 'awful',
    'waste', 'boring', 'disappointing', 'sesak', 'ramai', 'macet', 'mahal',
    'berbahaya', 'seram', 'sepi', 'kumuh', 'sempit', 'panas', 'jorok'
}

# ===============================
# KEYWORD UNTUK TEMA WISATA
# ===============================
TEMA_KEYWORDS = {
    'pantai': ['pantai', 'beach', 'laut', 'pasir', 'ombak', 'sunset', 'sunrise', 
               'diving', 'snorkeling', 'sea', 'ocean', 'tepi', 'pesisir'],
    
    'hutan': ['hutan', 'forest', 'pohon', 'hijau', 'jungle', 'trek', 'hiking', 
              'mangrove', 'rimba', 'pepohonan', 'kanopi', 'bakau'],
    
    'air_terjun': ['air terjun', 'waterfall', 'curug', 'sungai', 'kolam', 
                   'river', 'air', 'mengalir', 'terjun'],
    
    'taman': ['taman', 'park', 'bunga', 'kebun', 'garden', 'tanaman', 
              'raya', 'kota', 'jogging'],
    
    'religi': ['masjid', 'mosque', 'church', 'gereja', 'vihara', 'temple', 
               'religious', 'islami', 'ibadah', 'agung', 'mushola'],
    
    'kuliner': ['makan', 'kuliner', 'food', 'resto', 'restaurant', 'cafe', 
                'kopi', 'coffee', 'rumah makan', 'seafood', 'warung', 'menu'],
    
    'edukasi': ['museum', 'edukasi', 'belajar', 'pengetahuan', 'sejarah', 
                'history', 'konservasi', 'satwa', 'education', 'budaya'],
    
    'belanja': ['belanja', 'shopping', 'mall', 'toko', 'souvenir', 'oleh oleh',
                'pasar', 'plaza', 'tenant', 'store']
}

# ===============================
# FUNGSI ANALISIS SENTIMEN
# ===============================
def analyze_sentiment(text):
    """
    Analisis sentimen dari teks review
    
    Returns:
    - kategori: Sangat Baik / Baik / Kurang Baik / Netral
    - skor: skor sentimen (positif - negatif)
    """
    words = set(text.lower().split())
    
    pos_count = len(words & POSITIVE_WORDS)
    neg_count = len(words & NEGATIVE_WORDS)
    
    # Hitung skor sentimen
    score = pos_count - neg_count
    
    # Tentukan kategori berdasarkan skor
    if pos_count > neg_count * 1.5:
        return "Sangat Baik", score
    elif pos_count > neg_count:
        return "Baik", score
    elif neg_count > pos_count:
        return "Kurang Baik", score
    else:
        return "Netral", 0

# ===============================
# FUNGSI DETEKSI TEMA
# ===============================
def detect_tema(text):
    """
    Deteksi tema wisata berdasarkan keywords
    
    Returns:
    - tema_utama: tema dengan skor tertinggi
    - tema_terkait: list tema lainnya yang relevan
    """
    text_lower = text.lower()
    tema_scores = {}
    
    # Hitung skor untuk setiap tema
    for tema, keywords in TEMA_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            tema_scores[tema] = score
    
    # Jika tidak ada tema yang terdeteksi
    if not tema_scores:
        return "Umum", []
    
    # Urutkan tema berdasarkan skor
    sorted_temas = sorted(tema_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Format nama tema (ganti underscore dengan spasi, capitalize)
    tema_utama = sorted_temas[0][0].replace('_', ' ').title()
    tema_terkait = [t[0].replace('_', ' ').title() for t in sorted_temas[:3]]
    
    return tema_utama, tema_terkait

# ===============================
# FUNGSI LABEL CLUSTER
# ===============================
def get_cluster_label(keywords):
    """
    Beri label cluster berdasarkan kata kunci dominan
    
    Returns:
    - label: format "Sentimen - Tema"
    """
    keyword_text = " ".join(keywords)
    
    # Cek sentimen dari keywords
    pos_count = sum(1 for w in keywords if w in POSITIVE_WORDS)
    neg_count = sum(1 for w in keywords if w in NEGATIVE_WORDS)
    
    if pos_count > neg_count:
        sentiment = "Positif"
    elif neg_count > pos_count:
        sentiment = "Negatif"
    else:
        sentiment = "Netral"
    
    # Deteksi tema dari keywords
    tema, _ = detect_tema(keyword_text)
    
    return f"{sentiment} - {tema}"

# ===============================
# FUNGSI EKSTRAK KATA KUNCI
# ===============================
def extract_top_keywords(text, top_n=5):
    """
    Ekstrak kata kunci paling sering muncul
    
    Returns:
    - list kata kunci teratas
    """
    words = text.lower().split()
    
    # Filter kata dengan panjang minimal 3 karakter
    words = [w for w in words if len(w) > 3]
    
    # Hitung frekuensi kata
    word_freq = Counter(words)
    
    # Ambil top N kata
    top_words = [word for word, count in word_freq.most_common(top_n)]
    
    return top_words