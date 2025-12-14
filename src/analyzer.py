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
# KATA FUNGSIONAL (DIABAIKAN)
# ===============================
FUNCTIONAL_WORDS = {
    # Kata hubung
    'tentang', 'untuk', 'dengan', 'dari', 'kepada', 'oleh', 'terhadap',
    'atas', 'bagi', 'hingga', 'sampai', 'sejak', 'selama', 'antara',
    
    # Kata keterangan
    'agak', 'sangat', 'cukup', 'terlalu', 'paling', 'lebih', 'kurang',
    'sekali', 'banget', 'amat', 'benar', 'sungguh', 'bahkan', 'hanya',
    'saja', 'juga', 'pun', 'lah', 'kah',
    
    # Kata depan
    'berbagai', 'beberapa', 'banyak', 'semua', 'setiap', 'seluruh',
    'masing', 'tiap', 'para',
    
    # Kata tambahan
    'jadi', 'menjadi', 'akan', 'telah', 'sudah', 'belum', 'masih',
    'sedang', 'tengah', 'lagi', 'kembali', 'terus', 'tetap',
    
    # Kata ganti
    'saya', 'kamu', 'anda', 'kita', 'kami', 'mereka', 'dia',
    'nya', 'ini', 'itu', 'sini', 'situ', 'sana',
    
    # Kata kerja umum yang tidak informatif
    'ada', 'adalah', 'ialah', 'yaitu', 'yakni', 'bahwa', 'kalau',
    'jika', 'bila', 'maka', 'lalu', 'kemudian', 'namun', 'tetapi',
    
    # Kata bahasa Inggris umum
    'the', 'and', 'for', 'with', 'from', 'this', 'that', 'very',
    'too', 'also', 'than', 'some', 'many', 'much', 'more', 'most'
}

# ===============================
# KATA SIFAT & KATA BENDA (PRIORITAS)
# ===============================
# Kata sifat (adjective) - deskripsi kualitas
ADJECTIVES = {
    # Ukuran
    'besar', 'kecil', 'luas', 'sempit', 'tinggi', 'rendah', 'panjang', 'pendek',
    'banyak', 'sedikit', 'tebal', 'tipis',
    
    # Warna
    'putih', 'hitam', 'merah', 'biru', 'hijau', 'kuning', 'coklat', 'abu',
    
    # Kondisi
    'bersih', 'kotor', 'jernih', 'keruh', 'terang', 'gelap', 'basah', 'kering',
    'baru', 'lama', 'rusak', 'utuh', 'rapih', 'berantakan',
    
    # Suhu & Sensasi
    'panas', 'dingin', 'sejuk', 'hangat', 'segar', 'pengap',
    
    # Kualitas
    'bagus', 'jelek', 'indah', 'cantik', 'buruk', 'baik', 'elok', 'menawan',
    'megah', 'sederhana', 'mewah', 'biasa', 'istimewa', 'unik', 'langka',
    
    # Suasana
    'tenang', 'ramai', 'sepi', 'sunyi', 'ribut', 'gaduh', 'hening',
    'nyaman', 'asri', 'natural', 'alami',
    
    # Emosi/Pengalaman
    'menyenangkan', 'membosankan', 'menakjubkan', 'mengecewakan',
    'menarik', 'menegangkan', 'melelahkan', 'menyegarkan',
    
    # Bentuk
    'bulat', 'kotak', 'persegi', 'bundar', 'lonjong', 'cembung', 'cekung',
    
    # Tekstur
    'halus', 'kasar', 'lembut', 'keras', 'lunak', 'licin', 'berbatu',
    
    # Jarak & Posisi
    'dekat', 'jauh', 'atas', 'bawah', 'dalam', 'dangkal', 'tersembunyi',
    
    # Kecepatan
    'cepat', 'lambat', 'pelan', 'tenang', 'deras',
    
    # Usia
    'muda', 'tua', 'modern', 'kuno', 'klasik', 'kontemporer',
    
    # Bahasa Inggris
    'beautiful', 'amazing', 'wonderful', 'spectacular', 'gorgeous',
    'stunning', 'magnificent', 'awesome', 'cool', 'nice', 'great',
    'clean', 'dirty', 'clear', 'fresh', 'natural', 'calm', 'quiet',
    'crowded', 'empty', 'hot', 'cold', 'warm', 'cool'
}

# Kata benda (noun) - objek konkret
NOUNS = {
    # Alam
    'pantai', 'laut', 'pasir', 'ombak', 'air', 'sungai', 'danau', 'kolam',
    'gunung', 'bukit', 'tebing', 'batu', 'karang', 'gua',
    'hutan', 'pohon', 'tanaman', 'bunga', 'rumput', 'daun', 'ranting',
    'sunset', 'sunrise', 'matahari', 'bulan', 'bintang', 'awan', 'langit',
    
    # Fauna
    'ikan', 'burung', 'monyet', 'orangutan', 'beruang', 'harimau', 'gajah',
    'kerbau', 'sapi', 'kambing', 'ayam', 'bebek', 'kucing', 'anjing',
    'lumba', 'pesut', 'penyu', 'kepiting', 'udang',
    
    # Bangunan & Infrastruktur
    'jembatan', 'jalan', 'gang', 'lorong', 'tangga', 'pagar', 'pintu', 'gerbang',
    'masjid', 'gereja', 'vihara', 'museum', 'taman', 'kebun',
    'warung', 'resto', 'restaurant', 'cafe', 'mall', 'plaza', 'pasar', 'toko',
    'hotel', 'penginapan', 'villa', 'cottage',
    'toilet', 'kamar', 'mandi', 'mushola', 'parkir',
    
    # Fasilitas
    'gazebo', 'ayunan', 'bangku', 'meja', 'kursi', 'panggung', 'arena',
    'kanopi', 'shelter', 'spot', 'area', 'zona', 'lokasi', 'tempat',
    
    # Transportasi
    'mobil', 'motor', 'sepeda', 'perahu', 'kapal', 'sampan', 'speed boat',
    
    # Makanan & Minuman
    'makanan', 'minuman', 'seafood', 'ikan bakar', 'kopi', 'teh', 'jus',
    'nasi', 'mie', 'sate', 'bakso', 'soto', 'menu', 'hidangan',
    
    # Aktivitas & Objek Wisata
    'pemandangan', 'view', 'landscape', 'panorama', 'vista',
    'foto', 'picture', 'selfie', 'dokumentasi',
    'tracking', 'trekking', 'hiking', 'jogging', 'camping',
    'diving', 'snorkeling', 'swimming', 'berenang',
    
    # Lainnya
    'tiket', 'harga', 'biaya', 'uang', 'rupiah',
    'orang', 'pengunjung', 'wisatawan', 'turis', 'guide', 'staff',
    'keluarga', 'anak', 'teman', 'pasangan',
    
    # Bahasa Inggris
    'beach', 'sea', 'ocean', 'forest', 'tree', 'flower', 'garden',
    'bridge', 'gate', 'entrance', 'waterfall', 'river', 'lake',
    'monkey', 'bird', 'fish', 'dolphin', 'turtle',
    'sunset', 'sunrise', 'view', 'landscape', 'food', 'restaurant'
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
# FUNGSI EKSTRAK KATA KUNCI (IMPROVED)
# ===============================
def extract_top_keywords(text, top_n=5):
    """
    Ekstrak kata kunci paling sering muncul
    HANYA kata sifat (adjective) dan kata benda (noun)
    TIDAK termasuk kata fungsional
    
    Returns:
    - list kata kunci teratas
    """
    words = text.lower().split()
    
    # Filter: hanya ambil kata sifat dan kata benda, buang kata fungsional
    filtered_words = []
    for word in words:
        # Skip jika kata terlalu pendek
        if len(word) <= 3:
            continue
        
        # Skip jika kata fungsional
        if word in FUNCTIONAL_WORDS:
            continue
        
        # Ambil hanya kata sifat atau kata benda
        if word in ADJECTIVES or word in NOUNS:
            filtered_words.append(word)
    
    # Hitung frekuensi kata
    word_freq = Counter(filtered_words)
    
    # Ambil top N kata
    top_words = [word for word, count in word_freq.most_common(top_n)]
    
    return top_words